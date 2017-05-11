Setting Up Validation:
Validating that the data coming in to the collection is best done after you have set up a new collection, and can be run the command line. Validators are set using a dictionary with the validation requirements. More info in the MongoDB docs: https://docs.mongodb.com/manual/core/document-validation/
Pymongo uses the 'db.command' method (more info: http://api.mongodb.com/python/current/api/pymongo/database.html#pymongo.database.Database.command) to set validation which requires the creation of a sorted dict.
Because Python does not have a built-in sorted dict type that MongoDB requires, you will need to convert the dict to SON type using the bson class.
Example:
>>> import bson
>>> validator = bson.son.SON([("collMod", "test_collection"), ("validator", {"$or": [{"phone": {"$exists": True}}, {"email": {"$exists": True}}]} ),("validationLevel", "strict")])
>>> db.command(validator)
Note that the first key value pair in the list is the command to run (collMod) followed by the collection name (test_collection in this case), the second is the validation rules we want to enforce, and the third is the validation level. Note also that if the collection does not exist, Pymongo will throw an error.


_______notes_________
so the problem is that you're trying to enforce a structure that isn't going to work:
the whole benefit of the http verbs structure is that it allows for different use cases. you're trying to avoid passing variables to each of the different classes, when in fact if you instantiate with the bare minimum and pass variables from
there you'll have cleaner code. this won't require a huge refactor... try to make all the crazy cases in the http verb
functions and keep all the rest of the code generic.



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

current thinking on refactor:
Each of the http verbs will determine what method gets called inside of the requested collection. The url structure will be https://bouldercomp.com/api/v1/<collection>/
When the classes' methods are called they will do any necessary processing (at least finding the object id to be edited) and pass it to one of the four CRUD methods in the Crud class. That method will then return a JSON response telling the client whether there was a success or failure and any other relevant information.


To Do:
1)
-update and improve RequestHelper and general application flow
-test all current api functions

2)
-address fields have separate street, zip, etc
-have other user validate send
-function to pull down results for the comp
-add api versioning
-everything should be returned to the client as JSON
