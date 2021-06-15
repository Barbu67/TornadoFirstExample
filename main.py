import os
from tornado import ioloop,web
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId

MONGODB_DB_URL = os.environ.get('OPENSHIFT_MONGODB_DB_URL') if os.environ.get('OPENSHIFT_MONGODB_DB_URL') else 'mongodb://localhost:27017/'
MONGODB_DB_NAME = os.environ.get('OPENSHIFT_APP_NAME') if os.environ.get('OPENSHIFT_APP_NAME') else 'evc'

client = MongoClient(MONGODB_DB_URL)
db = client[MONGODB_DB_NAME]

class IndexHandler(web.RequestHandler):
    def get(self):
        self.write("Tornado WebServer is running on the Mystery Machine")

    def write_error(self, status_code, **kwargs):
        self.write("Ooops! You caused a %d error." % status_code)


class EvcConfigurationsHandler(web.RequestHandler):
    def get(self):
        evcconfigurations = db.evcconfigurations.find()
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(list(evcconfigurations),default=json_util.default))

    #@tornado.web.authenticated
    def post(self):
        evcconfiguration_data = json.loads(self.request.body)
        evcconfiguration_id = db.evcconfigurations.insert_one(evcconfiguration_data)
        print('evcconfiguration created with id ' + str(evcconfiguration_id))
        self.set_header("Content-Type", "application/json")
        self.set_status(201)

    def write_error(self, status_code, **kwargs):
        self.write("Ooops! You caused a %d error." % status_code)


class EvcConfigurationHandler(web.RequestHandler):
    def get(self , evcconfiguration_id):
        evcconfiguration = db.evcconfigurations.find_one({"_id":ObjectId(str(evcconfiguration_id))})
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps((evcconfiguration),default=json_util.default))

    def write_error(self, status_code, **kwargs):
        self.write("Ooops! You caused a %d error." % status_code)

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug" : True,
    "autoreload" : True
}

application = web.Application([
    (r'/', IndexHandler),
    (r'/index', IndexHandler),
    (r'/api/v1/evcconfigurations',EvcConfigurationsHandler),
    (r'/api/v1/evcconfigurations/(.*)', EvcConfigurationHandler)
],**settings)

if __name__ == "__main__":
    application.listen(8888)
    ioloop.IOLoop.instance().start()