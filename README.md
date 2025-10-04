# 🧠 NLP Query Engine for Employee Data 🤖

This is a full-stack web application that serves as an intelligent query engine for employee data. It can answer natural language questions by dynamically querying both a structured SQL database and a collection of unstructured documents (like resumes or performance reviews).

## ✨ Key Features

* **🔗 Dynamic Schema Discovery:** Automatically connects to and understands the structure of any SQL database without hard-coding table or column names.
* **🗣️➡️💾 Natural Language to SQL:** Uses a Large Language Model (Google's Gemini) to translate plain English questions into precise SQL queries.
* **📄🔎 Semantic Document Search:** Ingests documents (PDF, DOCX, TXT), creates vector embeddings, and uses a FAISS index to find the most semantically relevant information.
* **🤝 Hybrid Querying:** Intelligently handles complex questions that require information from both the database and the documents, presenting a unified result.
* **🖥️ Interactive Web UI:** A modern, responsive, and theme-able user interface built with React and Material-UI (MUI).
* **⚡ Performance:** Features an in-memory cache to provide instant results for repeated queries.

## 🛠️ Tech Stack

* **🐍 Backend:**
    * Python 3.8+
    * FastAPI
    * SQLAlchemy
    * Sentence-Transformers & FAISS
    * Google Generative AI
    * Python-dotenv

* **⚛️ Frontend:**
    * React (with Vite)
    * Material-UI (MUI)
    * Axios

## 🚀 Getting Started

### ✅ Prerequisites

* Git
* Python 3.8+ and Pip
* Node.js and npm

### 1. Clone the Repository

```bash
git clone [https://github.com/kavu-13/NLP-Query-Engine.git](https://github.com/kavu-13/NLP-Query-Engine.git)
cd NLP-Query-Engine
```

### 2. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Windows
    venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Generate `requirements.txt` and install dependencies:**
    ```bash
    pip freeze > requirements.txt
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    * Create a file named `.env` inside the `backend` folder.
    * Add your Google Gemini API key to it:
        ```
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```

### 3. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    # From the root project folder
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

## 💻 Usage

### 🏃‍♂️ Running the Application

You need to run both the backend and frontend servers simultaneously in two separate terminals.

* **Start the Backend Server:**
    * Open a terminal in the `backend` directory.
    * Make sure your virtual environment is active.
    * Run the command:
        ```bash
        uvicorn main:app --reload
        ```
    * The server will be running on `http://127.0.0.1:8000`.

* **Start the Frontend Server:**
    * Open a *second* terminal in the `frontend` directory.
    * Run the command:
        ```bash
        npm run dev
        ```
    * The application will be available at `http://localhost:5173` (or the URL shown in the terminal).

### 🖱️ Using the Interface

1.  Open your browser to the frontend URL (e.g., `http://localhost:5173`).
2.  **Connect to a Database:** Use the first panel to connect to your SQL database.
3.  **Upload Documents:** Use the second panel to upload unstructured files.
4.  **Ask a Question:** Use the third panel to ask questions in natural language.
