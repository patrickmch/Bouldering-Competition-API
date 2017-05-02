from setup import *

class User:
    def __init__(self, dic):
        self.vars = dic

    def get_var(self, var):
        return self.vars.get(var)

    # necessary for flask_login
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.vars.get("_id"))

    def is_authenticated(self):
        return True
