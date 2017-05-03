from setup import *

class Req:

    def __init__(self, request):
        self.req = request
        self.req_id = None

    def get_req_id(self):
        return self.req_id

    def set_req_id(self, collection):
        default = 0
        for k,v in self.req.items():
            if k == 'email':
                obj = collection.find_one({'email' : v})
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
