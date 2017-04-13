from setup import *


def get_info(id):
    info = posts.find_one(ObjectId(id))
    return 'Here is info: %s' % info

def create_participant():
    req = request.get_json()
    # json_string = json.loads(str(req))
    # new_participant ={}
    # return str(req)
    # for k, v in req.iteritem():
    #     if (k == "date"):
    #         v = ISODate(v)
    #     new_participant = {k:v}
    # pprint(new_participant)
    try:
        new_id = posts.insert_one(req).inserted_id
    except pymongo.errors.WriteError as error:
        #more detailed exceptions (eg. what fields were not filled out) are not possible with current Mongo validation
        logging.error(error)
        return "Failed to create a participant as one or more required fields were missing or incomplete"
    else:
        return str(new_id)
