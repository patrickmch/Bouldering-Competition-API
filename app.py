from setup import *
from crud import *
from user import User
from user_api import UserAPI

app = Flask(__name__)
login_manager.init_app(app)
app.secret_key = '\xec0\xea\xccD\xd3\x03\x87\xf4K1A\xeb?$*\x0cN\xb5I\xf1\x02\xb3\x13'


@login_manager.user_loader
def load_user(user_id):
    user = User(participants.find_one({'_id' : ObjectId(user_id)}))
    return user

#url rules
@app.route('/api/login/', methods = generic_methods)
def login():
    auth = request.authorization
    user_data = participants.find_one({'email' : auth['username']})
    if pwd_encrypt.verify(req['password'], user_data['password']):
        user = User(user_data)
        login_user(user)
        return str(user.get_id())
    else:
        return 'incorrect password for email %s' % auth['username']

@app.route('/api/logout/', methods = generic_methods)
def logout():
    logout_user()
    return 'logged out'

# POST creates a user and therefore does not require login
app.add_url_rule('/api/users/', view_func = UserAPI.as_view('users'), methods= ['POST'])
app.add_url_rule('/api/users/', view_func = login_required(UserAPI.as_view('users')), methods= ['GET', 'PUT', 'DELETE'])
app.add_url_rule('/api/competitions/', view_func = login_required(UserAPI.as_view('competitions')), methods= ['GET', 'POST', 'PUT', 'DELETE'])
app.add_url_rule('/api/venues/', view_func = login_required(UserAPI.as_view('venues')), methods= ['GET', 'POST', 'PUT', 'DELETE'])
