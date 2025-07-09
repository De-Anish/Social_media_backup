from django.contrib import admin
from .models import Tweet, Follower, UserProfile

admin.site.register(Tweet)
admin.site.register(Follower)
admin.site.register(UserProfile)
