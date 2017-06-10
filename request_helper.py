from setup import *
from response_handler import ErrorResponse
from datetime import datetime
from flask import request
class RequestHelper:

    def __init__(self, **kwargs):

        self.kwargs = kwargs
        self.collection_name = request.path.split('/')[2] # the collection name will be the 2nd part of the path
        self.collection = db[self.collection_name] # get the collection using the collection name
        self.req = self.get_request_json() # get the request data in json format
        self.process_request() # set the request id and process request data
        self.auth = request.authorization # get the authorization from the request

    def get_db_data(self):
        return self.db_data

    def get_collection_name(self):
        return self.collection_name

    def get_collection(self):
        return self.collection

    def get_request_json(self):
        try:
            return request.get_json()
        except:
            return None

    def api_key(self):
        try:
            return request.headers['Api-Key']
        except KeyError:
            raise ErrorResponse(401, 'No API key was supplied')

    def get_request(self):
        return self.req

    def get_item(self, item):
        return self.req[item]

    def get_id(self):
        return self.req_id

    def set_item(self, key, val):
        self.req[key] = val
        return True

    def set_date(self, field_name):
        self.set_item(field_name, datetime.strptime(self.get_item(field_name), "%d/%m/%Y"))

    #find the proper id for the request and set it:
    def process_request(self):
        method = request.method
        if method == 'POST':
            # creating new doc; set defaults for req_id and db_data
            self.req_id = 0
            self.db_data = None
            return
        try:
            self.kwargs['_id'] = bson.ObjectId(self.kwargs['_id'])
        except KeyError:
            # nothing to do here- the other identifiers (ie. email) do not need to be converted to bson.ObjectId
            pass

        # query the database to find the corresponding data
        obj = self.collection.find_one(self.kwargs)
        # set the req_id and request_data

        try:
            self.req_id = obj.get('_id')
            self.db_data = obj
        except AttributeError:
            raise ErrorResponse(404)
