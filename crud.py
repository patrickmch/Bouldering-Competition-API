from setup import *
from response_handler import create_response, ErrorResponse
class Crud:
    def __init__(self):
        self.collection = g.req.get_collection()

    def find_doc(self):
        # we should have already found db data in the process_request method when instantiate_req was called
        data = g.req.get_db_data()
        if g.req.get_collection_name() == 'participants':
            # remove the password and _id from the return set if this is a user
            data.pop('password', None)
            data.pop('_id', None)
        else:
            data['_id'] = str(data['_id'])
        return create_response(201, data)

    def create_doc(self):
        try:
            new_id = str(self.collection.insert_one(g.req.get_request()).inserted_id)
        except pymongo.errors.WriteError:
             raise ErrorResponse(400, 'Failed to insert the requested data in to the database because one or more fields was missing or incomplete')
        return create_response(200, {'_id' : new_id})


    def update_doc(self):
        insert = g.req.get_request()
        result = self.collection.update_one({'_id' : ObjectId(g.req.get_id())}, {'$set' : insert}, False)
        if result.matched_count < 1:
            #unknown error- if the document was not found a 404 would have already been raised in process request
            raise ErrorResponse(500)
        return create_response(200)



    def delete_doc(self):
        result = self.collection.delete_one({"_id" : ObjectId(g.req.get_id())})
        if result.deleted_count < 1:
            #unknown error- if the document was not found a 404 would have already been raised in process request
            raise ErrorResponse(500)
        return create_response(200)
