import os
from io import BytesIO
from PIL import Image
import requests
import binascii
import string
import random
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from .Model import DbModel
from .Model import SubmitArticleModel
from .Model import UserModel, ArticleModel

from .forms import RegisterForm, LoginForm
# Create your views here.


def hello(request):
    db = DbModel.DbModel()
    arm = ArticleModel.ArticleModel()
    latest_posts = arm.get_latest_articles()

    print("curr session", request.session.get("username", ""))

    register_form = RegisterForm()
    login_form = LoginForm()
    return render(request, "index.html",
                  {"posts": latest_posts,
                   "session_username":request.session.get("username", None),
                   "register_form":register_form,
                   "login_form": login_form})

def faq(request):
    register_form = RegisterForm()
    login_form = LoginForm()
    return render(request, "faq.html",
                  {"session_username":request.session.get("username", None),
                   "register_form": register_form,
                   "login_form": login_form})

def write(request):

    print(request.session)
    if "username" not in request.session:
        print("username is null")
        response = HttpResponseRedirect("/")
        return response
    else:
        return render(request, "write.html", {"session_username": request.session.get("username", None)})

def article(request):
    #request.path_info contains actual URL suffix
    #print(request.path_info)
    postName = request.path_info[1:]
    arm = ArticleModel.ArticleModel()

    post = arm.get_article(postName)
    comments = arm.get_comments(post)
    #print(comments)
    # this variable is -1 if disliked, 0 if none, 1 if liked
    hasThisUserLiked = 0
    if "username" in request.session:
        hasThisUserLiked = arm.hasUserLiked(post, request.session["user_id"])
    references = arm.convertReferencesToArray(post.references)
    #print("HAS THIS USER LIKED ",hasThisUserLiked)
    register_form = RegisterForm()
    login_form = LoginForm()
    tags = post.tags.names()
    for tag in tags:
        print(tag)
    #print(post)
    if post:
        passed_title = post.title
        web_title = passed_title+" - It's Your View"
        return render(request, "article.html", {"title":passed_title,
                                                "web_title" : web_title,
                                                "name" : post.name,
                                                "post": post,
                                                "references": references,
                                                "tags": tags,
                                                "has_this_user_liked" : hasThisUserLiked,
                                                "content":post.content,
                                                "comments": comments,
                                                "session_username":request.session.get("username", None),
                                                "session_name":request.session.get("name", None),
                                                "session_user_slug": request.session.get("user-slug", None),
                                                "session_has_profile_pic": request.session.get("has_profile_pic", False),
                                                "session_profile_pic_name": request.session.get("profile_pic_name", None),
                                                "register_form": register_form,
                                                "login_form": login_form})
    else:
        return render(request, "article.html", {"title":"404 Not Found",  "content":None,
                                                "session_username":request.session.get("username", None),
                                                "register_form": register_form,
                                                "login_form": login_form})
def myAccount(request):
    user_slug = request.session["user-slug"]
    return HttpResponseRedirect("/user/"+user_slug)

def user_profile(request):
    print(request.path_info)
    user_slug = request.path_info[6:]
    print(user_slug)
    register_form = RegisterForm()
    login_form = LoginForm()
    usm = UserModel.UserModel()
    arm = ArticleModel.ArticleModel()
    user = usm.getUserBySlug(user_slug)
    hasDp = False
    if user:
        user_id = user.id
        articles_cnt = user.articleCnt
        hasDp = user.profilePic
    else:
        articles_cnt = 0
    if articles_cnt == 0:
        articles = None
    else:
        articles = usm.getArticles(user_id, 0, 5)
        articles = arm.humaniseDates(articles)


    doesSessionUserFollowThisPerson = None
    thisPersonFollowsSessionUser = None
    if "username" in request.session:
        doesSessionUserFollowThisPerson = usm.doesUserFollow(request.session["user_id"], user_id)
        thisPersonFollowsSessionUser = usm.doesUserFollow(user_id, request.session["user_id"])

    #print("SESSION",request.session["user-slug"], user_slug)
    print("DOES HE/SHE FOLLOW", doesSessionUserFollowThisPerson)
    print("DOES THIS PERSON FOLLOW YOU ", thisPersonFollowsSessionUser)

    # get follower and following count of the user
    followerCnt = user.followerCnt
    followingCnt = user.followingCnt
    about = user.about
    #split about into lines
    if about:
        split_about = about.split("\n")
    else:
        split_about = None

    facebook_url = user.facebook_url
    if facebook_url == "facebook_url":
        facebook_url = None
    twitter_url = user.twitter_url
    if twitter_url == "twitter_url":
        twitter_url = None
    linkedin_url = user.linkedin_url
    if linkedin_url == "linkedin_url":
        linkedin_url = None
    print("FACEBOOK URL", facebook_url)
    # pass additional info

    if user:
        return render(request, "my_account.html",
                      {"session_username": request.session.get("username", None),
                       "session_user_slug": request.session.get("user-slug",None),
                       "session_user_id": request.session.get("user_id", -1),
                       "user_slug" : user_slug,
                       "user_dp": user.profilePicFileName,
                       "user_id": user_id,
                       "user_username" : user.email,
                       "web_title": user.first_name+" - It's Your View",
                       "articles": articles,
                       "articles_cnt": articles_cnt,
                       "does_logged_in_user_follow": doesSessionUserFollowThisPerson,
                       "this_person_follows_you": thisPersonFollowsSessionUser,
                       "follower_cnt": followerCnt,
                       "following_cnt": followingCnt,
                       "has_dp": hasDp,
                       "about": split_about,
                       "full_about": about,
                       "facebook_url": facebook_url,
                       "twitter_url": twitter_url,
                       "linkedin_url": linkedin_url,
                       "session_name": user.first_name,
                       "register_form": register_form,
                       "login_form": login_form
                       })

    return render(request, "article.html", {"title": "404 Not Found", "content": None,
                                            "session_username": request.session.get("username", None),
                                            "register_form": register_form,
                                            "login_form": login_form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            emailId = form.cleaned_data["lgn_emailId"]
            password = form.cleaned_data["lgn_password"]
            user = authenticate(username=emailId, password=password)
            if user:
                print("authenticated successfully")
                request.session["username"] = emailId
                request.session["user-slug"] = user.user_slug
                request.session["user_id"] = user.id
                request.session["name"] = user.first_name
                request.session["has_profile_pic"] = user.profilePic
                request.session["profile_pic_name"] = user.profilePicFileName
                print("USER SLUG",request.session["user-slug"])
                return JsonResponse({"result": "OK"}, status=200)

            #some problem
            print("SOME PROBLEM")
            return JsonResponse({"result": "NOK", "reason": "not_auth"}, status=200)
        #form is not valid
        return JsonResponse({"result": "NOK", "reason": "invalid_form"}, status=200)
    return JsonResponse({"result": "NOK", "reason": "invalid_method"}, status=403)
    #return render(request, "login.html", {"goTo": "/write"})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            emailId = form.cleaned_data["emailId"]
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            usm = UserModel.UserModel()
            result = usm.validatePasswords(password, confirm_password)
            if not result:
                #Passwords don't match
                return JsonResponse({"result": "NOK", "reason" : "passwords_dont_match"}, status=200)
            result = usm.addUser(emailId, name, password)
            #here result is the username
            print("RESULT ",result)
            if not result:
                #problems in adding user
                return JsonResponse({"result": "NOK", "reason" : "problem_in_user_creation"}, status=200)
            #everything ok
            request.session["username"] = emailId
            request.session["user-slug"] = result.user_slug
            request.session["user_id"] = result.id
            request.session["name"] = result.first_name
            request.session["has_profile_pic"] = result.profilePic
            request.session["profile_pic_name"] = result.profilePicFileName
            return JsonResponse({"result": "OK"}, status=200)
            #return HttpResponseRedirect(request.path_info)
        return JsonResponse({"result": "NOK", "reason": "invalid_form"}, status=200)
    return JsonResponse({"result": "NOK", "reason": "invalid_method"}, status=403)

def login_do(request):
    if request.is_ajax and request.method == "POST":
        print(request)
        db = DbModel.DbModel()
        data = request.POST.copy()
        username = request.POST["username"]
        password = request.POST["password"]


        userFound = db.get_user(username, password)
        print(userFound)
        if userFound:
            request.session["username"] = userFound["username"]
            return JsonResponse({"result" : "OK"}, status=200)

    return JsonResponse({"result": "NOK"}, status=200)

def logout_do(request):
    try:
        username = request.session["username"]
        print(username)
        del request.session["username"]
        del request.session["user-slug"]
        del request.session["user_id"]
        #return HttpResponseRedirect("/")
        return JsonResponse({"result": "OK"}, status=200)
    except Exception as e:
        return JsonResponse({"result": "NOK"}, status=200)

def upload_img(request):
    if request.method == "POST":
        try:            
            print(request.FILES["file"])
            username = request.session["user-slug"]
            print("USERNAME IS "+username)
            isDp = False
            if "type" in request.POST:
                isDp = request.POST["type"]
            if isDp:
                image_name = "dp_full.jpg"
            else:
                image_name = str(request.FILES["file"])
            path = handle_uploaded_img(request.FILES["file"], username, image_name)
            return JsonResponse({"location" : path}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({"result": "NOK"}, status=403)

#upload profile pic
def upload_img_data(request):
    if "user_id" not in request.session:
        return JsonResponse({"result": "NOK"}, status=403)
    if request.method == "POST":
        try:
            img_data = request.POST["image_data_url"]
            username = request.session["user-slug"]
            dpFileName = str(''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=5))) + ".jpg"
            img_loc = handle_image_data(img_data, username, dpFileName)
            if not img_loc:
                return JsonResponse({"result": "NOK"}, status=403)
            # dp uploaded successfully
            usm = UserModel.UserModel()

            res = usm.updateDpStatus(request.session["user_id"], dpFileName)
            if res:
                return JsonResponse({"location": img_loc, "result": "OK"}, status=200)
            else:
                return JsonResponse({"location": img_loc, "result": "NOK"}, status=200)
        except Exception as e:
            print(e)

def handle_image_data(img_data, username, dpFileName):
    try:
        binary_data = binascii.a2b_base64(img_data.split("base64,")[1])

        image_name = dpFileName
        cur_dir = os.getcwd()
        dir_name = cur_dir + "\\blog\\static\\img\\user\\" + username
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        img_path = dir_name+"\\"+image_name
        fd = open(img_path, 'wb')
        fd.write(binary_data)
        fd.close()
        return "static/img/user/" + username + "/" + image_name
    except Exception as e:
        print(e)
        return False



def handle_uploaded_img(img, username, image_name):

    cur_dir = os.getcwd()
    dir_name = cur_dir+"\\blog\\static\\img\\user\\"+username
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    ret = dir_name+"\\"+image_name
    with open(ret, 'wb+') as destination:
        for chunk in img.chunks():
            destination.write(chunk)
    return "static/img/user/"+username+"/"+image_name

def submit_article(request):
    if "user_id" not in request.session:
        return JsonResponse({"result": "NOK"}, status=403)
    if request.is_ajax and request.method == "POST":
        print(request)
        title = request.POST["title"]
        content = request.POST["content"]
        references = request.POST["references"]
        tags = request.POST["tags"]
        print(title, references)
        submit_mod = SubmitArticleModel.SubmitArticleModel()
        slug = submit_mod.get_slug(title)
        print(slug)
        user_id = request.session["user_id"]
        if(slug):
            ar = submit_mod.save_article(title, slug, content, references, tags, user_id)
            print(ar)
            if ar:
                #return JsonResponse({"result": "OK", "url":ar.name}, status=200)
                print("ARTICLE CREATED SUCCESFULLY")
                return JsonResponse({"result": "OK", "url": ar.name}, status=200)
                #return HttpResponseRedirect("/"+ar.name)
            else:
                return JsonResponse({"result": "NOK", "reason": "problem_in_upload"}, status=200)
        #already exists
        return JsonResponse({"result": "NOK", "reason" : "already_exists"}, status=200)
    return JsonResponse({"result": "NOK"}, status=403)


def follow(request):
    if request.is_ajax and request.method == "POST":
        whomToFollow = request.POST["whomToFollow"]
        #whomToFollow is a user id
        source = request.session["user_id"]
        #source is also a user id
        usm = UserModel.UserModel()
        if usm.follow(source, whomToFollow):
            return JsonResponse({"result": "OK"}, status=200)
        return JsonResponse({"result": "NOK", "reason": "could_not_follow"}, status=200)
    return JsonResponse({"result": "NOK"}, status=403)

def unfollow(request):
    if request.is_ajax and request.method == "POST":
        whomToFollow = request.POST["whomToFollow"]
        # whomToFollow is a user id
        source = request.session["user_id"]
        usm = UserModel.UserModel()
        if usm.unfollow(source, whomToFollow):
            return JsonResponse({"result": "OK"}, status=200)
        return JsonResponse({"result": "NOK", "reason": "could_not_follow"}, status=200)
    return JsonResponse({"result": "NOK"}, status=403)

def getArticlesOnPageNo(request):
    if request.is_ajax:
        user_id = request.GET["user_id"]
        pageNo = request.GET["pageNo"]
        print(user_id, pageNo)
        usm = UserModel.UserModel()

        arm = ArticleModel.ArticleModel()
        start = 5*(int(pageNo) - 1)
        end = 5*(int(pageNo))
        try:
            articles = usm.getArticles(user_id, start, end)
            articles_arr = arm.serialiseArticles(articles)
            return JsonResponse({"result": "OK", "articles":articles_arr}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"result": "NOK"}, status=200)
    return JsonResponse({"result": "NOK"}, status=403)

def getFollOnPageNo(request):
    if request.is_ajax:
        user_id = request.GET["user_id"]
        pageNo = request.GET["pageNo"]

        usm = UserModel.UserModel()
        start = 3 * (int(pageNo) - 1)
        end = 3 * (int(pageNo))
        foll_arr = []
        try:
            type = int(request.GET["type"])
            if type == 2:
                #retrieve followers
                print("getting followers")
                followers = usm.getFollowers(user_id, start, end)
                foll_arr = usm.serialiseFoll(followers, 2)
                print(foll_arr)
            else:
                #retrieve following
                following = usm.getFollowing(user_id, start, end)
                foll_arr = usm.serialiseFoll(following, 1)
                print(foll_arr)
            return JsonResponse({"result": "OK", "foll": foll_arr}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"result": "NOK"}, status=200)


    return JsonResponse({"result": "NOK"}, status=403)


def updateAdditionalInfo(request):
    if request.is_ajax:
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            try:
                usm = UserModel.UserModel()
                result = usm.updateAdditionalInfo(user_id, request)
                if result:
                    return JsonResponse({"result": "OK"}, status=200)
                else:
                    return JsonResponse({"result": "NOK", "reason": "unable_to_update"}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({"result": "NOK"}, status=200)
        else:
            return JsonResponse({"result": "NOK"}, status=403)
    return JsonResponse({"result": "NOK"}, status=403)

def updatePwd(request):
    if request.is_ajax:
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            email = request.session["username"]
            try:
                usm = UserModel.UserModel()
                result = usm.changePwd(user_id, email, request)
                if result:
                    return JsonResponse({"result": "OK"}, status=200)
                return JsonResponse({"result": "NOK", "reason": "unable_to_update"}, status=403)
            except Exception as e:
                print(e)
                return JsonResponse({"result": "NOK", "reason": "unable_to_update"}, status=403)
        else:
            return JsonResponse({"result": "NOK"}, status=403)
    return JsonResponse({"result": "NOK"}, status=403)

def like(request):
    if request.is_ajax:
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            postId = request.POST["postId"]
            type = request.POST["type"]
            arm = ArticleModel.ArticleModel()
            result = arm.likePost(user_id, postId, type)
            if result:
                return JsonResponse({"result": "OK"}, status=200)
            return JsonResponse({"result": "NOK"}, status=403)
        return JsonResponse({"result": "NOK"}, status=403)
    return JsonResponse({"result": "NOK"}, status=403)

def comment(request):
    if request.is_ajax:
        if "user_id" in request.session:
            # can comment
            user_id = request.session["user_id"]
            postId = request.POST["postId"]
            text = request.POST["comment"]
            if len(text) > 500:
                return JsonResponse({"result": "NOK", "reason" : "comment_too_long"}, status=200)
            arm = ArticleModel.ArticleModel()
            result = arm.comment(user_id, postId, text)
            if result:
                return JsonResponse({"result": "OK", "id": result}, status=200)
            return JsonResponse({"result": "NOK"}, status=403)
        return JsonResponse({"result": "NOK"}, status=403)
    return JsonResponse({"result": "NOK"}, status=403)

def editComment(request):
    if request.is_ajax:
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            commentId = request.POST["id"]
            text = request.POST["comment"]
            if len(text) > 500:
                return JsonResponse({"result": "NOK", "reason": "comment_too_long"}, status=200)
            arm = ArticleModel.ArticleModel()
            result = arm.editComment(user_id, commentId, text)
            if result:
                return JsonResponse({"result": "OK"}, status=200)
            return JsonResponse({"result": "NOK", "reason": "problem_updating_comment"}, status=403)
        return JsonResponse({"result": "NOK"}, status=403)
    return JsonResponse({"result": "NOK"}, status=403)

def deleteComment(request):
    if request.is_ajax:
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            commentId = request.POST["id"]
            arm = ArticleModel.ArticleModel()
            result = arm.deleteComment(user_id, commentId)
            if result:
                return JsonResponse({"result": "OK"}, status=200)
            return JsonResponse({"result": "NOK", "reason": "problem_updating_comment"}, status=403)
        return JsonResponse({"result": "NOK"}, status=403)
    return JsonResponse({"result": "NOK"}, status=403)

def reportArticle(request):
    if request.is_ajax:
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            postId = request.POST["articleId"]
            reasons = request.POST["reasons"]
            comment = request.POST["comment"]
            arm = ArticleModel.ArticleModel()
            result = arm.reportArticle(user_id, postId, reasons, comment)
            if result:
                return JsonResponse({"result": "OK"}, status=200)
            return JsonResponse({"result": "NOK", "reason": "problem_updating_comment"}, status=403)
        return JsonResponse({"result": "NOK"}, status=403)
    return JsonResponse({"result": "NOK"}, status=403)

def deleteArticle(request):
    if request.is_ajax:
        if "user_id" in request.session:
            user_id = request.session["user_id"]
            postId = request.POST["articleId"]

            arm = ArticleModel.ArticleModel()
            result = arm.deleteArticle(user_id, postId)
            if result:
                return JsonResponse({"result": "OK"}, status=200)
            return JsonResponse({"result": "NOK", "reason": "problem_deleting_article"}, status=403)
        return JsonResponse({"result": "NOK"}, status=403)
    return JsonResponse({"result": "NOK"}, status=403)