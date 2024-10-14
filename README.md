# Conversation Agent
![Alt text](readme_image.jpg?raw=true "Title")
## ABOUT
- Create a conversation chatbot with predefined answers easily, just change the `conversation_flow.json` file.
- Custom alternative to IBM Watson assistant or RASA library with minimal learning curve.
  
## Tech Stack
- AI orchestrator: Langchain
- LLM: OpenAI API
- REST API: Flask, Flask-smorest
- Database: PostgreSQL database with Flask-SQLALchemy
- Docker and docker-compose 
- Dependencies management: Poetry
- Deployment: Gunicorn server on Render.com (free version, can take forever to load)

## RUN DEVELOPMENT
- Create a `.env` file as in `env_template`.
- Set `environment=development` and `port=5000`.
- Open the Docker desktop program.
- Type `docker compose up`.
- This will create two Docker images for a Flask application and PostgreSQL database.
- Send a POST request on `http://localhost:5000/api/chat` with JSON body `{"query": "your_question"}`.
- Swagger UI [here](http://localhost:5000/swagger-ui)
- check database by using pgAdmin

## RUN IN PRODUCTION
### Create a Render.com PostgreSQL database service
- Create a PostgreSQL database and get the database_name, username password and host_name

### Create a Render.com web service
- Create a web service in Render.com.
- Set environment secrets with the variables obtained from PostgreSQL db.
- Set `environment=production` and `port=10000`.
- Set runtime to Docker.
- This will create a Gunicorn production server with 4 workers.
- Send a POST request on `https://conversation-agent.onrender.com/api/chat` with JSON body `{"query": "your_question"}`.
- Swagger UI [here](https://conversation-agent.onrender.com/swagger-ui)
