from crud import *
from setup import *
from user import User
MethodView = views.MethodView

class API(MethodView):

    def __init__(self):
        self.crud = Crud()
        self.collection = g.req.get_collection()

    def get(self):
        return 'hello'
        # return str(request.args)
        return crud.find_doc()

    def post(self):
        return crud.create_doc()

    def delete(self):
        return crud.delete_doc()

    def put(self):
        return crud.update_doc()
