from setup import *
from user import User

def handle_request(view_function):
    @wraps(view_function)
    def decorated_function(**kwargs):
        # kwargs has user id and collection name passed in url (if any)
        req = request.get_json()
        try:
            req_id = req["_id"]
        except:
            req_id = req[0]["_id"]

        if not kwargs:
            # assumption is that no kwargs means create user is being called: return the view function
            return view_function(req)
        collection_name = kwargs.get("collection_name")
        if current_user.can_edit_request(req_id, collection_name, authorization):
            return view_function(collection_name = collection_name, user = current_user, request = req)
        else:
            #user not authenticated
            abort(403, "You do not have permission to edit the requested resource.")
    return login_required(decorated_function)
