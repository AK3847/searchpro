import streamlit as st
import requests
import json

st.title("searchpro - LLM")

user_query = st.text_input("Enter your query:")

if st.button("Search"):
    if user_query:
        backend_api = "http://127.0.0.1:5000/query"
        headers = {"Content-Type": "application/json"}
        data = {"query": f"{user_query}"}

        response = requests.post(backend_api, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json().get("response", "No response")
            st.write(result)
        else:
            st.write("Error:", response.status_code)
    else:
        st.write("Please enter a query.")
