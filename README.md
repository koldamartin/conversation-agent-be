# ABOUT
- Create a conversation chatbot with predefined answers easily, just change the `conversation_flow.json` file.

# RUN DEVELOPMENT
- Create a `.env` file as in `env_template`.
- Set `environment=development` and `port=5000`.
- Open the Docker desktop program.
- Type `docker compose up`.
- This will create two Docker images for a Flask application and PostgreSQL database.
- Send a PUT request on `http://localhost:5000/api/chat` with JSON body `{"query": "your_question"}`.

# RUN IN PRODUCTION
- Create a web service in Render.com.
- Set environment secrets.
- Set `environment=production` and `port=8080`.
- Set runtime to Docker.
- This will create a Gunicorn production server.
- Send a PUT request on `https://conversation-agent-be-new.onrender.com/api/chat` with JSON body `{"query": "your_question"}`. 
