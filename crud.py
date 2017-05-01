from setup import *
class Crud:
    def __init__(self, **kwargs):
        self.collection_name = kwargs.get("collection_name", "participants")
        self.collection = db[self.collection_name]
        self.request = kwargs.get("request")
        self.user = kwargs.get("user", "new_user")

    def find_doc(self):
        info = self.collection.find_one(ObjectId(self._id))
        return str(info)

    def create_doc(self):

        request = self.request
        # elif self.collection == db.competitions:
        #     request["comp_date"] = datetime.strptime(request["comp_date"], "%d/%m/%Y")
        #     #add a venue id to the competitions to enforce a relationship between the two collections
        #     request["venue_id"] = ObjectId(request["venue_id"])
        try:
            new_id = self.collection.insert_one(request).inserted_id
        except pymongo.errors.WriteError as error:
            #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
            logging.error(error)
            return "Failed to insert the requested data in to the database as one or more fields was missing or incomplete"
        else:
            return "success %s" % str(new_id)

    def update_doc(self):
        request = self.request
        try:
            result = self.collection.update_one(request[0], request[1], False)
        except KeyError as error:
            return "A KeyError was raised. Please make sure that you are using the \'_id\' key for all updates, and that the key for the field \'%s\' exists in the \'%s\' collection." % (request[1]['$set'].keys()[0], self.collection_name)
        except bson.errors.InvalidId as error:
            return "Invalid id"
        else:
            if result.matched_count < 1:
                return "No matching record exists for id %s" % request[0]["_id"]
            elif result.modified_count < 1:
                return "Failed to update \'%s\' with an id of \'%s\'" % (request[1]["$set"].keys()[0], request[0]["_id"])
            else:
                return  "%s record was successfully updated" % str(result.matched_count)

    def delete_doc(self):
        try:
            result = self.collection.delete_one({"_id" : ObjectId(self.request["_id"])})
        except:
            raise
        else:
            if result.deleted_count < 1:
                return "No records were deleted with id %s" % self.request["_id"]
            else:
                return "%s record with the id %s was deleted successfully" % (str(result.deleted_count), self.request["_id"])
