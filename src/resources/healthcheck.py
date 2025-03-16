from flask_restx import Namespace, Resource

healthcheck_ns = Namespace('healthcheck')


@healthcheck_ns.route("/")
class HealthCheck(Resource):
    def get(self):
        return {'status': 'ok'}
