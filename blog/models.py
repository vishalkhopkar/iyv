from django.db import models
from taggit.managers import TaggableManager

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from users.models import CustomUser
import django.utils.timezone as tz
import datetime
# Create your models here.

class Tag(models.Model):
    #tags used in the article
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length = 50)
    used_in_articles_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ["-used_in_articles_cnt"]

class Article(models.Model):
    #id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 100)
    content = models.TextField()
    name = models.SlugField()
    date_time = models.DateTimeField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="author")
    comments = models.ManyToManyField(CustomUser, through = "Comment", related_name="article_comments")
    likes = models.ManyToManyField(CustomUser, through = "Like", related_name="article_likes")
    likesCnt = models.IntegerField(default=0)
    dislikesCnt = models.IntegerField(default=0)
    commentsCnt = models.IntegerField(default=0)
    references = models.TextField(blank=True)
    isPublished = models.BooleanField(default=True)
    #tags = models.ManyToManyField(Tag, through = "TagArticle", related_name="article_tags")
    tags = TaggableManager()
    isReported = models.BooleanField(default=False)
    reportReasons = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name
    def add_tag(self, tag):
        new_tag = TagArticle(article = self, tag = tag)
        new_tag.save()
        new_tag.tag.used_in_article_cnt += 1
    class Meta:
        get_latest_by = ["-date_time"]
        ordering = ["-date_time","-likesCnt"]

class TagArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="tagarticle_article")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tagarticle_tag")


class Comment(models.Model):
    #user-article many to many relationship
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comment_user")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment_article")
    comment_text = models.CharField(max_length=500)

    date_time = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ["date_time"]

# this model is applicable for like or dislike
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="like_user")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="like_article")
    type = models.BooleanField(default=True)
    class Meta:
        unique_together = ["user", "article"]









