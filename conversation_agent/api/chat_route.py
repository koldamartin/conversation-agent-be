from flask_smorest import Blueprint, abort
from flask.views import MethodView
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge

from conversation_agent.schemas.chat_schema import MessageSchema, MessageResponseSchema
from conversation_agent.services.conversation_service import generate_response

blp = Blueprint("chat_route", __name__, url_prefix="/api/chat")


@blp.route("/")
class ChatRoute(MethodView):
    @blp.arguments(MessageSchema)
    @blp.response(200, MessageResponseSchema)
    def put(self, json_body):
        try:
            result = generate_response(json_body["query"])
            return {"result": result}
        except KeyError as e:
            abort(400, message=f"Missing required key: {json_body}. Details: {e}")
        except BadRequest as e:
            abort(400, message=f"Bad Request. Details: {e}")
        except RequestEntityTooLarge as e:
            abort(413, message=f"Payload Too Large. Details: {e}")
        except Exception as e:
            abort(500, message=f"Internal Server Error. Details:{e}")
