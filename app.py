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
    #use the user_auth class to authenticate the user
    ua = UserAuth(user)
    ua.authenticate_user()
    return user

def instantiate_req(func):
    # wraps response function so as to instantiate the RequestHelper class
    def wrapper():
        g.req = RequestHelper()
        return func()
    return wrapper


#url rules:
app.add_url_rule('/api/logout/', 'logout', UserAuth.logout)
app.add_url_rule('/api/login/', 'login', UserAuth.login)

# POST creates a user and therefore does not require login:
app.add_url_rule('/api/participants/', view_func = instantiate_req(UserAPI.as_view('new_user')), methods= ['POST'])
# all other methods require login:
app.add_url_rule('/api/participants/', view_func = instantiate_req(login_required(UserAPI.as_view('users'))), methods= ['GET', 'PUT', 'DELETE'])
app.add_url_rule('/api/competitions/', view_func = instantiate_req(login_required(CompAPI.as_view('competitions'))), methods= all_methods)
app.add_url_rule('/api/venues/', view_func = instantiate_req(login_required(VenueAPI.as_view('venues'))), methods= all_methods)
