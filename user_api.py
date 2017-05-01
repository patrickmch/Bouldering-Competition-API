from crud import *
from setup import *
class UserAPI(MethodView):

    def __init__(self, req):
        self.req = req
        self.collection_name = "participants"

    # find a single user:
    def get(self):
        # TODO should we just return data here rather than trying to call crud?
        crud = Crud(self.request, collection_name = collection_name)
        crud.find_doc()

    # create new user:
    def post(self):
        # if new_user check email to make sure it is not a duplicate account
        query = self.collection.find({"email" : request["email"]})
        if query.count() > 0:
            return "The email you provided is already in use."
        #create new datetime object for easier querying
        self.request["birthday"] = datetime.strptime(request["birthday"], "%d/%m/%Y")
        # encrypt password
        self.request["password"] = pwd_encrypt.hash(self.request["password"])
        crud = Crud(self.request, collection_name = collection_name)
        crud.create_doc()

    # delete a single user
    def delete(self):
        crud = Crud(self.request, collection_name = collection_name)
        crud.delete_doc()

    def put(self, user_id):
        crud = Crud(self.request, collection_name = collection_name)
        crud.update_doc()
