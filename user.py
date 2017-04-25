from setup import *

class User:
    def __init__(self, dic):
        self.vars = dic

    def get_var(self, var):
        return self.vars.get(var)


    # check if the user is sending other users' data and if they are authorized to do so
    def can_edit_user(self, req_id):
        if self.vars.get('_id') != req_id and self.vars.get('role') == "admin":
            return True
        elif self.vars.get('_id') == req_id:
            return True
        else:
            #user not authorized to modify others' info
            #TODO better error messages along side this??
            abort(403)

    """pass the collection name and user role to determine if user is authorized to modify a collection
    based on rules stored in a dictionary """
    def can_edit_collection(self, collection_name):
        authorization = {
            'participants': {
                'participant': True,
                'admin': True
            },
            'competitions': {
                'participant' : False,
                'admin': True
            },
            'venue' : {
                'participant' : False,
                'admin' : True
            }
        }
        return authorization[collection_name][self.role]

    """user authentication/authorization
    require app_key requires the user to send a key parameter (the user id)
    in the url that authenticates them"""
    def is_valid_appkey(self, collection_name, req_id):
        #user id is the app key (for demo purposes only!!)
        if self.vars.get('_id') == req_id:
            if self.can_edit_collection(collection_name):
                return True
            else:
                #user not authorized
                abort(403)
        else:
            #user not authenticated
            abort(401)
