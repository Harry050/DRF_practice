from django.contrib import admin
from .models import Process, Process_Thread, Process_Sub_Thread, UserProfile
# Register your models here.

admin.site.register(Process)
admin.site.register(Process_Thread)
admin.site.register(Process_Sub_Thread)
admin.site.register(UserProfile)
