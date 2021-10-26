from django.contrib import admin
from .models import Followers, FriendRequest

# Register your models here.
admin.site.register(Followers)
admin.site.register(FriendRequest)