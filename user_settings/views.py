from django.shortcuts import render,redirect
from .models import Settings
from .forms import SettingsForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login")
def settings(request):
    setting_exists = ""
    #checks if the user has a settings model and save it an as instance to updat eon the frontend
    if Settings.objects.filter(user = request.user).exists():
        setting = Settings.objects.get(user = request.user)
        form = SettingsForm(instance = setting)
        setting_exists = True
    else:
        form = SettingsForm()
    
    if request.method == "POST":
        if setting_exists:
            posted_form = SettingsForm(request.POST,instance = setting)
        else:
            posted_form = SettingsForm(request.POST)
        dummy = posted_form.save(commit = False)
        dummy.user = request.user
        dummy.save()
        return redirect("settings")
  
    context = {
        "form":form
    }
    return render(request,"user_settings/settings.html",context)