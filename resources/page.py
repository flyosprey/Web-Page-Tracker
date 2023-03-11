from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException

from custom_validators.link_validator import LinkValidator, UrlValidatorError
from schemas import PageRequestSchema, PageResponseSchema
from models import PageModel
from parsers import PageSpider, HeadersWithSchemas
from db import db

from loggers.page_logger import page_logger


Bip = Blueprint("page", __name__, description="Analyze of page")


@Bip.route("/pages")
class Page(MethodView):
    @Bip.arguments(PageRequestSchema)
    @Bip.response(200, PageResponseSchema)
    def post(self, payload):
        try:
            LinkValidator.normalize_url(payload["url"])
            spider = PageSpider(payload["url"], HeadersWithSchemas())
            result = spider.get_result()
            page_logger.info("Extracted result successfully!")
            model_result = PageModel(**result)
            db.session.add(model_result)
            db.session.commit()
            page_logger.info("Saved result into database!")

            return jsonify(result), 200
        except RequestException as error:
            page_logger.info(error)
            abort(404, message=str(error))
        except UrlValidatorError as error:
            page_logger.info(error)
            abort(400, message=str(error))
        except SQLAlchemyError as error:
            page_logger.info(error)
            abort(500, message="An error occurred while calculating the result!")

