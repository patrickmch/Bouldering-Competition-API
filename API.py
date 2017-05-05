from crud import *
from setup import *
from user import User
MethodView = views.MethodView

class API(MethodView):


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


    def get(self):
        self.handle_request()
        return crud.find_doc()

    def post(self):
        self.handle_request()
        return crud.find_doc()

    def delete(self):
        self.handle_request()
        return crud.delete_doc()

    def put(self, user_id):
        self.handle_request()
        return crud.update_doc()
