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

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def handle_request(view_function):
    @wraps(view_function)
    def decorated_function(**kwargs):
        # kwargs has user id and collection name passed in url (if any)
        # the request's user id and the kwarg's user id will be different if the user is trying to edit another user
        req = request.get_json()
        if not kwargs:
            # assumption is that no kwargs means create user is being called: return the view function
            return view_function(req)
        user = User(db.participants.find_one({"_id" : ObjectId(kwargs.get("id"))}))
        collection_name = kwargs.get("collection_name")
        return str(user.get_id())
        if user.can_edit_request(req["_id"], collection_name, authorization):
            return view_function(collection_name = collection_name, user = user, request = request)
        else:
            #user not authenticated
            abort(403, "You do not have permission to edit the requested resource.")
    return decorated_function
