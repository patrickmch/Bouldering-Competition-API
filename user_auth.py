from setup import *
from user import *
from request_helper import RequestHelper

class UserAuth:

    def __init__(self):
        self.req = RequestHelper()
        self.auth = request.authorization

    # this dict determines user roles
    user_authorization = {
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

    # check if the user is sending data they are authorized to edit
    def can_edit_request(self):
        if current_user.get_var('_id') == self.req.get_req_id():
            # user is editing themself - always authorized
            return True
        else:
            #use the collection name and user role to determine if user is authorized to modify a collection
            #based on values stored in a dictionary
            return authorization[self.collection_name][current_user.get_var('role')]

    def handle_request(self):
        if not self.can_edit_request():
            #user not authenticated
            abort(403, 'You do not have permission to access the requested resource.')

    @staticmethod
    def login():
        user_data = db.participants.find_one({'email' : request.authorization['username']})
        if pwd_encrypt.verify(req['password'], user_data['password']):
            user = User(user_data)
            login_user(user)
            return str(user.get_id())
        else:
            return 'incorrect password for email %s' % request.authorization['username']

    @staticmethod
    def logout():
        logout_user()
        return 'logged out'

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        user = User(participants.find_one({'_id' : ObjectId(user_id)}))
        return user
