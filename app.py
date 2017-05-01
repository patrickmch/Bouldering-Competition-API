from setup import *
from crud import *
from handle_request import *
from user import User
from user_api import UserAPI

app = Flask(__name__)
login_manager.init_app(app)
app.secret_key = '\xec0\xea\xccD\xd3\x03\x87\xf4K1A\xeb?$*\x0cN\xb5I\xf1\x02\xb3\x13'
# create variable/function with generic info to keep the code DRY
# all urls take function to call, and (with the exception of create_user) take an id (used as api_key) and the
# collection_name of collection to be modified
generic_methods = ["GET", "POST"]

def url_string(func_to_call):
    return '/api/%s/<string:id>/<string:collection_name>/' % func_to_call

@login_manager.user_loader
def load_user(user_id):
    user = User(participants.find_one({"_id" : ObjectId(user_id)}))
    return user

#url rules
@app.route('/api/login/', methods = generic_methods)
def login():
    req = request.authorization
    user_data = participants.find_one({"email" : req["username"]})
    if pwd_encrypt.verify(req["password"], user_data["password"]):
        user = User(user_data)
        login_user(user)
        return str(user.get_id())
    else:
        return "incorrect password for email %s" % req["username"]

@app.route('/api/logout/', methods = generic_methods)
def logout():
    logout_user()
    return "logged out"


app.add_url_rule('/api/users/', view_func = UserAPI.as_view('users'), methods= ['GET',])
# @app.route('api/users/', view_func = UserAPI.as_view('users'), methods= ['GET',])
# @handle_request
# def read(**kwargs):
#     new_search = Crud(**kwargs)
#     return new_search.find_doc()

# @app.route(url_string('update_doc'), methods= generic_methods)
# @login_required
# @handle_request
# def update(**kwargs):
#     update = Crud(**kwargs)
#     return update.update_doc()
#
# @app.route(url_string('delete_doc'), methods= generic_methods)
# @handle_request
# def delete(**kwargs):
#     delete = Crud(**kwargs)
#     return delete.delete_doc()
