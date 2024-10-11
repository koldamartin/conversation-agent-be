import os
from flask_smorest import Blueprint, abort
from flask import session
from flask.views import MethodView
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
import logging
from sqlalchemy import desc

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
            # Get the user id from the session
            current_user_id = session.get("session_id")

            # Get the latest chat history for the same session
            recent_query = db.session.query(ConversationModel) \
                .filter(ConversationModel.user_id == current_user_id) \
                .order_by(desc(ConversationModel.timestamp)) \
                .first()
            if recent_query:
                chat_history = [recent_query.query, recent_query.answer]
                # If it is dialog end, clear the chat history
                if recent_query.end_flow == 'Yes':
                    chat_history.clear()
            else:
                chat_history = []

            # Generate the response
            result = generate_response(json_body["query"], chat_history)
            # Add new entry to db
            new_entry = ConversationModel(user_id=current_user_id,
                                          query=json_body["query"],
                                          answer=result[0],
                                          end_flow=result[1])
            db.session.add(new_entry)
            db.session.commit()
            return {"result": result[0]}

        except KeyError as e:
            abort(400, message=f"Missing required key: {json_body}. Details: {e}")
        except BadRequest as e:
            abort(400, message=f"Bad Request. Details: {e}")
        except RequestEntityTooLarge as e:
            abort(413, message=f"Payload Too Large. Details: {e}")
        except Exception as e:
            abort(500, message=f"Internal Server Error. Details:{e}")
