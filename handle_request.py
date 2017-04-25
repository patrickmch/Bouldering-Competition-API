from setup import *
from user import User

authorization = {
    'participants': {
        'participant': False,
        'judge' : True,
        'admin': True
    },
    'competitions': {
        'participant' : False,
        'judge' : True,
        'admin': True
    },
    'venue' : {
        'participant' : False,
        'judge' : False,
        'admin' : True
    }
}

def handle_request(view_function):
    @wraps(view_function)
    def decorated_function(**kwargs):
        #get the app key, collection name, and user data
        #kwargs has user id and collection name passed in url (if any)
        req = request.get_json()
        user_id = ObjectId(kwargs.get("id"))
        try:
            user = User(db.participants.find_one({"_id" : ObjectId(user_id)}))
        except:
            # no user id means create user is being called: return the view function
            user = User(None)
            return view_function(req)
        collection_name = kwargs.get("collection_name")
        if user.is_valid_appkey(collection_name, req['_id'], authorization):
            return view_function(collection_name = collection_name, user = user, request = request)
        else:
            #user not authorized
            abort(401)
    return decorated_function
