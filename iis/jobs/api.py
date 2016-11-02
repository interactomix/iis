from flask_restful import Resource, Api


api = Api()


class Processes(Resource):
    def get(self):
        return {
           "processes": [
               {"id": "thing1", "name": "Thing1"},
               {"id": "thing2", "name": "Thing2"}
           ]
        }

api.add_resource(Processes, '/api/processes')