from crud import *
from setup import *
from user import User
MethodView = views.MethodView
class API(MethodView):

    def __init__(self):
        self.req = request.get_json()

    def handle_request(self):
        req = self.req
        return str(req)
    #TODO refactor here
        # try:
        #     req_id = req["_id"]
        # except:
        #     req_id = req[0]["_id"]
        # if current_user.can_edit_request(req_id, collection_name, authorization):
        #     return view_function(collection_name = collection_name, user = current_user, request = req)
        # else:
        #     #user not authenticated
        #     abort(403, "You do not have permission to edit the requested resource.")


    def get(self):
        crud = Crud(self.request, collection_name = collection_name)
        crud.find_doc()

    def post(self):
        return self.handle_request()
        crud = Crud(self.request, collection_name = collection_name)
        crud.find_doc()

    def delete(self):
        crud = Crud(self.request, collection_name = collection_name)
        crud.delete_doc()

    def put(self, user_id):
        crud = Crud(self.request, collection_name = collection_name)
        crud.update_doc()
