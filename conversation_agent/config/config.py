from dotenv import load_dotenv
import os
import uuid

load_dotenv()

environment = os.getenv("ENVIRONMENT")
port = os.getenv("PORT")
openai_api_key = os.getenv("OPENAI_API_KEY")
llm_model = os.getenv("LLM")
db_name = os.getenv("POSTGRES_NAME")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_user = os.getenv("POSTGRES_USER")
app_secret_key = os.getenv("APP_SECRET_KEY")

if not environment:
    raise EnvironmentError("ENVIRONMENT must be set", 401)
if not port:
    raise EnvironmentError("PORT must be set", 401)
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY must be set", 401)
if not llm_model:
    raise EnvironmentError("LLM must be set", 401)
