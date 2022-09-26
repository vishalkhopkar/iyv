from ..models import Article, Like, Comment
from users.models import CustomUser
import humanize
import datetime as dt

class ArticleModel:
    def serialiseArticles(self, articles):
        ret = []
        for article in articles:
            temp = {}
            temp["title"] = article.title
            temp["name"] = article.name
            temp["date_time"] = article.date_time.strftime("%d %B %Y")
            print(temp["date_time"])
            ret.append(temp)
        return ret


    def humaniseDates(self, articles):
        for article in articles:
            article.date_time = article.date_time.strftime("%d %B %Y")
            #print(article.date_time)
        return articles

    def get_latest_articles(self):
        try:
            articles = Article.objects.filter()[0:5]

            print(articles)
            articles = self.humaniseDates(articles)
            return articles
        except Exception as e:
            print(e)
            return False

    def get_article(self, article_name):
        try:
            ar = Article.objects.filter(name = article_name)[0]
            if ar:
                #exists
                print(ar.title, ar.author.first_name)
                return ar
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def likePost(self, userId, postId, type):

        if int(type) == 1:
            print("liking")
            likeType = True
        elif int(type) == -1:
            # dislike
            print("disliking")
            likeType = False
        else:
            # type is 0
            return self.removeLikeDislike(userId, postId)
        try:

            like, created_like = Like.objects.update_or_create(user_id = userId, article_id = postId,
                                                               defaults = {'type' : likeType})
            if created_like:
                # new like or dislike is created
                if likeType:
                    # new like is created
                    prevLikesCnt = Article.objects.filter(id=postId)[0].likesCnt
                    newLikesCnt = prevLikesCnt + 1
                    Article.objects.filter(id=postId).update(likesCnt=newLikesCnt)
                else:
                    # new dislike is created
                    prevDislikesCnt = Article.objects.filter(id=postId)[0].dislikesCnt
                    newDislikesCnt = prevDislikesCnt + 1
                    Article.objects.filter(id=postId).update(dislikesCnt=newDislikesCnt)
            elif like:
                # like or dislike is updated
                if likeType:
                    # first disliked, now liked
                    prevLikesCnt = Article.objects.filter(id=postId)[0].likesCnt
                    prevDislikesCnt = Article.objects.filter(id=postId)[0].dislikesCnt
                    newLikesCnt = prevLikesCnt + 1
                    newDislikesCnt = prevDislikesCnt - 1
                    Article.objects.filter(id=postId).update(likesCnt=newLikesCnt, dislikesCnt=newDislikesCnt)
                else:
                    # first liked, now disliked
                    prevLikesCnt = Article.objects.filter(id=postId)[0].likesCnt
                    prevDislikesCnt = Article.objects.filter(id=postId)[0].dislikesCnt
                    newLikesCnt = prevLikesCnt - 1
                    newDislikesCnt = prevDislikesCnt + 1
                    Article.objects.filter(id=postId).update(likesCnt=newLikesCnt, dislikesCnt=newDislikesCnt)
            else:
                print("UNUSUAL CASE")
                return False
            return True
        except Exception as e:
            print(e)
            return False

    def removeLikeDislike(self, userId, postId):
        try:
            # get existing like type
            like = Like.objects.filter(user_id = userId, article_id = postId)[0]
            if not like:
                print("UNUSUAL CASE FOR UNLIKING OR UN-DISLIKING")
                return False

            # normal case, like/dislike found
            likeType = like.type
            # remove the like object
            like.delete()
            if likeType:
                # first liked, now un-liked
                prevLikesCnt = Article.objects.filter(id=postId)[0].likesCnt
                newLikesCnt = prevLikesCnt - 1
                Article.objects.filter(id=postId).update(likesCnt=newLikesCnt)
            else:
                # first disliked, now un-disliked
                prevDislikesCnt = Article.objects.filter(id=postId)[0].dislikesCnt
                newDislikesCnt = prevDislikesCnt - 1
                Article.objects.filter(id=postId).update(dislikesCnt=newDislikesCnt)
            return True
        except Exception as e:
            print(e)
            return False


    def hasUserLiked(self, post, userId):
        try:
            res = Like.objects.filter(article_id = post.id, user_id = userId)
            if res.count() > 0:
                if res[0].type:
                    #liked
                    return 1
                else:
                    # disliked
                    return -1
            # none
            return 0
        except Exception as e:
            print("hasUserLiked exception ",e)
            return 0

    def comment(self, userId, postId, text):
        try:
            comment = Comment(user_id = userId, article_id = postId, comment_text = text)
            comment.save()
            # get previous comments count
            prevCmtsCount = Article.objects.filter(id = postId)[0].commentsCnt
            Article.objects.filter(id = postId).update(commentsCnt = prevCmtsCount + 1)
            return comment.id
        except Exception as e:
            print("[comment] Exception: ",e)
            return False

    def editComment(self, userId, commentId, text):
        try:
            comment_author_id = Comment.objects.filter(id=commentId)[0].user_id
            if userId != int(comment_author_id):
                print("Cannot edit someone else's comment")
                return False
            Comment.objects.filter(id=commentId).update(comment_text = text)
            return True
        except Exception as e:
            print("[editComment] Exception ",e)
            return False


    def deleteComment(userId, commentId):
        try:
            comment = Comment.objects.filter(id=commentId)[0]
            comment_author_id = comment.user_id
            comment_post_id = comment.article_id
            print("COMMENT POST ID ",comment_post_id)
            if userId != int(comment_author_id):
                print("Cannot edit someone else's comment")
                return False
            comment.delete()
            prevCommentsCnt = Article.objects.filter(id=comment_post_id)[0].commentsCnt
            Article.objects.filter(id=comment_post_id).update(commentsCnt=prevCommentsCnt - 1)
            return True
        except Exception as e:
            print("[deleteComment] Exception ",e)
            return False



    def get_comments(self, post):
        try:
            comments = Comment.objects.filter(article_id = post.id)
            return comments
        except Exception as e:
            print("get_comments Exception ",e)
            return None

    def reportArticle(self, userId, postId, reasons, comment):
        try:
            Article.objects.filter(id=postId).update(isReported = True, reportReasons = reasons)
            return True
        except Exception as e:
            print("[reportArticle] Exception ", e)
            return None

    def deleteArticle(self, userId, postId):
        try:
            article = Article.objects.filter(id = postId)[0]
            article_author_id = article.author_id
            print("ARTICLE AUTHOR ID", article_author_id, "USER ID", userId)
            if article_author_id != userId:
                print("Cannot delete someone else's article")
                return False
            # same owner
            article.delete()
            return True
        except Exception as e:
            print("[deleteArticle] Exception ",e)
            return False

    def convertReferencesToArray(self, references):
        # here references is a string
        len_refs = len(references)
        # strip the []
        references = references[1: len_refs - 1]

        splitRef = references.split(",")
        ret = []
        for ref in splitRef:
            len_ref = len(ref)
            # strip the ""
            isLink = False
            ref = ref[1: len_ref - 1]
            if ref.startswith("http"):
                isLink = True

            ret.append({
                "name": ref,
                "isLink": isLink
            })
        print(ret)
        return ret