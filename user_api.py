from crud import *
from setup import *
class UserAPI(MethodView):

    def get(self, user_id):
        # if new_user check email to make sure it is not a duplicate account
        query = self.collection.find({"email" : request["email"]})
        if query.count() > 0:
            return "The email you provided is already in use."
        #create new datetime object for easier querying
        self.request["birthday"] = datetime.strptime(request["birthday"], "%d/%m/%Y")
        # encrypt password
        self.request["password"] = pwd_encrypt.hash(self.request["password"])
        crud = Crud(self.request, collection_name = "participants", user = user)
        crud.find_doc()

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass
