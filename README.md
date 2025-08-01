# PDF Chatbot

Chat with your PDFs using Retrieval-Augmented Generation (RAG).
This project indexes local PDF files into a FAISS vector store and answers questions using an OpenAI chat model with conversation memory.

> **Stack:** LangChain, OpenAI (Chat + Embeddings), FAISS, (optional) Streamlit UI

---

## Features

* 📄 **Multi-PDF ingestion** using `PyPDFLoader`
* ✂️ **Smart chunking** via `RecursiveCharacterTextSplitter`
* 🧠 **Semantic search** with **FAISS** and `text-embedding-3-small`
* 💬 **Conversational QA** using `ConversationalRetrievalChain` + `ConversationBufferMemory`
* ⚡ **Automatic indexing** on first run (rebuilds if the FAISS store is missing)
* 🖥️ **CLI chatbot** (always available)
* 🌐 **Optional Streamlit UI** (simple chat interface)

---

## Project structure

```
PDF-Chatbot-main/
├── LICENSE
├── README.md              # ← you are here
├── main.py                # CLI + core RAG pipeline
├── ui.py                  # Optional Streamlit chat app
├── requirements.txt
└── data/                  # (create) put your PDF files here
```

Key modules in `main.py`:

* `load_and_split(pdf_paths, chunk=1000, overlap=100)` – loads PDFs and splits them into chunks
* `build_vector_store(docs, store_path="faiss_store")` – builds and persists a FAISS index
* `get_vector_store(pdf_dir="data", store_path="faiss_store")` – loads existing index or rebuilds it from PDFs
* `make_chat_chain(vectordb)` – creates a `ConversationalRetrievalChain` using `gpt-4o-mini` and memory

**Defaults:**

| Purpose                | Default value            |
| ---------------------- | ------------------------ |
| PDF directory          | `data/`                  |
| Vector store directory | `faiss_store/`           |
| Embeddings model       | `text-embedding-3-small` |
| Chat model             | `gpt-4o-mini`            |

---

## Prerequisites

* Python **3.9+** (3.10 recommended)
* An **OpenAI API key** with access to the above models

Create a `.env` file in the project root (or export env vars) containing:

```
OPENAI_API_KEY=sk-...
```

> The app loads `OPENAI_API_KEY` via `python-dotenv`. If the variable is not set, the program will error on startup.

---

## Setup

```bash
# 1) (optional but recommended) create & activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Add your PDFs
mkdir -p data
# Place one or more .pdf files into the ./data directory
```

---

## Usage

### A) CLI (recommended for first run / index build)

The first run builds the vector store from the PDFs in `./data`.
Subsequent runs will reuse the saved FAISS index.

```bash
python main.py
```

Example session:

```
PDF Chatbot – type 'exit' to quit.

You: What is the main conclusion of the report?
Bot: ...
You: Summarize section 2 in three bullet points.
Bot: ...
You: exit
```

### B) Streamlit UI (optional)

A lightweight web UI is provided in `ui.py`.

```bash
# Make sure the FAISS index exists (run the CLI once if needed)
streamlit run ui.py
```

> The UI loads the existing `faiss_store` and lets you chat in the browser.
> If you change your PDFs, rerun the CLI to rebuild the index.

---

## Configuration

You can tweak chunking, overlap, directories, and models by editing the constants / function parameters in `main.py`:

| Setting       | Where to change                                                      | Default         |
| ------------- | -------------------------------------------------------------------- | --------------- |
| PDF directory | `PDF_DIR`                                                            | `"data"`        |
| Vector store  | `VECTOR_STORE`                                                       | `"faiss_store"` |
| Chunking      | `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)` | as shown        |
| Embeddings    | `OpenAIEmbeddings(model="text-embedding-3-small")`                   | as shown        |
| Chat model    | `ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)`              | as shown        |

---

## Troubleshooting

| Issue                                                | Fix                                                       |
| ---------------------------------------------------- | --------------------------------------------------------- |
| **`OPENAI_API_KEY environment variable is not set`** | Ensure `.env` is present or the variable is exported.     |
| **`No PDFs found in 'data'. Add files and retry.`**  | Place one or more `.pdf` files in `./data` and run again. |
| Rebuild index                                        | Delete the `faiss_store/` directory and rerun the CLI.    |
| **`allow_dangerous_deserialization=True`** warning   | Only load FAISS indexes you trust.                        |

---

## Roadmap (ideas)

* Multi-file upload from the UI
* Per-document/source citations in answers
* Support for non-PDF formats (DOCX, HTML)
* Cloud vector stores (Chroma/PGVector) behind a flag
* Dockerfile & CI pipeline

---

## License

This project is released under the **MIT License** (see `LICENSE`).

© 2025 Manohar
