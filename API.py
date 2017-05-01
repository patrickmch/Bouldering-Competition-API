from crud import *
from setup import *
MethodView = views.MethodView
class API(MethodView):

    def __init__(self, req = None):
        self.req = req

    # find a single comp:
    def get(self):
        return 'exito'
        # crud = Crud(self.request, collection_name = collection_name)
        # crud.find_doc()

    # create new comp:
    def post(self):
        crud = Crud(self.request, collection_name = collection_name)
        crud.find_doc()

    # delete a single comp
    def delete(self):
        crud = Crud(self.request, collection_name = collection_name)
        crud.delete_doc()

    # update single comp
    def put(self, user_id):
        crud = Crud(self.request, collection_name = collection_name)
        crud.update_doc()
