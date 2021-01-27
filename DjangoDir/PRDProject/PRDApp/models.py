from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Process(models.Model):
    process_name = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.process_name

class Process_Thread(models.Model):
    process_thread_name = models.CharField(max_length=100, null=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    def __str__(self):
        return self.process_thread_name

class Process_Sub_Thread(models.Model):
    process_sub_thread_name = models.CharField(max_length=100, null=False)
    process_thread = models.ForeignKey(Process_Thread, on_delete=models.CASCADE)
    def __str__(self):
        return self.process_sub_thread_name

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='tracks', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user_process = models.ForeignKey(Process, on_delete=models.CASCADE)
    user_process_thread =  models.ForeignKey(Process_Thread, on_delete=models.CASCADE)
    user_process_sub_thread = models.ManyToManyField(Process_Sub_Thread)

    
    def special_return(self):
        return self.user_process, self.user_process_thread.process_thread_name
        #, self.user_process_thread.process_thread_name, self.user_process_sub_thread.process_sub_thread_name

    def __str__(self):
        template = '{0.user.username} {0.date_created} {0.user_process.process_name} {0.user_process_thread.process_thread_name} {0.comment}'
        return " %s  %s " % (template.format(self), ", ".join(topping.process_sub_thread_name for topping in self.user_process_sub_thread.all()))
        
        #return template.format(self)
        #return self.comment


