from setup import *

# get doc by doc id
def get_info(id):
    info = participants.find_one(ObjectId(id))
    return str(info)

#create a new document in collection (specified as arg)
def create_doc(collection):
    collection = db[collection]
    new_doc = request.get_json()
    if collection == db.participants:
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

def update_doc(collection):
    collection = db[collection]
    update_info = request.get_json()
    update_info[0]['_id'] = ObjectId(update_info[0]['_id'])
    # return str(update_info[0])
    result = collection.update_one(update_info[0], update_info[1], False)
    return str(result.matched_count)
