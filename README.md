# ABOUT
- Create a conversation chatbot with predefined answers easily, just change the conversation_flow.json file

# RUN DEVELOPMENT
- Create .env file as in env_template
- Set environment=development and port=5000
- type <docker compose up>
- This will create two docker images for a flask application and postgreSQL database
- Send a PUT request on <http://localhost:5000/api/chat> with json body {"query": "your_question"}

# RUN IN PRODUCTION
- create a web service in render.com
- set environment secrets
- development=production and port=8080
- set runtime to Docker
- This will create a Gunicorn production server
- Send a PUT request on <https://conversation-agent-be-new.onrender.com/api/chat> with json body {"query": "your_question"}
