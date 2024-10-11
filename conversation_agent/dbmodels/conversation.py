from conversation_agent.db import db


class ConversationModel(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    query = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
