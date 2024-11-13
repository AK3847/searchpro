import json
import requests
import os
from openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils import get_instructions, format_query

load_dotenv()
app = Flask(__name__)


def format_query(query_data):
    extracted_data = """"""
    if "knowledgeGraph" in query_data:
        extracted_data += str(query_data["knowledgeGraph"])
    if "answerBox" in query_data:
        extracted_data += str(query_data["answerBox"])
    extracted_data += str(query_data["organic"])
    return extracted_data


def llm_response(formatted_result, user_query):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    instruction_prompt = get_instructions()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": f"{instruction_prompt}",
            },
            {
                "role": "user",
                "content": f"""
                User query:
                {user_query}

                Context:
                {formatted_result}
                """,
            },
        ],
    )
    return response.choices[0].message.content


@app.route("/query", methods=["POST"])
def query():
    query_data = request.get_json()
    user_query = query_data.get("query")

    search_url = "https://google.serper.dev/search"
    payload = json.dumps({"q": f"{user_query}", "location": "India", "gl": "in"})
    headers = {
        "X-API-KEY": f'{os.environ.get("SERPER_API_KEY")}',
        "Content-Type": "application/json",
    }

    query_response = requests.request(
        "POST", url=search_url, headers=headers, data=payload
    )

    formatted_result = format_query(query_response.json())

    final_resposne = llm_response(formatted_result, user_query)
    return jsonify({"response": f"{final_resposne}"})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
