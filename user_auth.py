from setup import *
from user import *
from flask import request
from settings import user_authorization
class UserAuth:

    def __init__(self, user):
        self.user = user

    # check if the user is sending data they are authorized to edit
    def can_edit_request(self):
        if self.user.get_var('_id') == g.req.get_req_id():
            # user is editing themself - always authorized
            return True
        else:
            #use the collection name and user role to determine if user is authorized to modify a collection
            #based on values stored in a dictionary
            return user_authorization[g.req.get_collection_name()][self.user.get_var('role')]

    def authenticate_user(self):
        if g.req.api_key() != self.user.get_id():
            raise ErrorResponse(401, 'You did not provide valid login credentials')
        elif not self.can_edit_request():
            #user not authenticated
            raise ErrorResponse(403, 'You do not have permission to access the requested resource.')


    @staticmethod
    def login():
        user_data = db.participants.find_one({'email' : request.authorization['username']})
        if pwd_encrypt.verify(request.authorization['password'], user_data['password']):
            user = User(user_data)
            flask_login.login_user(user)
            return create_response(200, {'api_key' : str(user.get_id())})
        else:
            raise ErrorResponse(401, 'Invalid password')

    @staticmethod
    def logout():
        flask_login.logout_user()
        return create_response(200, {'message' : 'Logout successful'})
