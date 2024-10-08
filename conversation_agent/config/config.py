from dotenv import load_dotenv
import os

load_dotenv()

environment = os.getenv("ENVIRONMENT")
port = os.getenv("PORT")
openai_api_key = os.getenv("OPENAI_API_KEY")
llm_model = os.getenv("LLM")

if not environment:
    raise EnvironmentError("ENVIRONMENT must be set", 401)
if not port:
    raise EnvironmentError("PORT must be set", 401)
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY must be set", 401)
if not llm_model:
    raise EnvironmentError("LLM must be set", 401)
