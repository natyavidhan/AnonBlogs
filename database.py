from pymongo import MongoClient
from datetime import datetime

import os

class Database:
    def __init__(self):
        self.db = MongoClient(os.getenv("MONGO_URI")).AnonBlogs
        self.pages = self.db.pages
    
    def get_page(self, name, password=None):
        if not password:
            return self.pages.find_one({'_id': name}) is not None
        return self.pages.find_one({'_id': name, 'password': password})

    def new_page(self, name, password):
        if self.get_page(name):
            return False
        data = {
            "_id": name,
            'password': password,
            'blogs': [],
            'created_on': datetime.now().strftime("%c")
        }
        self.pages.insert_one(data)
        return data