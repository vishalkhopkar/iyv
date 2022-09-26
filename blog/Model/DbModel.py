from pymongo import MongoClient


class DbModel:
    def __init__(self):
        self.conn = MongoClient()
        self.db = self.conn["vishal"]

    def get_article(self, name):
        collection = self.db["posts"]
        query = {"name": name}
        try:
            postFound = collection.find_one(query)
            if postFound:
                return postFound
            else:
                return False
        except:
            print("Error in retrieving")
            return False

    def get_latest_articles(self):
        collection = self.db["posts"]
        try:
            articles = collection.find().sort("date", -1).limit(5)
            if articles:
                return articles
            else:
                return False
        except:
            print("Articles retrieval error")
            return False
    def get_user(self, username, password):
        collection = self.db["users"]
        query = {"username" : username, "password" : password}
        try:
            userFound = collection.find_one(query)
            if userFound:
                return userFound
            return False
        except:
            return False
