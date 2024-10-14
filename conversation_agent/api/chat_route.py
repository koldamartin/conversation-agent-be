import os
from flask_smorest import Blueprint, abort
from flask import session, jsonify
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
    def post(self, json_body):
        """Load the current session ID and latest chat history,
        generate response based on conversation flow schema
        and save to database.
        """
        try:
            current_user_id = self.get_current_user_id()
            chat_history = self.get_chat_history(current_user_id)
            response, end_flow = self.generate_response(json_body["query"], chat_history)
            self.save_conversation(current_user_id, json_body["query"], response, end_flow)
            return {"result": response}

        except KeyError as e:
            abort(400, message=f"Missing required key: {json_body}. Details: {e}")
        except BadRequest as e:
            abort(400, message=f"Bad Request. Details: {e}")
        except RequestEntityTooLarge as e:
            abort(413, message=f"Payload Too Large. Details: {e}")
        except Exception as e:
            abort(500, message=f"Internal Server Error. Details:{e}")

    def get_current_user_id(self):
        return session.get("session_id")

    def get_chat_history(self, user_id):
        recent_query = db.session.query(ConversationModel) \
            .filter(ConversationModel.user_id == user_id) \
            .order_by(desc(ConversationModel.timestamp)) \
            .first()
        if recent_query:
            chat_history = [recent_query.query, recent_query.answer]
            if recent_query.end_flow == 'Yes':
                chat_history.clear()
        else:
            chat_history = []
        return chat_history

    def generate_response(self, query, chat_history):
        # This is a placeholder for your actual response generation logic
        return generate_response(query, chat_history)

    def save_conversation(self, user_id, query, response, end_flow):
        new_entry = ConversationModel(user_id=user_id,
                                      query=query,
                                      answer=response,
                                      end_flow=end_flow)
        db.session.add(new_entry)
        db.session.commit()
