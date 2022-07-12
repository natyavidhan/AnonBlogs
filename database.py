from pymongo import MongoClient
from datetime import datetime
import bcrypt

import os
import random

class Database:
    def __init__(self):
        self.db = MongoClient(os.getenv("MONGO_URI")).AnonBlogs
        self.pages = self.db.pages
    
    def get_page(self, name, password=None):
        if not password:
            return self.pages.find_one({'_id': name})
        page = self.pages.find_one({'_id': name})
        if page:
            if bcrypt.checkpw(password.encode('utf-8'), page['password']):
                return page

    def new_page(self, name, password):
        if self.get_page(name):
            return False
        data = {
            "_id": name,
            'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
            'blogs': [],
            'created_on': datetime.now().strftime("%c")
        }
        self.pages.insert_one(data)
        return data
    
    def new_blog(self, name, blog):
        blog = {
            'id': "".join(random.choice("0123456789abcdefghijklmnopqrstuvwxyz") for i in range(5)),
            'title': blog['title'],
            'content': blog['content'],
            'created_on': datetime.now().strftime("%c")
        }
        self.pages.update_one({'_id': name}, {'$push': {'blogs': blog}})
        return blog

    def get_blogs(self, name):
        user = self.pages.find_one({'_id': name})
        if user:
            return user['blogs']