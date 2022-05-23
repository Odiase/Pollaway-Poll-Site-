from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User

from polls.views import my_polls

from .models import Profile,Followers
from .forms import ProfileForm

from notifications.models import Notification
from user_settings.models import Settings
from polls.models import Poll

default_image_path = f"{settings.BASE_DIR}/media/profile_images/default-image.jpg"

# Create your views here.

@login_required(login_url="login", redirect_field_name="my-account")
def account_page(request):
    no_of_followers = 0
    no_of_following = 0
    has_a_profile = False

    # getting the user's followers, if he or she has any
    try:
        no_of_followers = len(Followers.objects.get(user = request.user).my_followers.all())
    except:
        pass

    # getting the people that the user is following
    try:
        no_of_following = len(Followers.objects.filter(my_followers = request.user))
    except:
        pass

    if Profile.objects.filter(user = request.user).exists():
        has_a_profile = True

    context = {
        "n_o_followers":no_of_followers,
        "n_o_following":no_of_following,
        "has_a_profile":has_a_profile,
    }
    return render(request,"user_account/account.html",context)


######################################################### PROFILE VIEWS ####################################################
@login_required(login_url="login")
def profile(request,id):
    user = User.objects.get(id = id)
    allow_followers = True
    has_followers = False
    is_a_follower = False
    hide_profile = False
    user_settings,created = Settings.objects.get_or_create(user = user)
    user_polls = len(Poll.objects.filter(user = user))

    try:
        profile = Profile.objects.get(user = user)
        if profile.image == "": # checking if the user has deleted the default image and setting a new one if deleted
            profile.image = default_image_path
            profile.save()

        #checking the user's setting to see if the user wants profile to be hidden
        if user_settings.hide_profile == True and profile.user != request.user:
            hide_profile = True
            return HttpResponse(status = 403)
    except:
        return HttpResponse(status = 404)
        
    # checks if the profile user has followers
    try:
        profile_user_followers = len(Followers.objects.get(user = user).my_followers.all())
        if profile_user_followers > 0:
            has_followers = True
    except:
        profile_user_followers = 0
    # checks if this is not the owner of this profile and if he/she is a follower of this profile's user
    if request.user != profile.user and Followers.objects.filter(user = user, my_followers = request.user).exists():
        is_a_follower = True

    context = {
        "profile":profile,
        "is_a_follower":is_a_follower,
        "no_of_followers":profile_user_followers,
        "setting":user_settings,
        "polls":user_polls,
    }
    return render(request,"user_account/profile.html",context)


@login_required(login_url="login")
def create_profile(request):
    if Profile.objects.filter(user = request.user).exists():
        return redirect("profile",request.user.id)

    form = ProfileForm()    
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            dummy = form.save(commit = False)
            dummy.user = request.user
            dummy.save()
            return redirect("profile", request.user.id)

    context = {"form":form}
    return render(request,"user_account/create_profile.html",context)


@login_required(login_url="login")
def update_profile(request):
    # check for user profile existence
    if Profile.objects.filter(user = request.user).exists():
        profile = Profile.objects.get(user = request.user)
        form = ProfileForm(instance = profile)
    else:
        return redirect("create-profile")

    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance = profile)
        if form.is_valid():
            form.save()
            return redirect("profile",request.user.id)
    context = {"form":form}
    return render(request,"user_account/update-profile.html",context)


@login_required(login_url="login")
def delete_profile(request):
    user = request.user
    #security measures
    if Profile.objects.filter(user = user).exists():
        profile = Profile.objects.get(user = user)

        if request.method == "POST":
            profile.delete()
            return redirect("my-account")
    else:
        return redirect("create-profile")
    return render(request,"user_account/delete-profile.html")


######################################################### FOLLOW VIEWS ####################################################
@login_required(login_url="login")
def follow(request,id):
    request_user = request.user
    allow_followers = True
    other_user = User.objects.get(id = id) # the other user, you want to follow
    user_settings,created = Settings.objects.get_or_create(user = other_user)
    
    # checking if the user doesnt want any followers
    if user_settings.allow_followers == False:
        return redirect("profile",other_user.id)
    # security verification to avoid unnecessary bugs
    if request_user == other_user:
        return redirect("profile",other_user.id)


    if request.method == "POST":
        # checks if this request's user is already a follower, so as not to dulicate notifications
        if Followers.objects.filter(user = other_user,my_followers = request_user).exists():
            return redirect("profile",other_user.id)
        else:
            # try to get the other_user's followers accnt, if its nt available, create a new one for the other user
            other_user_followers,created = Followers.objects.get_or_create(user = other_user) #the other user's followers account
            other_user_followers.my_followers.add(request_user)

            #send out notifications to both users
            notification = Notification.objects.create(user = request.user,message = f"You Are Now Following {other_user.username}")
            notification.save()
            other_user_notification = Notification.objects.create(user = other_user,message = f"{request_user.username} Started Following You")
            other_user_notification.save()

            return redirect("profile",other_user.id)


@login_required(login_url="login")
def unfollow(request,id):
    request_user = request.user
    other_user = User.objects.get(id = id) # the user you want to unfollow
    #security verfification to avoid crashing our program
    if request_user == other_user:
        return redirect("profile",other_user.id)
    
    if request.method == "POST":
        Followers.objects.get(user = other_user).my_followers.remove(request_user)

        # sends out notification to both users
        notification = Notification.objects.create(user = request_user,message = f"You Have Unfollowed {other_user.username}")
        notification.save()
        other_user_notification = Notification.objects.create(user = other_user,message = f"{request_user.username} Stopped Following You")
        other_user_notification.save()

        return redirect("profile",other_user.id)


@login_required(login_url="login")
def my_followers(request,id):
    user = User.objects.get(id = id)
    hide_followers = Settings.objects.get(user = user).hide_subscribers
    follower_account_user = Followers.objects.get(user = user) # gets the user's followers account
    followers = follower_account_user.my_followers.all()
    if hide_followers:
        if follower_account_user.user == request.user:
            pass
        else:
            return HttpResponse("<h1>You Are Not Allowed To See This User's Followers</h1>")
    length_of_followers = len(followers)
    context = {
        "followers":followers,
        "l_o_p":length_of_followers,
        "hide_followers":hide_followers,
    }
    return render(request,"user_account/followers.html",context)


@login_required(login_url="login")
def following(request,id):
    user = User.objects.get(id = id)
    following = Followers.objects.filter(my_followers = user) # the accounts the user follows
    length_of_following = len(following)
    context = {
        "following":following,
        "lof":length_of_following
    }
    print(following)
    return render(request,"user_account/following.html",context)