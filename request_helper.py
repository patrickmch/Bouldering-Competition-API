from setup import *

class RequestHelper:

    def __init__(self):
        self.collection_name = request.path.split('/')[2]
        self.collection = db[self.collection_name]
        self.req = request.get_json()
        self.req_id = self.set_req_id()
        self.auth = request.authorization

    def get_collection_name(self):
        return self.collection_name

    def api_key(self):
        return request.headers['Api-Key']

    def auth(self):
        return self.auth

    def get_collection(self):
        return self.collection

    def get_req(self):
        return self.req

    def get_item(self, item):
        try:
            return self.req[item]
        except:
            return "no item found"

    def get_req_id(self):
        return self.req_id

    def set_item(self, key, val):
        self.req[key] = val
        return True

    def set_date(self, field_name):
        self.set_item(field_name, datetime.strptime(self.get_item(field_name), "%d/%m/%Y"))

    def set_req_id(self):
        default = 0
        for k,v in self.req.items():
            if k == 'email':
                obj = self.collection.find_one({'email' : v})
                try:
                    self.req_id = obj.get('_id')
                except:
                    self.req_id = default
                break
            elif k == '_id':
                try:
                    self.req_id = v
                except:
                    self.req_id = default
                break

        return self.req_id
