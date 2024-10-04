from langchain_openai import ChatOpenAI

from conversation_agent.config.config import openai_api_key, llm_model

llm = ChatOpenAI(model=llm_model,
                 temperature=0,
                 openai_api_key=openai_api_key)