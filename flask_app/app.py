import json
import requests
import os
from openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils import get_instructions, format_query

load_dotenv()
app = Flask(__name__)


def llm_response(formatted_result, user_query) -> json:
    """
    Generate an AI response using OpenAI's chat completion API.

    Args:
        formatted_result (str): Preprocessed search results to provide context
        user_query (str): Original query from the user

    Returns:
        str: JSON formatted response from the OpenAI model

    Raises:
        OpenAIError: If there's an error communicating with the OpenAI API
    """
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
def query() -> json:
    """
    Handle POST requests to /query endpoint.

    Expects a JSON payload with a 'query' field. Performs a web search using
    Serper API and processes the results through an AI model.

    Request Body:
    >>>    {
    >>>        "query": "user's search query"
    >>>    }

    Returns:
    >>> JSON: {
            "response": "LLM-generated response based on search results"
        }

    Raises:
        400: If the request payload is missing or invalid
        500: If there's an error with external API calls
    """
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
