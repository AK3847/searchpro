from flask import Flask, request, jsonify
import json
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI

with open("../instruction.txt", "r") as f:
    instruction_prompt = f.read()

load_dotenv()

app = Flask(__name__)


def format_query(query_data):
    extracted_data = """
    
    """
    with open("test.json", "w") as f:
        json.dump(query_data, f)

    extracted_data += str(query_data["organic"])
    return extracted_data


def llm_response(formatted_result, user_query):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"{instruction_prompt}",
                # "content": "You are an AI assistant, whose task is to deliver the content based on the given json query_response of a google search",
            },
            {
                "role": "user",
                #  "content": f"{formatted_result}"
                "content": f"""
                User query:
                {user_query}

                Context:
                {formatted_result}
                """,
            },
        ],
        max_tokens=1024,
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
