import streamlit as st
import requests
import uuid

session_id = st.session_state.get("session_id", str(uuid.uuid4()))
st.session_state["session_id"] = session_id

st.set_page_config(page_title="LLM RAG Search", page_icon="🔍", layout="centered")

st.markdown(
    """
    <style>
        .stTextInput>div>div>input {
            font-size: 1.2rem;
        }
        .stButton>button {
            font-size: 1.1rem;
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
        }
        .stMarkdown {
            font-size: 1.1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("LLM-based RAG Search")
st.markdown("Ask me anything and I'll search the web, analyze the content, and generate an intelligent response using a large language model.")

# --- Input ---
query = st.text_input("🔎 Enter your query here", placeholder="e.g., What are the benefits of green tea?", key="query")

# Allow pressing Enter to trigger
if query:
    with st.spinner("Searching and thinking... 🤔"):
        try:
            flask_url = "http://localhost:5001/query"
            response = requests.post("http://localhost:5001/query", json={
                "query": query,
                "session_id": session_id
            })

            if response.status_code == 200:
                answer = response.json().get('answer', "No answer received.")
                st.success("✅ Answer:")
                st.markdown(f"> {answer}")
            else:
                st.error(f"❌ Backend error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("🚫 Could not connect to the Flask backend. Is it running?")
