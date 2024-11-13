import streamlit as st
import requests
import json

## Custom CSS styling to chaneg font to Poppins ;)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .stMarkdown {
        font-family: 'Poppins', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("SearchPro")
st.write("_Websearch powered by LLM_")

user_query = st.text_input("Enter your query:")

if st.button("Search"):
    if user_query:
        backend_api = "http://127.0.0.1:5000/query"
        headers = {"Content-Type": "application/json"}
        data = {"query": f"{user_query}"}

        with st.spinner("_Searching the web...._"):
            response = requests.post(
                backend_api, headers=headers, data=json.dumps(data)
            )
        if response.status_code == 200:
            result = response.json()
            result = result.get("response", {})
            result = result.strip("```").lstrip("json")
            result = json.loads(result)

            sources = result.get("sources", [])
            answer = result.get("response", {})

            tabs = st.tabs(["Answer", "Sources"])

            with tabs[0]:
                st.markdown("### Answer")
                st.markdown(answer["text"])

            with tabs[1]:
                st.markdown("### Sources")
                for source in sources:
                    st.markdown(f"-[{source['description']}]({source['link']})")

        else:
            st.write("Error:", response.status_code)
    else:
        st.write("Please enter a query.")
