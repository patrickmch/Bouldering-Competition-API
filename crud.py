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
        return self.create_response(data)

    def create_doc(self):
        try:
            new_id = self.collection.insert_one(g.req.get_request()).inserted_id
        except pymongo.errors.WriteError as error:
            #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
            logging.error(error)
            return "Failed to insert the requested data in to the database as one or more fields was missing or incomplete"
        else:
            return "success %s" % str(new_id)

    def update_doc(self):
        insert = g.req.get_request()
        try:
            result = self.collection.update_one({'_id' : ObjectId(g.req.get_id())}, {'$set' : insert}, False)
        except KeyError as error:
            return "A KeyError was raised. Please make sure that you are using the \'_id\' key for all updates, and that the key for the field \'%s\' exists." % insert[1]['$set'].keys()[0]
        except bson.errors.InvalidId as error:
            return "Invalid id"
        else:
            if result.matched_count < 1:
                return "No matching record exists for id %s" % insert[0]["_id"]
            elif result.modified_count < 1:
                return "Failed to update \'%s\' with an id of \'%s\'" % (insert[1]["$set"].keys()[0], insert[0]["_id"])
            else:
                return  "%s record was successfully updated" % str(result.matched_count)

    def delete_doc(self):
        result = self.collection.delete_one({"_id" : ObjectId(g.req.get_id())})
        #TODO do not reveal id if it is a user id
        if result.deleted_count < 1:
            return "No records were deleted with id %s" % g.req.get_id()
        else:
            return "%s record with the id %s was deleted successfully" % (str(result.deleted_count), g.req.get_id())

    def create_response(self, result):
        pass
