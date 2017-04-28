from setup import *

class User:
    def __init__(self, dic):
        self.vars = dic

    def get_var(self, var):
        return self.vars.get(var)

    # check if the user is sending data they are authorized to edit
    def can_edit_request(self, req_id, collection_name, authorization):
        if self.vars.get("_id") == req_id:
            # user is editing themself - always authorized
            return True
        elif self.vars.get('_id') != req_id:
            """pass the collection name and user role to determine if user is authorized to modify a collection
            based on values stored in a dictionary"""
            return authorization[collection_name][self.vars.get('role')]
        else:
            return False

    # necessary for flask_login
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.vars.get("_id"))

    def is_authenticated(self):
        return True
