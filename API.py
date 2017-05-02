from crud import *
from setup import *
from user import User
MethodView = views.MethodView
class API(MethodView):

    def __init__(self):
        self.req = request.get_json()

    # check if the user is sending data they are authorized to edit
    def can_edit_request(self):
        if current_user.get_var('_id') == req_id:
            # user is editing themself - always authorized
            return True
        elif current_user.get_var('_id') != req_id:
            """pass the collection name and user role to determine if user is authorized to modify a collection
            based on values stored in a dictionary"""
            return authorization[collection_name][self.vars.get('role')]
        else:
            return False

    def handle_request(self):
        req = self.req
        return str(req)
    #TODO refactor here
        try:
            req_id = req["_id"]
        except:
            req_id = req[0]["_id"]
        if self.can_edit_request():
            return view_function(collection_name = collection_name, user = current_user, request = req)
        else:
            #user not authenticated
            abort(403, "You do not have permission to edit the requested resource.")


    def get(self):
        create_crud_instance()
        crud.find_doc()

    def post(self):
        return self.handle_request()
        create_crud_instance()
        crud.find_doc()

    def delete(self):
        create_crud_instance()
        crud.delete_doc()

    def put(self, user_id):
        create_crud_instance()
        crud.update_doc()

    def create_crud_instance():
        crud = Crud(self.request, collection_name = self.collection_name)
