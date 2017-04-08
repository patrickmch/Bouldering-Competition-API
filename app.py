import pymongo
import pprint
from pymongo import MongoClient
from flask import Flask, jsonify
from bson.objectid import ObjectId


client = MongoClient()
db = client.test
collection = db.test_collection
posts = db.posts
app = Flask(__name__)



@app.route('/')
def index():
    found_posts = posts.find_one()
    for key, value in found_posts.iteritems():
        if key == "_id":
            return "Test '{0}' : '{1}'".format(key, ObjectId(value))
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'
