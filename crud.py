from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
import bson
import pymongo
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
from participant import Participant

client = MongoClient()
db = client.test
collection = db.test_collection
posts = db.posts


validator = bson.son.SON([("collMod", "posts"),
("validator", {"$or": [{"phone": {"$exists": True}},
{"email": {"$exists": True}}]} ),
("validationLevel", "strict")])

db.command(validator)

def get_info(id):
    info = posts.find_one(ObjectId(id))
    return 'Here is info: %s' % info

def create_participant():
    new_participant = request.get_json()
    try:
        new_id = posts.insert_one(new_participant).inserted_id
    except pymongo.errors.WriteError as error:
        #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
        logging.error(error)
        return "Failed to create a participant as one or more required fields were missing or incomplete"
    else:
        return str(new_id)
