from crud import *
from setup import *
from API import API
from request_helper import RequestHelper

class UserAPI(API):

    def __init__(self):
        self.crud = Crud()
        self.collection = g.req.get_collection()

    # create new user:
    def post(self):
        req = g.req
        # check email to make sure it is not a duplicate account
        req_email = req.get_req_item("email")
        query = self.collection.find({"email" : req_email})
        if query.count() > 0:
            return "The email you provided is already in use."
        #create new datetime object for easier querying
        req.set_date("birthday")
        # encrypt password
        req.set_req("password", pwd_encrypt.hash(req.get_req_item("password")))
        return self.crud.create_doc()
