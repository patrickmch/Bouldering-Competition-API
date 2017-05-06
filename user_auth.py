from setup import *
from user import *
from request_helper import RequestHelper

class UserAuth:

    def __init__(self, user):
        self.user = user

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
        if self.user.get_var('_id') == g.req.get_req_id():
            # user is editing themself - always authorized
            return True
        else:
            #use the collection name and user role to determine if user is authorized to modify a collection
            #based on values stored in a dictionary
            return self.user_authorization[g.req.get_collection_name()][self.user.get_var('role')]

    def authenticate_user(self):
        if g.req.api_key() != self.user.get_id():
            abort(401, 'You did not provide valid login credentials')
        elif not self.can_edit_request():
            #user not authenticated
            abort(403, 'You do not have permission to access the requested resource.')


    @staticmethod
    def login():
        # TODO refactor login
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
