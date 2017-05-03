from crud import *
from setup import *
from user import User
from req import Req
MethodView = views.MethodView

class API(MethodView):

    # check if the user is sending data they are authorized to edit
    def can_edit_request(self):
        if current_user.get_var('_id') == req.get_req_id():
            # user is editing themself - always authorized
            return True
        else:
            #use the collection name and user role to determine if user is authorized to modify a collection
            #based on values stored in a dictionary
            return authorization[collection_name][self.vars.get('role')]

    def handle_request(self):
        req = Req(request.get_json())
        req.set_req_id(self.collection)
        crud = Crud(self.request, collection_name = self.collection_name)
        if not self.can_edit_request():
            #user not authenticated
            abort(403, 'You do not have permission to access the requested resource.')


    def get(self):
        self.handle_request()
        crud.find_doc()

    def post(self):
        return self.handle_request()
        self.handle_request()
        crud.find_doc()

    def delete(self):
        self.handle_request()
        crud.delete_doc()

    def put(self, user_id):
        self.handle_request()
        crud.update_doc()
