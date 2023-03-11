from flask import jsonify, abort
from flask.views import MethodView
from flask_smorest import Blueprint

from custom_validators import LinkValidator, DomainValidatorError
from parsers import DomainSpider, HeadersWithSchemas
from schemas import DomainRequestSchema, DomainResponseSchema
from loggers.domain_logger import domain_logger


Bip = Blueprint("domain", __name__, description="Analyze of domain")


@Bip.route("/stats")
class Domain(MethodView):
    @Bip.arguments(DomainRequestSchema)
    @Bip.response(200, DomainResponseSchema)
    def post(self, payload):
        try:
            domain = LinkValidator.normalize_domain(payload["domain"])
        except DomainValidatorError as error:
            domain_logger.info(error)
            abort(400, message=str(error))
        else:
            spider = DomainSpider(domain, HeadersWithSchemas())
            result = spider.get_result()
            domain_logger.info("Extracted result successfully")
            return jsonify(result), 200
