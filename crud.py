from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

import pymongo
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

from participant import jerry

client = MongoClient()
db = client.test
collection = db.test_collection
posts = db.posts


def get_info(id):
    info = posts.find_one(ObjectId(id))
    return 'Here is info: %s' % info

def heres_jerry():
    return 'Here\'s Jerry: %s' % jerry.name
