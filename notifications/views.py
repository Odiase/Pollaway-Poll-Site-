from linecache import cache
from django.conf import settings
from django.shortcuts import render,redirect
from .models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page
# from django.core.cache import cache

from polls.models import Featured_Polls,Poll

#CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.
# @cache_page(CACHE_TTL)
@login_required(login_url="login")
def notifications(request):
    
    # checking for expired polls and notifying the user
    def check_expired_polls(queryset):
        for poll in queryset:
            if poll.is_expired():
                message = f"Your Poll '{poll.title}' Was Closed at {poll.expire.date()}"
                # send a notification to all the users that participated in the poll 
                if Notification.objects.filter(user = poll.user, message = message).exists():
                    pass
                else:
                    notification = Notification.objects.create(user = poll.user, message = message, read = False)
                    notification.save()

                for i in Featured_Polls.objects.filter(polls= poll):
                    message = f"The Poll '{poll.title}' Was Closed at {poll.expire.date()}"
                    if Notification.objects.filter(user = i.user, message = message).exists():
                        pass
                    else:
                        notification = Notification.objects.create(user = i.user,read = False,message = message)
                        notification.save()
    try:
        user_polls = Poll.objects.filter(user = request.user)
        user_featured_polls = Featured_Polls.objects.get(user = request.user).polls.all()
        check_expired_polls(user_polls)
        check_expired_polls(user_featured_polls)
    except:
        user_polls = ""
        user_featured_polls = ""

    user_notifications = Notification.objects.filter(user = request.user, deleted = False)
    context = {
        "all_notifications":user_notifications,
        "length":len(user_notifications)
    }
    return render(request,"notifications/notifications.html",context)


@login_required(login_url="login")
def mark_notification_as_read(request,id):
    notification = Notification.objects.get(id = id)
    if notification.user != request.user:
        return redirect("login")

    #saves the notification as read
    if request.method == "POST":
        notification.read = True
        notification.save()
        return redirect("notifications")


@login_required(login_url="login")
def delete_notification(request,id):
    notification = Notification.objects.get(id = id)
    if notification.user != request.user:
        return redirect("login")

    if request.method == "POST":
        notification.delete()
        return redirect("notifications")


@login_required(login_url="login")
def mark_all_as_read(request):
    unread_notifications = Notification.objects.filter(user = request.user,read = False)
    for notification in unread_notifications:
        notification.read = True
        notification.save()
    return redirect("notifications")


@login_required(login_url="login")
def delete_all_read(request):
    read_notifications = Notification.objects.filter(user = request.user,read = True)
    for notification in read_notifications:
        notification.deleted = True
        notification.save()
    return redirect("notifications")