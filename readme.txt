Setting Up Validation:
Validating that the data coming in to the collection is best done after you have set up a new collection, and can be run the command line. Validators are set using a dictionary with the validation requirements. More info in the MongoDB docs: https://docs.mongodb.com/manual/core/document-validation/
Pymongo uses the 'db.command' method (more info: http://api.mongodb.com/python/current/api/pymongo/database.html#pymongo.database.Database.command) to set validation which requires the creation of a sorted dict.
Because Python does not have a built-in sorted dict type that MongoDB requires, you will need to convert the dict to SON type using the bson class.
Example:
>>> import bson
>>> validator = bson.son.SON([("collMod", "test_collection"), ("validator", {"$or": [{"phone": {"$exists": True}}, {"email": {"$exists": True}}]} ),("validationLevel", "strict")])
>>> db.command(validator)
Note that the first key value pair in the list is the command to run (collMod) followed by the collection name (test_collection in this case), the second is the validation rules we want to enforce, and the third is the validation level. Note also that if the collection does not exist, Pymongo will throw an error.


Possible Collection Structure:
1)
-participants
  fname, lname, birthday, sex, email, password

-venue
  name, address, competitions
  -competitions
    name, participant_ids
    -routes
       name, grade
        -sends
          participant_id, comp_id

2)
-participants
  fname, lname, birthday, sex, email, password
  -sends
    route_id

-venue
  name, address, competitions
  -competitions
    name, participant_ids
    -routes
      name, grade, attempts

3) *best
-participants
  fname, lname, birthday, sex, email, password
  -sends
    route_id, attempts

-venue
  name, address, competition_id

-competitions
  name, participant_ids, venue_id
    -routes
      name, grade, points

4)
-participants
  fname, lname, birthday, sex, email, password
  -sends
    route_id, attempts

-competitions
  name, participant_ids, venue_ids
  -venue
    name, address, competitions
    -routes
      name, grade, points
