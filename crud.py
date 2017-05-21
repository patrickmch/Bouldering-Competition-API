from setup import *
from response_handler import ErrorResponse
class Crud:
    def __init__(self):
        self.collection = g.req.get_collection()

    def find_doc(self):
        # we should have already found db data in the process_request method when instantiate_req was called
        data = g.req.get_db_data()
        if data == None:
            raise ErrorResponse(404)
        if g.req.get_collection_name() == 'participants':
            # remove the password and _id from the return set if this is a user
            data.pop('password', None)
            data.pop('_id', None)
        response = {
            'status_code' : 201,
            'data' : data
        }
        return jsonify(response)

    def create_doc(self):
        try:
            new_id = str(self.collection.insert_one(g.req.get_request()).inserted_id)
        except pymongo.errors.WriteError:
             raise ErrorResponse(400, 'Failed to insert the requested data in to the database because one or more fields was missing or incomplete')
        response = {
            'status_code' : 200,
            '_id' : new_id
        }
        return jsonify(response)


    def update_doc(self):
        insert = g.req.get_request()
        result = self.collection.update_one({'_id' : ObjectId(g.req.get_id())}, {'$set' : insert}, False)
        if result.matched_count < 1:
            raise ErrorResponse(404)
        response = {
            'status_code' : 200
        }
        return jsonify(response)



    def delete_doc(self):
        result = self.collection.delete_one({"_id" : ObjectId(g.req.get_id())})
        if result.deleted_count < 1:
            raise ErrorResponse(404)
        response = {
            'status_code' : 200
        }
        return jsonify(response)
