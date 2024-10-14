from langchain.tools import StructuredTool
import json
import os

current_dir = os.path.dirname(__file__)
dialog_flow_path = os.path.join(current_dir, 'dialog_flow.json')


def create_tool(data):
    def get_answer(query: str) -> tuple[str, str]:
        return data['response'], data['end_flow']
    return StructuredTool.from_function(
        name=data['name'],
        func=get_answer,
        description=data['description'],
        return_direct=True
    )


def get_tools() -> list:
    with open(dialog_flow_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return [create_tool(row) for row in data]
