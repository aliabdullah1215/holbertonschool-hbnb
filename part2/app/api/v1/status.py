from flask_restx import Namespace, Resource

status_ns = Namespace("status", description="API status")

@status_ns.route("/")
class StatusResource(Resource):
    def get(self):
        return {"status": "OK"}, 200
