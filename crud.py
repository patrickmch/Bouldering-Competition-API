from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

import pymongo
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

from participant import Participant

client = MongoClient()
db = client.test
collection = db.test_collection
posts = db.posts


def get_info(id):
    info = posts.find_one(ObjectId(id))
    return 'Here is info: %s' % info

def create_participant():
    new_participant = request.get_json()
    new_id = posts.insert_one(new_participant).inserted_id
    return 'heelloo %s' % str(new_id)
    # return 'test'
