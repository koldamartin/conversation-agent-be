import os

from flask_smorest import Blueprint, abort
from flask import session
from flask.views import MethodView
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
import logging
import uuid

from conversation_agent.schemas.chat_schema import MessageSchema, MessageResponseSchema
from conversation_agent.services.conversation_service import generate_response
from conversation_agent.dbmodels.conversation import ConversationModel
from conversation_agent.db import db



blp = Blueprint("chat_route", __name__, url_prefix="/api/chat")


@blp.route("/")
class ChatRoute(MethodView):
    @blp.arguments(MessageSchema)
    @blp.response(200, MessageResponseSchema)
    def put(self, json_body):
        try:
            result = generate_response(json_body["query"])
            # Step 1: Load chat history from the database for the user_id
            #user_id = os.getenv("SESSION_ID")
            user_id = session.get("SESSION_ID")
            #chat_history_records = db.session.query(ConversationModel).filter_by(user_id=user_id).all()

            # Step 3: Extract the answer from the result
            answer = result
            #chat_history = [{"query": record.query, "answer": record.answer} for record in chat_history_records]

            # Step 4: Store the query and answer in the database
            new_entry = ConversationModel(user_id=user_id,
                                          query=json_body["query"],
                                          answer=answer)
            logging.info(f"New entry created: {new_entry}")
            db.session.add(new_entry)
            logging.info(f"New entry added to db: {new_entry}")
            db.session.commit()
            logging.info(f"Data saved to db: user_id={user_id}")
            return {"result": result}

        except KeyError as e:
            abort(400, message=f"Missing required key: {json_body}. Details: {e}")
        except BadRequest as e:
            abort(400, message=f"Bad Request. Details: {e}")
        except RequestEntityTooLarge as e:
            abort(413, message=f"Payload Too Large. Details: {e}")
        except Exception as e:
            abort(500, message=f"Internal Server Error. Details:{e}")
