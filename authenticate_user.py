from setup import *

class User:
    def __init__(self, dic):
        self.vars = dic

    def get_var(self, var):
        return self.vars.get(var)

    # check if the user is sending other users' data and if they are authorized to do so
    def can_edit_user(self, request):
        if self._id != request["_id"] and self.role == "admin":
            return
        elif self._id == request["_id"]:
            return
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




def filter_request(view_function):
    @wraps(view_function)
    def decorated_function(**kwargs):
        #get the app key, collection name, and user data
        req = request.get_json()
        # if not kwargs:
        #     # if there are no keyword arguments create_user is being called
        #     # return the view function and create a new user
        #     return view_function(request)

        try:
            # user_data = db.participants.find_one({"_id" : ObjectId(kwargs.get("id"))})
            user = User(db.participants.find_one({"_id" : ObjectId(kwargs.get("id"))}))
            # user = User(user_data)
            return str(user.get_var('_id'))
        except:
            user = User(None)
        collection_name = kwargs.get("collection_name")

        # @login_manager.user_loader
        # def load_user(user_id):
        #     return User.get(user_id)
        # app_key = ObjectId(kwargs.get("id"))
        # user = user_instance(app_key)
        # is_valid_appkey(app_key, collection_name, user)
        # edit_self(user, request)
        # return view_function(collection_name = collection_name, user = user, request = request)
        return "test %s" % str(user)
    return decorated_function
