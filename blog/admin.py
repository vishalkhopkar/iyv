from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Article,  Tag, Like, Comment
from users.models import CustomUser, Follower
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Follower)
admin.site.register(Article)
admin.site.register(Like)
admin.site.register(Comment)
#admin.site.register(MyUser)
#admin.site.register(CustomUser, UserAdmin)
