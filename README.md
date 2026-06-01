# 📚 Multilingual Multi-Document AI Chatbot

An AI-powered multilingual chatbot that answers questions from multiple PDF documents using OCR, Retrieval-Augmented Generation (RAG), FAISS vector search, Groq LLM, and MySQL-powered chat history storage.

---

## 🚀 Key Features

- 📄 Multi-PDF Question Answering
- 🔍 OCR Support for Scanned PDFs
- 🌍 Multilingual Query & Response Support
- 🧠 Query Rewriting for Better Retrieval
- 📚 Retrieval-Augmented Generation (RAG)
- ⚡ FAISS Semantic Search
- 🤖 Groq LLM Integration
- 📌 Source-Aware Responses with Page References
- 🗄️ MySQL Chat History Storage
- 💬 Interactive Streamlit Interface

---

## 📸 Application Preview

### Home Page

![Home Page](images/homepage.png)

### PDF Upload & Processing

![PDF Upload](images/upload.png)

### Chat Response with Sources

![Chat Response](images/answers.png)

### MySQL Chat History Storage

![Database Storage](images/mysql.png)

---

## 📊 UML Diagrams

### Use Case Diagram

![Use Case Diagram](images/usecase%20diagram.png)

### Class Diagram

![Class Diagram](images/class%20diagram.png)

### Sequence Diagram

![Sequence Diagram](images/sequence%20diagram.png)

### Component Diagram

![Component Diagram](images/component%20diagram.png)

---

## 🔄 System Workflow

```text
User Query
    ↓
Language Detection
    ↓
Translate to English
    ↓
Query Rewriting
    ↓
FAISS Retrieval
    ↓
Groq LLM Answer Generation
    ↓
Response Translation
    ↓
Source Citation
    ↓
Store Chat History in MySQL
```

---

## 🏗️ System Architecture

```text
PDF Documents
      │
      ▼
PDF Loader
      │
      ▼
OCR Extraction
      │
      ▼
Document Chunking
      │
      ▼
Embedding Generation
      │
      ▼
FAISS Vector Store
      │
      ▼
Retriever
      │
      ▼
RAG Pipeline
      │
      ▼
Groq LLM
      │
      ▼
Translated Response
      │
      ▼
MySQL Storage
```

---

## 🛠️ Tech Stack

| Category | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Backend | Python |
| Framework | LangChain |
| LLM | Groq |
| Embeddings | HuggingFace |
| Vector Database | FAISS |
| OCR | Tesseract OCR |
| Database | MySQL |
| PDF Processing | PyMuPDF |
| Translation | Google Translator |
| Language Detection | LangDetect |

---

## 📂 Project Structure

```text
multilingual-chatbot/
│
├── app.py
├── db.py
├── requirements.txt
│
├── utils/
│   ├── pdf_loader.py
│   ├── embeddings.py
│   ├── rag_chain.py
│   ├── translator.py
│   └── rewriter.py
│
├── images/
│   ├── homepage.png
│   ├── upload.png
│   ├── answers.png
│   ├── mysql.png
│   ├── usecase diagram.png
│   ├── class diagram.png
│   ├── sequence diagram.png
│   └── component diagram.png
│
└── README.md
```

---

## 🎯 Challenges Solved

- Extracted text from scanned PDFs using OCR
- Supported multilingual user interactions
- Improved retrieval quality through query rewriting
- Enabled semantic search using FAISS
- Generated source-aware answers with citations
- Stored conversation history using MySQL
- Retrieved information across multiple PDF documents

---

## ⚙️ Installation

```bash
git clone <repository-url>

cd multilingual-chatbot

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

## 🔮 Future Enhancements

- User Authentication
- Session-Based Chat History
- Feedback System
- Conversation Memory
- Voice-Based Queries
- Cloud Deployment

---

## 👩‍💻 Contributors

- Sukruti Naidu
- Navya Pachigolla

---

## ⭐ Support

If you found this project useful:

- ⭐ Star the repository
- 🍴 Fork the repository
- 🤝 Contribute to the project