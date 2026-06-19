# 📚 Enterprise RAG Knowledge Assistant

An Enterprise-grade Retrieval-Augmented Generation (RAG) application built using LangChain, ChromaDB, Streamlit, and Large Language Models.

## 🚀 Live Demo

Coming Soon

## 📌 Features

- PDF Upload & Processing
- Intelligent Document Chunking
- Semantic Search using Vector Embeddings
- ChromaDB Vector Database
- Retrieval-Augmented Generation (RAG)
- Multi-Chat Support
- Source Citations
- Relevance Scoring
- Enterprise Knowledge Assistant UI
- Session-Based Document Isolation

---

## 🏗 Architecture

PDF Upload
↓
Document Chunking
↓
Embeddings Generation
↓
ChromaDB Storage
↓
Semantic Retrieval
↓
LLM Context Injection
↓
Answer Generation
↓
Source Attribution

---

## 🛠 Tech Stack

### AI / LLM

- OpenAI
- Groq
- LangChain

### Vector Database

- ChromaDB

### Backend

- Python

### Frontend

- Streamlit

### Embeddings

- Sentence Transformers
- HuggingFace Embeddings

---

## 📂 Project Structure

```bash
enterprise-rag-assistant/
│
├── app.py
├── requirements.txt
├── .env.example
│
├── utils/
│   ├── llm.py
│   ├── pdf_loader.py
│   ├── retriever.py
│   ├── rag_chain.py
│   └── vector_store.py
│
├── uploads/
├── vectorstore/
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Ashish6099/enterprise-rag-assistant.git
cd enterprise-rag-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create:

```env
.env
```

Example:

```env
OPENAI_API_KEY=your_key_here

# OR

GROQ_API_KEY=your_key_here
```

---

## ▶ Run Application

```bash
streamlit run app.py
```

---

## 📸 Current Capabilities

- Upload PDF
- Generate Embeddings
- Create Vector Database
- Ask Questions
- Retrieve Relevant Chunks
- Generate AI Answers
- Display Sources
- Multi-Chat Conversations

---

## 🎯 Future Roadmap

- Multi-PDF Knowledge Bases
- Website Crawling
- User Authentication
- Chat Export
- Agentic RAG
- Hybrid Search
- Memory Management
- Production Deployment

---

## 👨‍💻 Author

### Ashish Rauniyar

AI Engineer | GenAI Engineer | AI Automation Engineer

GitHub:
https://github.com/Ashish6099

LinkedIn:
https://linkedin.com/in/ashish-rauniyar-6600961a8

Portfolio:
https://ashish6099.github.io/Ashish-Portfolio/

---

## ⭐ If you found this project useful, consider starring the repository.
