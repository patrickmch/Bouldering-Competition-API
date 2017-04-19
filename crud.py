from setup import *

# get doc by doc id
def find_doc(collection_name, id):
    collection = db[collection_name]
    info = collection.find_one(ObjectId(id))
    return str(info)

#create a new document in the collection specified in url
def create_doc(collection_name):
    collection = db[collection_name]
    new_doc = request.get_json()
    if collection == db.participants:
        # check to make sure user does not already have an account
        query = collection.find({"email" : new_doc["email"]})
        if query.count() > 0:
            return "The email you provided is already in use."
        new_doc["birthday"] = datetime.strptime(new_doc["birthday"], "%d/%m/%Y")
    elif collection == db.competitions:
        new_doc["comp_date"] = datetime.strptime(new_doc["comp_date"], "%d/%m/%Y")
        new_doc["venue_id"] = ObjectId(new_doc["venue_id"])
    try:
        new_id = collection.insert_one(new_doc).inserted_id
    except pymongo.errors.WriteError as error:
        #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
        logging.error(error)
        return "Failed to create a participant as one or more required fields were missing or incomplete"
    else:
        return str(new_id)

#update a new document in the collection specified in url
def update_doc(collection_name):
    collection = db[collection_name]
    update_info = request.get_json()

    try:
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

# TODO put the decorator in app.py/ move the routes over to other style and test this code
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        app_key = ObjectId(kwargs.get("id"))
        result = db.participants.find_one({"_id" : ObjectId(app_key)})
        if result["_id"] == app_key:
            return str(kwargs)
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
