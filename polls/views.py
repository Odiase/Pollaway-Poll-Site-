from distutils.command import check
from django.contrib.auth.models import User
from django.http import HttpResponse,response
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail

from notifications.models import Notification
from user_account.models import Followers

from .models import (Poll,Poll_Option,Poll_Vote,Featured_Polls)
from .forms import PollForm

# non-view function (used in the voting view)
def check_blank_options(request,options):
    unblank_options = 0
    blank_options = False
    for option in options:
        if len(option) != 0:
            unblank_options+=1
    if unblank_options < 2:
            blank_options = True
    return blank_options


# Create your views here.
@login_required(login_url="login")
def all_polls(request):

    # this function removes duplicated results from the different categories that the results are coming from
    def add_to_queried_polls(array):
        for i in array:
            if i in queried_polls:
                pass
            else:
                queried_polls.append(i)

    # gets the required polls based on the filters available in the all-polls page
    q = request.GET.get("q") if request.GET.get("q") != None else ''
    queried_polls = Poll.objects.filter(category__icontains = q, public = True )
    search_input = ""
    user = request.user

    filtered_queried_polls = []
    following_polls = [] # holding the polls of users, this user is following

    if request.method == "POST":
        queried_polls = []
        search_input = request.POST["search-input"]
        poll_user_result = Poll.objects.filter(user__username = search_input, public = True)
        poll_title_result = Poll.objects.filter(title__icontains = search_input, public = True)
        poll_category_result = Poll.objects.filter(category__icontains = search_input, public = True)
        
        '''add all the poll objects to the queried_polls list gootten from the various search categories'''
        add_to_queried_polls(poll_title_result)
        add_to_queried_polls(poll_category_result)
        add_to_queried_polls(poll_user_result)


    for poll in queried_polls:
        # filtering the polls this current user is already involved in
        if Featured_Polls.objects.filter(user = user,polls = poll).exists() or poll.user == user:
            pass
        else:
            if poll.is_expired():
                pass
            elif Followers.objects.filter(user = poll.user, my_followers = user).exists():
                following_polls.append(poll)
            else:
                following_polls.append(poll)

    num_of_queried_polls = len(filtered_queried_polls)
    context = {
        "polls":filtered_queried_polls,
        "lop":num_of_queried_polls,
        "following_polls":following_polls,
        "lofp":len(following_polls)
    }
    return render(request,"polls/all-polls.html",context)


@login_required(login_url="sign-up")
def create_poll(request):
    form = PollForm()
    if request.method == "POST":
    # poll data
        user = request.user
        title = request.POST['title']
        category = request.POST["category"]
    # try to get the options below if they exist
        try:
            public = request.POST["public"]
        except:
            public = ""
        try:
            multiple_choices = request.POST["multiple_option_selection"]
        except:
            multiple_choices = ""
    # check and get images if there are
        try:
            image1 = request.FILES["image1"]
        except:
            image1 = ""
        try:
            image2 = request.FILES["image2"]
        except:
            image2 = ""   
    # poll option data
        options = request.POST.getlist("option")
    # cleaning the form
        # converting the options values to a value that the model understands
        if public:
            public = True
        else:
            public == False
        
        if multiple_choices:
            multiple_choices = True
        else:
            multiple_choices = False
        
        # checking for empty poll submissions
        if check_blank_options(request, options) == True:
            messages.info(request,"Pls Include AT Least 2 Options")
            return redirect("create-poll")
        if title == "" and image1 == "" or title == "" and image2 == "":
            messages.info(request,"pls include A Title or An Image")
            return redirect("create-poll")

    # save the poll and the options 
        poll = Poll.objects.create(user = user,title = title,category = category,public = public,image1 = image1, image2 = image2,multiple_option_selection = multiple_choices)
        for option in options:
            if option == "":
                pass
            else:
                Poll_Option.objects.create(poll = poll, option = option)
        return redirect("single-poll", poll.id)
    context = {
        "form":form
    }
    return render(request,"polls/create-poll.html",context)


@login_required(login_url="login")
def single_poll(request,id):
    poll = Poll.objects.get(id = id)
    poll_options = len(poll.option.all())
    is_featured = False
    if Featured_Polls.objects.filter(user = request.user,polls = poll).exists():
        is_featured = True
    context = {
        "poll":poll,
        "poll_options":poll_options,
        "featured":is_featured,
    }
    return render(request,"polls/single-poll.html",context)


@login_required(login_url="login")
def my_polls(request):
    user_polls = Poll.objects.filter(user = request.user)
    user_featured_polls,created = Featured_Polls.objects.get_or_create(user = request.user)
    featured_polls = user_featured_polls.polls.all()
    l_o_f_p = len(featured_polls)
    l_o_u_p = len(user_polls)
    context = {
        "personal_polls":user_polls,
        "other_polls":featured_polls,
        "lofp":l_o_f_p,
        "loup":l_o_u_p,

    }
    return render(request,"polls/my-polls.html",context)



############################################### POll Features and functionalities #########################################

@login_required(login_url="login")
def vote(request):
    # adding this poll to the user's featured polls
    def add_to_featured(voter,poll):
        user_featured_polls,created = Featured_Polls.objects.get_or_create(user = voter)
        # checking if the user is the creator of the poll
        if poll.user == voter:
            pass
        else:
            user_featured_polls.polls.add(poll)
    
    multiple_choices = False
    if request.method == "POST":
        voter = request.user
        options = request.POST.getlist("option")
        poll = Poll.objects.get(id = request.POST["poll-id"])

        if poll.is_expired():
            return HttpResponse(status = 403)

    # checks if the options list submitted is empty
        if options:
            if Poll_Option.objects.get(id = int(options[0])).poll.multiple_option_selection == True: # checking the status of the poll's multiple choices
                multiple_choices = True
        
        if multiple_choices == True:
            for option in options:
                option = Poll_Option.objects.get(id = int(option))
                if Poll_Vote.objects.filter(voter = voter, poll_option = option).exists(): # checks if the user already checked this option
                    pass
                else:
                    Poll_Vote.objects.create(voter = voter, poll_option = option)
                    add_to_featured(voter,poll)
                    messages.info(request, "Poll Saved Succesfully")
        else:
            fraud = False
            option = Poll_Option.objects.get(id = int(options[0]))
            poll_options = poll.option.all()  # getting the other poll options
            for single_option in poll_options:
                if Poll_Vote.objects.filter(voter = voter,poll_option = single_option).exists(): # checking if the user has already voted on this poll
                    fraud = True
            
            if fraud == True:
                pass
            else:
                Poll_Vote.objects.create(voter = voter, poll_option = option)
                add_to_featured(voter,poll)
                messages.success(request, "Poll Saved Succesfully")
        return redirect("polls")


@login_required(login_url="login")
def delete_poll(request,id):
    poll = Poll.objects.get(id = id)
    poll.delete()
    return redirect("my-polls")

@login_required(login_url="login")
def remove_featured_poll(request,id):
    poll = Poll.objects.get(id = id)
    user_featured_polls = Featured_Polls.objects.get(user = request.user).polls
    user_featured_polls.remove(poll)
    return redirect("my-polls")