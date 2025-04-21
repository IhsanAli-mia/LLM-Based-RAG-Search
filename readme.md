
# LLM-Based RAG System
A powerful search application that combines web scraping with the Retrieval-Augmented Generation (RAG) approach to provide intelligent answers to user queries.
Main packages used: 


## Overview

This project consists of two main components:

1. **Frontend (Streamlit)**: A clean, user-friendly interface where users can enter their queries and view the generated responses.
2. **Backend (Flask)**: A service that handles the search process, content retrieval, and answer generation using a language model.

The application works by:
- Taking a user query
- Searching the web for relevant information using SerpAPI
- Scraping and processing the content from top search results
- Using a vector database (FAISS) to store and retrieve relevant context
- Leveraging OpenAI's language models to generate comprehensive, contextually-aware answers
- Maintaining conversational context across a session

## Features

- **Web Search Integration**: Uses SerpAPI to find relevant web pages based on the user's query
- **Content Extraction**: Employs the Newspaper3k library to extract clean text from web pages
- **Vector Embedding**: Converts text into embeddings for semantic similarity search
- **Session-Based Memory**: Maintains conversation history for contextual follow-up questions
- **RAG Architecture**: Enhances LLM responses with retrieved web content for more accurate answers

## Main Packages

- **Streamlit**: Powers the interactive web interface with minimal code
- **Flask**: Runs the backend API service that processes queries and generates responses
- **LangChain**: Orchestrates the RAG workflow, connecting the LLM with retrieval components
- **FAISS**: Creates and manages the vector database for efficient similarity search
- **SerpAPI**: Provides Google search results programmatically
- **Newspaper3k**: Extracts clean text content from web pages
- **OpenAI**: Connects to OpenAI's API for text embeddings and LLM responses
- **python-dotenv**: Manages environment variables for API keys

## Prerequisites

- Python 3.8 or above

## Setup Instructions

### Step 1: Clone or download the Repository (if emailed)

```bash
git clone https://github.com/your-repo-url.git
cd project_name
```

Or download it

### Step 2: Set Up a Virtual Environment

You can use `venv` or `conda` to create an isolated environment for this project.

#### Using `venv`

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

#### Using `conda`

```bash
conda create --name project_env python=3.8
conda activate project_env
```

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory as in `.env.example`


### Step 5: Run the Flask Backend

Navigate to the `flask_app` directory and start the Flask server:

```bash
cd flask_app
python app.py
```

### Step 6: Run the Streamlit Frontend

In a new terminal, run the Streamlit app:

```bash
cd streamlit_app
streamlit run app.py
```

### Step 7: Open the Application

Open your web browser and go to `http://localhost:8501`. You can now interact with the system by entering your query.

## Project Structure

- **flask_app/**: Contains the backend Flask API and utility functions.
- **streamlit_app/**: Contains the Streamlit front-end code.
- **.env**: Stores API keys (make sure this file is not included in version control).
- **requirements.txt**: Lists the project dependencies.
