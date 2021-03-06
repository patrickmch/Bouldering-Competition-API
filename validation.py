# function to validate collection information
def collection_validation(collection_name, validation_dict, validation_level):
    # convert python dict to sorted dict type using bson's SON method: first item in the list is the command we want to use with the collection name; next is the validation dictionary; next is the validation level
    validator = bson.son.SON([("collMod", collection_name),
    ("validator", validation_dict),
    ("validationLevel", validation_level)])
    # pass sorted dict to Mongo's command method
    db.command(validator)
    print    "Validation Successful"

# validation dictionaries: these determine what data MongoDB allow to be stored in each collection.

#this is a regex to enforce the storage of valid emails
email_regex = {"$regex": "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"}

users_validation = {
    "$and" :
    [
        {"fname" : {"$type" : "string"}},
        {"lname" : {"$type" : "string"}},
        {"birthday" : {"$exists" : "true"}},
        {"sex" : {"$in" : ["m", "f"]}},
        {"email" : email_regex},
    ]
}

venue_validation = {
    "$and" :
    [
        {"venue_name": {"$type" : "string"}},
        {"venue_address" : {"$type" : "string"}},
        {"venue_email" : email_regex}
    ]
}

competition_validation = {
    "$and" :
    [
        {"comp_name" : {"$type" : "string"}},
        {"comp_date" : {"$exists" : "true"}},
        {"venue_id" : {"$exists" : "true"}}
    ]
}
# collection_validation("competitions", competition_validation, "strict")
