from ..models import Article
from users.models import CustomUser
from slugify import slugify
import datetime

class SubmitArticleModel:
    def get_slug(self, title):
        slug = slugify(title)
        existing_article = Article.objects.filter(name=slug)
        print(existing_article)
        if existing_article:
            return False

        #no article with such a title exists
        return slug

    def save_article(self, title, slug, content, references, tags, user_id):
        #tagify tags
        tagsArr = tags.split(",")
        print(tagsArr)
        try:
            time = datetime.datetime.now()
            ar = Article(title = title, name = slug, content = content, date_time = time,
                         author_id = user_id, likesCnt = 0, dislikesCnt = 0, commentsCnt = 0,
                         references = references)

            ar.save()
            for tag in tagsArr:
                ar.tags.add(tag)
            user = CustomUser.objects.filter(id = user_id)[0]
            print("AUTHOR FOR COUNT UPDATE ",user)
            prevArticleCnt = user.articleCnt
            print("prev article count ",prevArticleCnt)
            CustomUser.objects.filter(id = user_id).update(articleCnt = prevArticleCnt + 1)
            return ar
        except Exception as e:
            print(e)
            return False

