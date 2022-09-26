from ..models import Article
from users.models import CustomUser, Follower
from users.managers import CustomUserManager
from datetime import datetime
from django.contrib.auth import authenticate


class UserModel:
    def addUser(self, emailId, name, password):
        try:
            userFound = CustomUser.objects.filter(email = emailId)
            if userFound:
                return False
            #create a username
            name_to_be_searched=name.strip().lower().replace(" ","-")
            existing_users_with_this_name_count = CustomUser.objects.filter(user_slug__startswith = name_to_be_searched).count()
            user_slug = name_to_be_searched+"-"+str(existing_users_with_this_name_count + 1)
            user = CustomUser.objects.create_user(email=emailId, first_name=name, user_slug=user_slug, password=password)

            #return user.getAllFields()
            return user
        except Exception as e:
            print(e)
            return False

    def validatePasswords(self, password, confirm_password):
        return True
        #TODO

    def getUserBySlug(self, userSlug):
        try:
            userFound = CustomUser.objects.filter(user_slug = userSlug)[0]
            print("USER ", userFound)
            if userFound:
                print("USER FOUND")
                return userFound
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def getArticles(self, user_id, start, limit):
        try:
            #last number in the user slug is the author id
            print("START ",start,limit)
            articles = Article.objects.filter(author__id = user_id)[start:limit]
            #articles = User.objects.filter(article__)
            articles_cnt = articles.count()
            print(articles, articles_cnt)
            return articles
        except Exception as e:
            return False

    def getArticlesCount(self, user):
        try:
            #last number in the user slug is the author id

            articles_cnt = Article.objects.filter(author__email = user.email).count()

            #print(articles, articles_cnt)
            return articles_cnt
        except Exception as e:
            return False

    def getFollowers(self, user_id, start, limit):
        try:
            followers = Follower.objects.filter(to_user__id = user_id)[start:limit]
            print("FOLLOWERS ",followers)
            return followers
        except Exception as e:
            print(e)
            return False
        #TODO
        return None

    def getFollowing(self, user_id, start, limit):
        try:
            followers = Follower.objects.filter(from_user__id = user_id)[start:limit]
            print("FOLLOWING ",followers)
            return followers
        except Exception as e:
            print(e)
            return False
        #TODO
        return None

    def follow(self, user, whomToFollow):
        #both user and whomToFollow are ids
        print("Follow")
        try:

            source = CustomUser.objects.filter(id = user)[0]
            prevFollowingCnt = source.followingCnt
            dest = CustomUser.objects.filter(id = whomToFollow)[0]
            prevFollowerCnt = dest.followerCnt
            print(user, dest)

            follower = Follower(from_user = source, to_user = dest)

            follower.save()

            #update follow count
            CustomUser.objects.filter(id=whomToFollow).update(followerCnt = prevFollowerCnt + 1)
            CustomUser.objects.filter(id=user).update(followingCnt = prevFollowingCnt + 1)
            return True
        except Exception as e:
            print(e)
            return False

    def unfollow(self, user, whomToFollow):
        #here whomToFollow is actually whom to unfollow (id)
        try:

            follower_obj = Follower.objects.filter(from_user__id = user, to_user__id = whomToFollow)[0]

            if follower_obj:
                prevFollowingCnt = follower_obj.from_user.followingCnt
                prevFollowerCnt = follower_obj.to_user.followerCnt
                print(follower_obj)
                CustomUser.objects.filter(id=follower_obj.from_user.id).update(followingCnt = prevFollowingCnt - 1)
                CustomUser.objects.filter(id=follower_obj.to_user.id).update(followerCnt = prevFollowerCnt - 1)
                follower_obj.delete()

                #update follow cnt

                return True
            return False
        except Exception as e:
            print(e)
            return False

    def doesUserFollow(self, source, dest):
        print("DOES USER FOLLOW ", source, dest)
        try:

            res = Follower.objects.filter(from_user__id = source, to_user__id = dest).count()
            if res > 0:
                return True
            print("No entry found")
            return None
        except Exception as e:
            print(e)
            return None

    def getFollowerCnt(self, user_id):
        try:
            res = Follower.objects.filter(to_user__id = user_id).count()
            return res
        except Exception as e:
            print(e)
            return None

    def getFollowingCnt(self, user_id):
        try:
            res = Follower.objects.filter(from_user__id = user_id).count()
            return res
        except Exception as e:
            print(e)
            return None

    def serialiseFoll(self, foll, type):
        ret = []
        for entry in foll:
            temp = {}
            if type == 1:
                #following
                temp["id"] = entry.to_user.id
                temp["name"] = entry.to_user.first_name
                temp["slug"] = entry.to_user.user_slug
                temp["dp"] = entry.to_user.profilePic
                temp["followerCnt"] = entry.to_user.followerCnt
            else:
                #follower
                temp["id"] = entry.from_user.id
                temp["name"] = entry.from_user.first_name
                temp["slug"] = entry.from_user.user_slug
                temp["dp"] = entry.from_user.profilePic
                temp["followerCnt"] = entry.from_user.followerCnt
            ret.append(temp)

        return ret

    def updateAdditionalInfo(self, user_id, request):
        #update about info of this user id
        aboutText = request.POST["about"]
        facebookUrl = request.POST["facebookUrl"]
        linkedinUrl = request.POST["linkedinUrl"]
        twitterUrl = request.POST["twitterUrl"]
        try:
            CustomUser.objects.filter(id = user_id).update(
                about = aboutText, facebook_url = facebookUrl,
                linkedin_url = linkedinUrl, twitter_url = twitterUrl
            )
            return True
        except Exception as e:
            print(e)
            return False

    def changePwd(self, user_id, email, request):
        currentPwd = request.POST["currentPwd"]
        newPwd = request.POST["newPwd"]
        confirmNewPwd = request.POST["confirmNewPwd"]
        if newPwd != confirmNewPwd:
            return False
        auth = authenticate(username=email, password=currentPwd)
        if auth:
            print("authenticated")

            try:
                user = CustomUser.objects.get(id=user_id)
                user.set_password(newPwd)
                user.save()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    def updateDpStatus(self, user_id, dpFileName):
        try:
            CustomUser.objects.filter(id = user_id).update(profilePic = True, profilePicFileName = dpFileName)
            return True
        except Exception as e:
            print(e)
            return False

