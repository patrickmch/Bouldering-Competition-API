from setup import *
from user import User

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
            user = User(None)
            return view_function(req)
        collection_name = kwargs.get("collection_name")
        user.is_valid_appkey(collection_name, req['_id'])
        return view_function(collection_name = collection_name, user = user, request = request)
    return decorated_function
