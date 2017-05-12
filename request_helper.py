from setup import *

class RequestHelper:

    def __init__(self):

        self.collection_name = request.path.split('/')[2] # the collection name will be the 2nd part of the path
        self.collection = db[self.collection_name] # get the collection using the collection name
        self.req = request.get_json() # get the request data in json format
        self.req_id = self.set_req_id() # set the request id
        self.auth = request.authorization # get the authorization from the request

    def get_collection_name(self):
        return self.collection_name

    def get_collection(self):
        return self.collection

    def api_key(self):
        return request.headers['Api-Key']

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
    def set_req_id(self):
        try:
            #loop through request to find an id or an email
            for key, value in self.req.items():
                # an email means that a user is being edited
                if key == 'email':
                    email = value
                    break
                # an id indicates that a comp or venue is being edited
                elif key == '_id':
                    req_id = value
                    break
        except AttributeError:
            # id or email passed in the url string
            if collection_name == 'participants':
                email = request.args.get('email')
            else:
                req_id = request.args.get('_id')
        try:
            obj = self.collection.find_one({'email' : email})
                try:
                    self.req_id = obj.get('_id')
                except:
                    # 0 is default; indicates new user being created
                    self.req_id = 0
        except NameError:
            req_id = self.req_id
        return self.req_id
