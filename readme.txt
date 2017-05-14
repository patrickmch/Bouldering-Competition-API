Setting Up Validation:
Validating that the data coming in to the collection is best done after you have set up a new collection, and can be run the command line. Validators are set using a dictionary with the validation requirements. More info in the MongoDB docs: https://docs.mongodb.com/manual/core/document-validation/
Pymongo uses the 'db.command' method (more info: http://api.mongodb.com/python/current/api/pymongo/database.html#pymongo.database.Database.command) to set validation which requires the creation of a sorted dict.
Because Python does not have a built-in sorted dict type that MongoDB requires, you will need to convert the dict to SON type using the bson class.
Example:
>>> import bson
>>> validator = bson.son.SON([("collMod", "test_collection"), ("validator", {"$or": [{"phone": {"$exists": True}}, {"email": {"$exists": True}}]} ),("validationLevel", "strict")])
>>> db.command(validator)
Note that the first key value pair in the list is the command to run (collMod) followed by the collection name (test_collection in this case), the second is the validation rules we want to enforce, and the third is the validation level. Note also that if the collection does not exist, Pymongo will throw an error.



Collection Schema:

-users
  fname, lname, birthday, sex, email, password
  -sends
    route_id, attempts, validated_by
  -role

-venue
  name, address, competition_ids

-competitions
  name, participant_ids, venue_ids
    -routes
      _id, name, grade, points


To Do:
-everything should be returned to the client as JSON
-clean up imports
-better error handling
-foreign key constraint on venue_id in competitions
-address fields have separate street, zip, etc
-have other user validate send
-function to pull down results for the comp
-add api versioning
