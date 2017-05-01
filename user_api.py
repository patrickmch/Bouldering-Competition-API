from crud import *
from setup import *
from API import API

class UserAPI(API):
    collection = db.participants

    # create new user:
    # def post(self):
    #     # if new_user check email to make sure it is not a duplicate account
    #     query = self.collection.find({"email" : request["email"]})
    #     if query.count() > 0:
    #         return "The email you provided is already in use."
    #     #create new datetime object for easier querying
    #     self.request["birthday"] = datetime.strptime(request["birthday"], "%d/%m/%Y")
    #     # encrypt password
    #     self.request["password"] = pwd_encrypt.hash(self.request["password"])
    #     crud = Crud(self.request, collection = collection)
    #     crud.create_doc()
