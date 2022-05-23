from django.forms import ModelForm
from .models import Settings

class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = "__all__"
        exclude = ['user']