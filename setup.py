#setup functions, validation, and boilerplate
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
    # convert python dict to sorted dict type using bson's SON method: first item in the list is the command we want to use with the collection name; next is the validation dictionary; next is the validation level
    validator = bson.son.SON([("collMod", collection_name),
    ("validator", validation_dict),
    ("validationLevel", validation_level)])
    # pass sorted dict to Mongo's command method
    db.command(validator)
    print    "Validation Successful"

participants_validation = {
    "$and" :
    [
        {"fname" : {"$type" : "string"}},
        {"lname" : {"$type" : "string"}},
        {"birthday" : {"$type" : "string"}},
        {"sex" : {"$in" : ["m", "f"]}},
        {"level" : {"$type" : "int"}}
    ]
}

collection_validation("posts", participants_validation, "strict")
