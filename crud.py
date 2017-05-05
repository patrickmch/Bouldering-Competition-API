from setup import *
class Crud:
    def __init__(self, collection):
        self.collection = collection

    def find_doc(self, req_id):
        info = self.collection.find_one(ObjectId(self._id))
        return str(info)

    def create_doc(self, req):
        try:
            return str(req.get_req())
            new_id = self.collection.insert_one(req.get_req()).inserted_id
        except pymongo.errors.WriteError as error:
            #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
            logging.error(error)
            return "Failed to insert the requested data in to the database as one or more fields was missing or incomplete"
        else:
            return "success %s" % str(new_id)

    def update_doc(self, req):
        request = self.request
        try:
            result = self.collection.update_one(request[0], request[1], False)
        except KeyError as error:
            return "A KeyError was raised. Please make sure that you are using the \'_id\' key for all updates, and that the key for the field \'%s\' exists." % request[1]['$set'].keys()[0]
        except bson.errors.InvalidId as error:
            return "Invalid id"
        else:
            if result.matched_count < 1:
                return "No matching record exists for id %s" % request[0]["_id"]
            elif result.modified_count < 1:
                return "Failed to update \'%s\' with an id of \'%s\'" % (request[1]["$set"].keys()[0], request[0]["_id"])
            else:
                return  "%s record was successfully updated" % str(result.matched_count)

    def delete_doc(self, req_id):
        try:
            result = self.collection.delete_one({"_id" : ObjectId(self.request["_id"])})
        except:
            raise
        else:
            #TODO do not reveal id
            if result.deleted_count < 1:
                return "No records were deleted with id %s" % self.request["_id"]
            else:
                return "%s record with the id %s was deleted successfully" % (str(result.deleted_count), self.request["_id"])
