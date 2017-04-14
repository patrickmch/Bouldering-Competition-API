from setup import *


def get_info(id):
    info = posts.find_one(ObjectId(id))
    return 'Here is info: %s' % info

def create_participant():
    new_participant = request.get_json()
    # format date
    new_participant["birthday"] = datetime.strptime(new_participant["birthday"], "%d/%m/%Y").isoformat()
    try:
        new_id = posts.insert_one(new_participant).inserted_id
    except pymongo.errors.WriteError as error:
        #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
        logging.error(error)
        return "Failed to create a participant as one or more required fields were missing or incomplete"
    else:
        return str(new_id)
