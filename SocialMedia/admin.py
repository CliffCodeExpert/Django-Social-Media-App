from django.contrib import admin
from .models import Profile, Post, LikePost

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at')
    list_filter = ('user',)
  
admin.site.register(LikePost)


