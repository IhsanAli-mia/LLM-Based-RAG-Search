from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from newspaper import Article
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import uuid

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# In-memory session storage
session_memories = {}
session_vectorstores = {}

@app.route('/query', methods=['POST'])
def query_handler():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query missing"}), 400

    user_query = data['query']
    session_id = data.get('session_id', str(uuid.uuid4()))

    print(f"[Session: {session_id}] Received query: {user_query}")

    # Step 1: Search and scrape articles based on the query
    articles = search_and_scrape(user_query)

    os.getenv("OPENAI_API_KEY")
    
    # Step 2: Embed and store in FAISS (or reuse existing session vector store)
    embeddings = OpenAIEmbeddings()
    documents = [Document(page_content=text) for text in articles]

    try:
        if session_id not in session_vectorstores:
            vectorstore = FAISS.from_documents(documents, embeddings)
            session_vectorstores[session_id] = vectorstore
        else:
            session_vectorstores[session_id].add_documents(documents)
            vectorstore = session_vectorstores[session_id]
    
        # Step 3: Setup or fetch memory
        if session_id not in session_memories:
            session_memories[session_id] = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )
    
        memory = session_memories[session_id]
    
        # Step 4: Create conversational retrieval chain
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")

        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            verbose=True
        )
    # Step 5: Generate response
        answer = chain.run(user_query)
    except Exception as e:
        
        print(f"Error during chain execution: {e}")
        return jsonify({"error": "Error processing the query"}), 500

    return jsonify({"answer": answer, "session_id": session_id})

def search_and_scrape(query, num_results=3):
    SERP_API_KEY = os.getenv("SERP_API_KEY")
    search_url = "https://serpapi.com/search"

    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "num": num_results
    }

    try:
        search_res = requests.get(search_url, params=params)
        search_res.raise_for_status()
        results = search_res.json().get("organic_results", [])

        contents = []
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        for res in results:
            if len(contents) >= num_results:
                break

            url = res.get("link")
            if url:
                try:
                    article = Article(url)
                    article.config.browser_user_agent = headers['User-Agent']
                    article.download()
                    article.parse()
                    if article.text:
                        contents.append(article.text)
                except Exception as e:
                    print(f"Error scraping {url}: {e}")

        return contents

    except Exception as e:
        print("Error during search and scrape:", e)
        return []

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
