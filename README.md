# Conversation Agent
## ABOUT
- Create a conversation chatbot with predefined answers easily, just change the `conversation_flow.json` file.
  
## Tech Stack
- AI orchestrator: Langchain
- LLM: OpenAI API
- REST API: Flask, Flask-smorest
- Database: PostgreSQL database with Flask-SQLALchemy
- Conteinarization: Docker and docker-compose 
- Dependencies management: Poetry
- Deployment: Gunicorn server on Render.com


## RUN DEVELOPMENT
- Create a `.env` file as in `env_template`.
- Set `environment=development` and `port=5000`.
- Open the Docker desktop program.
- Type `docker compose up`.
- This will create two Docker images for a Flask application and PostgreSQL database.
- Send a PUT request on `http://localhost:5000/api/chat` with JSON body `{"query": "your_question"}`.

## RUN IN PRODUCTION
### Create a Render.com PostgreSQL database service
- Create a PostgreSQL database and get the database_name, username password and host_name

### Create a Render.com web service
- Create a web service in Render.com.
- Set environment secrets with the variables obtained from PostgreSQL db.
- Set `environment=production` and `port=8080`.
- Set runtime to Docker.
- This will create a Gunicorn production server with 4 workers.
- Send a PUT request on `https://conversation-agent-be-new.onrender.com/api/chat` with JSON body `{"query": "your_question"}`.



