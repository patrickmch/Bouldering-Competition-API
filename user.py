class User:
    def __init__(self, data):
        self.data = data

    def get_var(self, var):
        return self.data.get(var)

    # necessary for flask_login
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.data.get('_id'))

    def is_authenticated(self):
        return True
