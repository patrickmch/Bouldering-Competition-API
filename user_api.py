from setup import *
from API import API

class UserAPI(API):

    def __init__(self):
        super(UserAPI, self).__init__()

    # create new user:
    def post(self):
        req = g.req
        # check email to make sure it is not a duplicate account
        req_email = req.get_item('email')
        query = self.collection.find({'email' : req_email})
        if query.count() > 0:
            #TODO raise ErrorResponse
            return 'The email you provided is already in use.'
        #create new datetime object for easier querying
        req.set_date('birthday')
        # encrypt password
        req.set_item('password', pwd_encrypt.hash(req.get_item('password')))
        return self.crud.create_doc()
