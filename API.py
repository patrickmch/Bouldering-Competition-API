from crud import Crud
from setup import *
from flask import views
MethodView = views.MethodView

class API(MethodView):

    def __init__(self):
        self.crud = Crud()
        self.collection = g.req.get_collection()

    def get(self):
        return self.crud.find_doc()

    def post(self):
        return self.crud.create_doc()

    def delete(self):
        return self.crud.delete_doc()

    def put(self):
        return self.crud.update_doc()
