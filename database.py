from pymongo import MongoClient
from datetime import datetime
import bcrypt

import os

class Database:
    def __init__(self):
        self.db = MongoClient(os.getenv("MONGO_URI")).AnonBlogs
        self.pages = self.db.pages
    
    def get_page(self, name, password=None):
        if not password:
            return self.pages.find_one({'_id': name}) is not None
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