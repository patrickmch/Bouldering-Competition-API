from setup import *

def filter_request(view_function):
    @wraps(view_function)
    def decorated_function(**kwargs):
        #TODO this is sloppy, but breaks without it
        from flask import request
        #get the app key, collection name, and user data
        request = request.get_json()
        if not kwargs:
            # if there are no keyword arguments create_user is being called
            # return the view function and create a new user
            return view_function(request)
        collection_name = kwargs.get("collection_name")
        app_key = ObjectId(kwargs.get("id"))
        user = db.participants.find_one({"_id" : app_key})
        is_valid_appkey(app_key, collection_name, user)
        edit_self(user, request)
        return view_function(collection_name = collection_name, user = user, _id = app_key, request = request)
    return decorated_function


# check if the user is sending other users' data and if they are authorized to do so
def edit_self(user, request):
    if user["_id"] != request["_id"] and user["role"] == "admin":
        return
    elif user["_id"] == request["_id"]:
        return
    else:
        #user not authorized to modify others' info
        #TODO better error messages along side this??
        abort(403)

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
