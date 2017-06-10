from setup import *
from crud import *
from user import User
from user_api import UserAPI
from competitions_api import CompAPI
from venue_api import VenueAPI
from user_auth import UserAuth
from request_helper import RequestHelper
from response_handler import create_response, ErrorResponse
from functools import wraps
import flask_login

app = Flask(__name__)
login_manager.init_app(app)
app.secret_key = '\xec0\xea\xccD\xd3\x03\x87\xf4K1A\xeb?$*\x0cN\xb5I\xf1\x02\xb3\x13'
_methods = ['GET', 'PUT', 'DELETE']

@login_manager.user_loader
def load_user(user_id):
    user = User(db.participants.find_one({'_id' : ObjectId(user_id)}))
    try:
        #if the request class exists use the user_auth class to authenticate the user
        ua = UserAuth(user)
        ua.authenticate_user()
    except AttributeError:
        pass
    return user

@app.errorhandler(ErrorResponse)
def handle_error(error):
    response = jsonify(error.to_dict())
    return response

def instantiate_classes(func):
    # wraps response function so as to instantiate the RequestHelper class
    def wrapper(**kwargs):
        #TODO renaming this with a lowdash could be nice...
        g.req = RequestHelper(**kwargs)
        return func()
    # rename the wrapper function to the function name to avoid AssertionError:
    wrapper.func_name = func.func_name
    return wrapper


#url rules:
app.add_url_rule('/api/logout/', 'logout', UserAuth.logout)
app.add_url_rule('/api/login/', 'login', UserAuth.login)

# users:
# posting to user creates a user and therefore does not require login:
app.add_url_rule('/api/participants/', view_func = instantiate_classes(UserAPI.as_view('new_user')), methods= ['POST'])
# all other methods require login:
app.add_url_rule('/api/participants/<string:email>/', view_func = instantiate_classes(flask_login.login_required(UserAPI.as_view('users'))), methods= _methods)

# venues
app.add_url_rule('/api/competitions/<string:_id>/', view_func = instantiate_classes(flask_login.login_required(CompAPI.as_view('competitions'))), methods= _methods)
app.add_url_rule('/api/competitions/', view_func = instantiate_classes(flask_login.login_required(CompAPI.as_view('new_comp'))), methods= ['POST'])

# comps
app.add_url_rule('/api/venues/', view_func = instantiate_classes(flask_login.login_required(VenueAPI.as_view('new_venue'))), methods= ['POST'])
app.add_url_rule('/api/venues/<string:_id>/', view_func = instantiate_classes(flask_login.login_required(VenueAPI.as_view('venues'))), methods= _methods)
