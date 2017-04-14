# boilerplate
from flask import Flask, jsonify, abort, make_response, request, url_for
import bson
import pymongo
from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import pprint
import json
import inspect
import ast
from datetime import datetime

# database and colllection setup
client = MongoClient()
db = client.test
# collection = db.test_collection
# posts = db.posts
participants = db.participants
venues = db.venues
competitions = db.competitions

# function to validate collection fields

def collection_validation(collection_name, validation_dict, validation_level):
    # convert python dict to sorted dict type using bson's SON method: first item in the list is the command we want to use with the collection name; next is the validation dictionary; next is the validation level
    validator = bson.son.SON([("collMod", collection_name),
    ("validator", validation_dict),
    ("validationLevel", validation_level)])
    # pass sorted dict to Mongo's command method
    db.command(validator)
    print    "Validation Successful"

# validation dictionaries
participants_validation = {
    "$and" :
    [
        {"fname" : {"$type" : "string"}},
        {"lname" : {"$type" : "string"}},
        {"birthday" : {"$type" : "string"}},
        {"sex" : {"$in" : ["m", "f"]}},
        {"email" : {"$regex": "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"}},
    ]
}

venue_validation = {
    "$and" :
    [
        {"venue_name": {"$type" : "string"}},
        {"venue_address" : {"$type" : "string"}}
    ]
}

competition_validation = {
    "$and" :
    [
        {"comp_name" : {"$type" : "string"}},
        {"venue_id" : {"$type" : "array"}},
    ]
}
# collection_validation("participants", participants_validation, "strict")
