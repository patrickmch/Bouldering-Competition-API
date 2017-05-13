from setup import *
import sys
class RequestHelper:

    def __init__(self, **kwargs):

        self.kwargs = kwargs
        self.collection_name = request.path.split('/')[2] # the collection name will be the 2nd part of the path
        self.collection = db[self.collection_name] # get the collection using the collection name
        self.req = self.get_request_json() # get the request data in json format
        self.process_request() # set the request id and process request data
        self.auth = request.authorization # get the authorization from the request

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
            abort(401, 'no api_key supplied')

    def get_request(self):
        return self.req

    def get_item(self, item):
        return self.req[item]

    def get_req_id(self):
        return self.req_id

    def set_item(self, key, val):
        self.req[key] = val
        return True

    def set_date(self, field_name):
        self.set_item(field_name, datetime.strptime(self.get_item(field_name), "%d/%m/%Y"))

    #find the proper id for the request and set it:
    def process_request(self):
        if self.collection_name == 'participants':
            # an email means that a user is being edited
            identifier = 'email'
        else:
            # an id means a venue or comp is being edited
            identifier = '_id'
        try:
            #loop through request to find an id or an email
            for key, value in self.req.items():
                if key == identifier:
                    search_value = value
        except AttributeError:
            # there was no json data so find the values passed in the url string
            search_value = self.kwargs.get(identifier)
        # query the database to find the corresponding data
        obj = self.collection.find_one({identifier : search_value})
        try:
            # data was found; set the req_id and request_data
            self.req_id = obj.get('_id')
            self.request_data = obj
        except AttributeError:
            # no data found; 0 indicates new user being created
            self.req_id = 0
            self.request_data = None
