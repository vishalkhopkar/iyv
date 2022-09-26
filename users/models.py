from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.
from .managers import CustomUserManager


class CustomUser(AbstractUser):

    username = None
    last_name = None
    #id = models.AutoField()
    email = models.EmailField(_('email address'), unique=True)
    profilePic = models.BooleanField(default=False)
    profilePicFileName = models.CharField(max_length=30, unique=False)
    user_slug = models.CharField(max_length=30, default="sample-slug")
    followers = models.ManyToManyField("self", through="Follower", symmetrical=False)
    isBanned = models.BooleanField(default=False)
    banDaysLeft = models.IntegerField(default=0)
    followerCnt = models.IntegerField(default=0)
    followingCnt = models.IntegerField(default=0)
    articleCnt = models.IntegerField(default=0)

    about = models.TextField(default=None, null=True, blank=True)
    facebook_url = models.CharField(max_length=100, default=None, null=True, blank=True)
    twitter_url = models.CharField(max_length=40, default=None, null=True, blank=True)
    linkedin_url = models.CharField(max_length=100, default=None, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def getAllFields(self):
        myDict = {}
        myDict["id"] = self.id
        myDict["email"] = self.email
        myDict["user_slug"] = self.user_slug
        myDict["followerCnt"] = self.followerCnt
        myDict["followingCnt"] = self.followingCnt


        return myDict

    def __str__(self):
        return self.email


class Follower(models.Model):

    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="to_user")

    class Meta:
        unique_together = ["from_user", "to_user"]