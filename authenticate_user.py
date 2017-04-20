from setup import *
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        collection_name = kwargs.get("collection_name")
        app_key = ObjectId(kwargs.get("id"))
        user = db.participants.find_one({"_id" : ObjectId(app_key)})
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
