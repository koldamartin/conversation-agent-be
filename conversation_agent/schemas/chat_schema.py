from marshmallow import Schema, fields


class MessageSchema(Schema):
    query = fields.String(required=True)


class MessageResponseSchema(Schema):
    result = fields.String()
