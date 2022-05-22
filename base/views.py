from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from user_settings.models import Settings
from user_account.models import Followers
from notifications.models import Notification

# Create your views here.
def home_page(request):
    return render(request,"base/homepage.html")

def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        '''Verifying the user's  submitted details with other user instances to check if any of the user's details already exists.'''
        if User.objects.filter(username = username).exists():
            messages.info(request,"Sorry This Username Has Been Taken") 
        if password1 == " " or password1 == "":
            messages.info(request,"Pls Enter A Valid Password")
            return redirect('sign-up')
        if password1 != password2:
            messages.info(request,"Your Passwords Do Not Match")
            return redirect('sign-up')
            
        if email == "":
            messages.info(request,"Pls Enter An Email")
            return redirect('sign-up')
        else:
            if User.objects.filter(email = email).exists():
                messages.info(request,"Sorry This Email Already Exist!")
                return redirect('sign-up')
        
        '''Create an account for the user from the user model, also create a setting and followers instance with the user, then send the user a welsome notification'''
        user = User.objects.create_user(username = username, password = password1, email = email)
        user.save()
        Notification.objects.create(user  = user, message = f"Hi There {user.username}, Welcome To Pollaway")
        Settings.objects.create(user = user)
        Followers.objects.create(user = user)

        # sending welcome email to the new user
        subject = "<h1>Welcome To POLLAWAY</h1>"
        message = f""" <p>Hi There {username}, we are pleased to have you on pollaway,
We do hope you have a nice time on the pollaway site and make use of this platform the fullest.
and feel free to report any problems on our "Report A bug" Page.
we are happy to have you once again visit your profile page using this link <a href= "">Here</a> </p>

<h4>POLLAWAY</h4>
"""
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject,message,from_email,recipient_list,fail_silently=False)
    
        login(request,user)
        # CHECKING THE URL TO SEE IF THIS REDIRECTS THE USER TO ANOTHER PAGE
        if request.GET.get("next") != None:
            return redirect(request.GET.get("next"))
        else:
           return redirect('polls')

    return render(request,"base/sign-up.html")

def Login(request):
    if request.user.is_authenticated:
        return redirect("polls")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            if request.GET.get("next") != None:
                return redirect(request.GET.get("next"))
            else:
                return redirect('polls')    
        else:
            messages.info(request,'Invalid Credentials')
    return render(request,'base/login.html')

def Logout(request):
    logout(request)
    return redirect('home')