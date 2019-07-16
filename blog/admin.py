from django.contrib import admin
from .models import Post



admin.site.site_header = "Admin Dashboard"

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'published_date')
    list_filter = ('created_date', 'published_date',)
    search_fields = ('title' ,)
admin.site.register(Post, PostAdmin)