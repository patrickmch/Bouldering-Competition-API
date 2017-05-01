from crud import *
from setup import *
class UserAPI(MethodView):

    def __init__(self, req):
        self.req = req
        self.collection_name = "competitions"

    # find a single comp:
    def get(self):
        # TODO should we just return data here rather than trying to call crud?
        crud = Crud(self.request, collection_name = collection_name)
        crud.find_doc()

    # create new comp:
    def post(self):
        self.collection == db.competitions:
        request["comp_date"] = datetime.strptime(request["comp_date"], "%d/%m/%Y")
        #add a venue id to the competitions to enforce a relationship between the two collections
        request["venue_id"] = ObjectId(request["venue_id"])
        crud = Crud(self.request, collection_name = collection_name)
        crud.create_doc()

    # delete a single comp
    def delete(self):
        crud = Crud(self.request, collection_name = collection_name)
        crud.delete_doc()

    #u
    def put(self, user_id):
        crud = Crud(self.request, collection_name = collection_name)
        crud.update_doc()
