from setup import *
class Crud:
    def __init__(self):
        self.collection = g.req.get_collection()

    def find_doc(self):
        # we should have already found db data in the process_request method when instantiate_req was called
        data = g.req.get_db_data()
        if data == None:
            # if there was no data already, look again
            data = self.collection.find_one(ObjectId(g.req.get_id()))
        if g.req.get_collection_name() == 'participants':
            # remove the password and _id from the return set if this is a user
            data.pop('password', None)
            data.pop('_id', None)
        return g._response.create_response(data)

    def create_doc(self):
        try:
            result = self.collection.insert_one(g.req.get_request()).inserted_id
        except pymongo.errors.WriteError as error:
            #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
            logging.error(error)
            return "Failed to insert the requested data in to the database as one or more fields was missing or incomplete"
        else:
            return "success %s" % str(result)

    def update_doc(self):
        insert = g.req.get_request()
        try:
            result = self.collection.update_one({'_id' : ObjectId(g.req.get_id())}, {'$set' : insert}, False)
        except Exception as e:
            #TODO add logging function here...
            result = e
            # except bson.errors.InvalidId as error:
            #     return "Invalid id"
        return g._response.create_response(result)



    def delete_doc(self):
        result = self.collection.delete_one({"_id" : ObjectId(g.req.get_id())})
        #TODO do not reveal id if it is a user id
        return g._response.create_response(result)
        # if result.deleted_count < 1:
        #     return "No records were deleted with id %s" % g.req.get_id()
        # else:
        #     return "%s record with the id %s was deleted successfully" % (str(result.deleted_count), g.req.get_id())
