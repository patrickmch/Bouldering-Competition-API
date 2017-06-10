Setting Up Validation:
Validating that the data coming in to the collection is best done after you have set up a new collection, and can be run the command line. Validators are set using a dictionary with the validation requirements. More info in the MongoDB docs: https://docs.mongodb.com/manual/core/document-validation/
Pymongo uses the 'db.command' method (more info: http://api.mongodb.com/python/current/api/pymongo/database.html#pymongo.database.Database.command) to set validation which requires the creation of a sorted dict.
Because Python does not have a built-in sorted dict type that MongoDB requires, you will need to convert the dict to SON type using the bson class.
Example:
>>> import bson
>>> validator = bson.son.SON([("collMod", "test_collection"), ("validator", {"$or": [{"phone": {"$exists": True}}, {"email": {"$exists": True}}]} ),("validationLevel", "strict")])
>>> db.command(validator)
Note that the first key value pair in the list is the command to run (collMod) followed by the collection name (test_collection in this case), the second is the validation rules we want to enforce, and the third is the validation level.

API usage:
The API works by searching three different collections (users, competitions, and venues) in the url string, and then using the http verb (POST, GET, PUT, DELETE) to handle your specific request. Most http method/collection combinations require you to send an api_key in the header with your request and require you to have logged in (done by sending your email and password to /api/login via header authentication). The only exception to this is POSTing to users as that creates a user, and returns an api_key, which that user can then use for all future requests.
GET, PUT or DELETE requests all require you to send an identifier for the database object you want to reference (e.g. api/venues/<identifier>/). In the case of users, it will be an email address; competitions and venues both require a comp or venue id respectively.



successful create doc
{
  "_id" : <string>,
  "response_code" : 200
}
successful update, delete
{
  "response_code" : 200
}
successful find
{
  "response_code" : 200,
  "data" : [...]
}
unauthorized
{
  "response_code" :401
}
unauthenticated
{
  "response_code" :403
}
not found
{
  "response_code" : 404
}




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
-users should be renamed users
-have a function to return a multiple matched values from a basic search (e.g. a bunch of comps)
-implement this mongokit: http://flask.pocoo.org/docs/0.12/patterns/mongokit/
-foreign key constraint on venue_id in competitions
-address fields have separate street, zip, etc
-have other user validate send
-function to pull down results for the comp
-add api versioning
