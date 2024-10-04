from langchain.tools import StructuredTool
import json
import os

current_dir = os.path.dirname(__file__)
dialog_flow_path = os.path.join(current_dir, 'dialog_flow.json')

def manage_history(history, query, response, end_flow):
    if end_flow == 'Yes':
        history.clear()
    else:
        history.extend((query, response))


def create_tool(data, history):
    def get_answer(query: str) -> str:
        manage_history(history, query, data['response'], data['end_flow'])
        return data['response']
    return StructuredTool.from_function(
        name=data['name'],
        func=get_answer,
        description=data['description'],
        return_direct=True
    )


def get_tools(history) -> list:
    with open(dialog_flow_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return [create_tool(row, history) for row in data]
