#setup functions, validation, and boilerplate
from flask import Flask, jsonify, abort, make_response, request, url_for
import bson
import pymongo
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import pprint
import json


client = MongoClient()
db = client.test
collection = db.test_collection
posts = db.posts

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def collection_validation(collection_name, validation_dict, validation_level):
    validator = bson.son.SON([("collMod", collection_name),
    ("validator", validation_dict),
    ("validationLevel", validation_level)])

    db.command(validator)
    print    "Validation Successful"

participants_validation = {
    "$and" :
    [
        {"fname" : {"$type" : "string"}},
        {"lname" : {"$type" : "string"}},
        {"birthday" : {"$type" : "date"}},
        {"sex" : {"$in" : ["m", "f"]}},
        {"level" : {"$type" : "int"}}
    ]
}

collection_validation("posts", participants_validation, "strict")
