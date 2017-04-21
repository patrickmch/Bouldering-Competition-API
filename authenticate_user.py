from setup import *

# user authentication/authorization
# require app_key requires the user to send a key parameter (the user id- NOT reccommended for live applications)
# in the url that authenticates them
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        #get the app key, collection name, and user data
        collection_name = kwargs.get("collection_name")
        app_key = ObjectId(kwargs.get("id"))
        user = db.participants.find_one({"_id" : ObjectId(app_key)})
        #user id is the app key (for demo purposes only!!)
        if user["_id"] == app_key:
            if user_is_auth(collection_name, user["role"]):
                return view_function(*args, **kwargs)
            else:
                #user not authorized
                abort(403)
        else:
            #user not authenticated
            abort(401)
    return decorated_function

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
