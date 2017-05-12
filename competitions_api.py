from crud import *
from setup import *
from API import API

class CompAPI(API):

    def __init__(self):
        super(UserAPI, self).__init__()

    # create new comp:
    def post(self):
        g.req.set_date('comp_date')
        #add a venue id to the competitions to enforce a relationship between the two collections
        g.req.set_item('venue_id', ObjectId(g.req.get_item('venue_id')))
        crud.create_doc()
