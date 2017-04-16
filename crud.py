from setup import *


def get_info(id):
    info = participants.find_one(ObjectId(id))
    return 'Here is info: %s' % info

#create a new document in collection (specified as arg)
def create_doc(collection):
    collection = db[collection]
    # pull in the data from request
    new_doc = request.get_json()
    # if date field exists, format as date
    try:
        new_doc["birthday"] = datetime.strptime(new_doc["birthday"], "%d/%m/%Y")
        new_doc["comp_date"] = datetime.strptime(new_doc["comp_date"], "%d/%m/%Y")
    except:
        pass
        
    try:
        new_id = collection.insert_one(new_doc).inserted_id
    except pymongo.errors.WriteError as error:
        #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
        logging.error(error)
        return "Failed to create a participant as one or more required fields were missing or incomplete"
    else:
        return str(new_id)
