import pymongo
import pprint
from pymongo import MongoClient
from flask import Flask, jsonify
from bson.objectid import ObjectId
from routes import api_routes

client = MongoClient()
db = client.test
collection = db.test_collection
posts = db.posts
app = Flask(__name__)

api_routes(app)

@app.route('/')
def index():
    found_posts = posts.find_one()
    all_posts = {}
    for post in posts.find():
        all_posts = post
    return 'Index Page %s' % post
    # return 'Index'
    # 58e93bfee75ab54869e8967c

@app.route('/hello')
def hello():
    return 'Hello, World'
