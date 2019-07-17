from django.contrib import admin
from .models import user_details

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'mail_sent_time', 'status')
    
admin.site.register(user_details, UserAdmin)