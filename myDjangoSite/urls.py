"""myDjangoSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from blog import views
urlpatterns = [
    path('admin', admin.site.urls),
    path('index', views.hello),
    path('login', views.login),
    path('faq', views.faq),
    path('write', views.write),
    path('myAccount', views.myAccount),
    path('register', views.register),
    path('login.do', views.login_do),
    path('logout.do', views.logout_do),
    path('follow', views.follow),
    path('unfollow', views.unfollow),
    path('getArticlesOnPageNo', views.getArticlesOnPageNo),
    path('getFollOnPageNo', views.getFollOnPageNo),
    path('updateAdditionalInfo', views.updateAdditionalInfo),
    path('updatePwd', views.updatePwd),
    path('upload_img', views.upload_img),
    path('upload_img_data', views.upload_img_data),
    path('like',views.like),
    path('comment',views.comment),
    path('editComment', views.editComment),
    path('deleteComment', views.deleteComment),
    path('reportArticle', views.reportArticle),
    path('deleteArticle', views.deleteArticle),
    path('submitArticle', views.submit_article),
    path('', views.hello),
    re_path(r'^user/.*$',views.user_profile),
    re_path(r'^.*$',views.article)
]
