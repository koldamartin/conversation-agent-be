from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from conversation_agent.tools.tool_loader import get_tools
from conversation_agent.services.llm_service import llm

chat_history = []
tools = get_tools(chat_history)


system_prompt = """
As an AI assistant, it is your job to provide a response to the user's query, utilizing only the tools provided {tools}. 
Your response must be the provided tool's output.
You must NOT generate any text. Only respond with the text string provided in the tools.
Always strictly follow the description of the tool. If you don't follow it, you will be penalized.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

agent = create_openai_functions_agent(llm, tools, prompt)
final_agent = AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True, max_iterations=3)


# def generate_response(history, query):
def generate_response(query: str) -> str:
    result = final_agent.invoke({'input': query, 'tools': tools, 'chat_history': chat_history})
    print(result)
    return result['output']


# while True:
#     user_query = input("User: ")
#     response = final_agent.invoke({'input': user_query, 'tools': tools, 'chat_history': chat_history})
#     print(f"AI: {response['output']}")
#     if user_query == "exit":
#         print("Exiting...")
#         break
