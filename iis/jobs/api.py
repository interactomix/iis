from flask_restful import Resource, Api


api = Api()


class Processes(Resource):
    def get(self):
        return {
           "processes": [
               {
                   "id": "thing1",
                   "name": "Thing1",
                   "postset": ["thing2", "thing4"]
               },
               {
                   "id": "thing2",
                   "name": "Thing2",
                   "postset": ["thing5, thing6"]
               },
               {
                   "id": "thing3",
                   "name": "Thing3",
                   "postset": ["thing2", "thing1"]
               },
               {
                   "id": "thing4",
                   "name": "Thing4",
                   "postset": ["thing2", "thing5", "thing6"]
               },
               {
                   "id": "thing5",
                   "name": "Thing5",
                   "postset": ["thing1", "thing2", "thing6"]
               },
               {
                   "id": "thing6",
                   "name": "Thing6",
                   "postset": ["thing5", "thing3"]
               }
           ]
        }

api.add_resource(Processes, '/api/processes')