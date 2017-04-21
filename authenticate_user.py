from setup import *

def filter_request(view_function):
    @wraps(view_function)
    def decorated_function(**kwargs):
        #TODO this is sloppy, but breaks without it
        from flask import request
        #get the app key, collection name, and user data
        collection_name = kwargs.get("collection_name")
        app_key = ObjectId(kwargs.get("id"))
        user = db.participants.find_one({"_id" : ObjectId(app_key)})
        request = request.get_json()
        # TODO this can't be called for create_user
        is_valid_appkey(app_key, collection_name, user)
        return view_function(collection_name = collection_name, user = user, app_key = app_key, request = request)
    return decorated_function

# user authentication/authorization
# require app_key requires the user to send a key parameter (the user id- NOT reccommended for live applications)
# in the url that authenticates them
def is_valid_appkey(app_key, collection_name, user):
    #user id is the app key (for demo purposes only!!)
    if user["_id"] == app_key:
        if user_is_auth(collection_name, user["role"]):
            return True
        else:
            #user not authorized
            abort(403)
    else:
        #user not authenticated
        abort(401)

#pass the collection name and user role to determine if user is authorized to modify a collection
# based on rules stored in a dictionary
def user_is_auth(collection_name, role):
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
    return authorization[collection_name][role]
