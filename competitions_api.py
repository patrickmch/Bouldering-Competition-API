from crud import *
from setup import *
from API import API

class CompAPI(API):

    def __init__(self):
        super(UserAPI, self).__init__()

    # create new comp:
    #TODO redo here to use g.req
    def post(self):
        request["comp_date"] = datetime.strptime(request["comp_date"], "%d/%m/%Y")
        #add a venue id to the competitions to enforce a relationship between the two collections
        request["venue_id"] = ObjectId(request["venue_id"])
        crud = Crud(self.request, collection = collection)
        crud.create_doc()
