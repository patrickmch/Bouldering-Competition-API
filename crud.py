from setup import *
class Crud:
    def __init__(self, **kwargs):
        self.collection = db[kwargs['collection_name']]
        self.request = kwargs['request']
        self.app_key = kwargs['app_key']
        self.user = kwargs['user']

    def find_doc(collection_name, id):
        collection = db[collection_name]
        info = collection.find_one(ObjectId(id))
        return str(info)


    def create_doc(self):
        request = self.request
        if self.collection == db.participants:
            # check to make sure user does not already have an account
            query = self.collection.find({"email" : request["email"]})
            if query.count() > 0:
                return "The email you provided is already in use."
            #create new datetime object for easier querying
            self.request["birthday"] = datetime.strptime(request["birthday"], "%d/%m/%Y")
        elif self.collection == db.competitions:
            request["comp_date"] = datetime.strptime(request["comp_date"], "%d/%m/%Y")
            #add a venue id to the competitions to enforce a relationship between the two collections
            request["venue_id"] = ObjectId(request["venue_id"])
        try:
            new_id = self.collection.insert_one(request).inserted_id
        except pymongo.errors.WriteError as error:
            #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
            logging.error(error)
            return "Failed to create a participant as one or more required fields were missing or incomplete"
        else:
            return "success %s" % str(new_id)

    #TODO update_doc allows others to edit their profile (this should require authorization)
    def update_doc(collection_name):
        collection = db[collection_name]
        update_info = request.get_json()
        try:
            #to be searchable the doc id must not be a string but an ObjectId
            update_info[0]['_id'] = ObjectId(update_info[0]['_id'])
            result = collection.update_one(update_info[0], update_info[1], False)
        except KeyError as error:
            return "A KeyError was raised. Please make sure that you are using the \'_id\' key for all updates, and that the key for the field \'%s\' exists in the \'%s\' collection." % (update_info[1]['$set'].keys()[0], collection_name)
        except bson.errors.InvalidId as error:
            return "Invalid id"
        else:
            if result.matched_count < 1:
                return "No matching record exists for id %s" % update_info[0]['_id']
            elif result.modified_count < 1:
                return "Failed to update \'%s\' with an id of \'%s\'" % (update_info[1]['$set'].keys()[0], update_info[0]['_id'])
            else:
                return  "%s record was successfully updated" % str(result.matched_count)

    def delete_doc(collection_name, id):
        #currently, users can only delete their own profiles
        collection = db[collection_name]
        try:
            result = collection.delete_one({"_id" : ObjectId(id)})
        except:
            raise
        else:
            if result.deleted_count < 1:
                return "No records were deleted with id %s" % id
            else:
                return "%s record with the id %s was deleted successfully" % (str(result.deleted_count), id)
