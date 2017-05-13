from setup import *
from crud import *
from user import User
from user_api import UserAPI
from competitions_api import CompAPI
from venue_api import VenueAPI
from user_auth import UserAuth
from request_helper import RequestHelper

app = Flask(__name__)
login_manager.init_app(app)
app.secret_key = '\xec0\xea\xccD\xd3\x03\x87\xf4K1A\xeb?$*\x0cN\xb5I\xf1\x02\xb3\x13'
all_methods = ['GET', 'POST', 'PUT', 'DELETE']

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

def instantiate_req(func):
    # wraps response function so as to instantiate the RequestHelper class
    def wrapper(**kwargs):
        g.req = RequestHelper(**kwargs)
        return func()
    # rename the wrapper function to the function name to avoid AssertionError:
    wrapper.func_name = func.func_name
    return wrapper


#url rules:
app.add_url_rule('/api/logout/', 'logout', UserAuth.logout)
app.add_url_rule('/api/login/', 'login', UserAuth.login)

# POST creates a user and therefore does not require login:
app.add_url_rule('/api/participants/', view_func = instantiate_req(UserAPI.as_view('new_user')), methods= ['POST'])
# all other methods require login:
app.add_url_rule('/api/participants/<string:email>/', view_func = instantiate_req(login_required(UserAPI.as_view('users'))), methods= ['GET', 'PUT', 'DELETE'])
app.add_url_rule('/api/competitions/<string:_id>/', view_func = instantiate_req(login_required(CompAPI.as_view('competitions'))), methods= all_methods)
app.add_url_rule('/api/venues/', view_func = instantiate_req(login_required(VenueAPI.as_view('new_venue'))), methods= ['POST'])
app.add_url_rule('/api/venues/<string:_id>/', view_func = instantiate_req(login_required(VenueAPI.as_view('venues'))), methods= all_methods)
