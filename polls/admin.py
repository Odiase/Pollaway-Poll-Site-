from django.contrib import admin
from .models import (Poll,Poll_Option,Poll_Vote,Featured_Polls)

# Register your models here.
admin.site.register(Poll)
admin.site.register(Poll_Option)
admin.site.register(Poll_Vote)
admin.site.register(Featured_Polls)