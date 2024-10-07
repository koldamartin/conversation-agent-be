from flask import Flask, request, Response
from flask_smorest import Api

from conversation_agent.config.config import environment, port
from conversation_agent.api.chat_route import blp as MessageBlueprint

app = Flask(__name__)
app.config["API_TITLE"] = "Message API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024  # 6 kB

api = Api(app)
api.register_blueprint(MessageBlueprint)


def main():
    if environment == "production":
        app.run(host="0.0.0.0", port=port)
    elif environment == "development":
        app.run(host="0.0.0.0", debug=True, port=port)
    else:
        raise ValueError("Invalid environment")


if __name__ == "__main__":
    main()

# TODO 1 - convert tools.xlsx to dialog_flow.json or tools.yaml -> Done
# TODO 2 - add saving data into sql database
# TODO 3 - add loading chat history from the same database
# TODO 4 - add buttons to each answer, will be part of the json output along with the response
# TODO 5 - divide files to correct directories -> Done
# TODO 6 - use flask smorest for exceptions, blueprints etc. -> Done

