# PDF-Chatbot# PDF-Chatbot 📂🤖
Conversational question-answering over your own PDF notes using **OpenAI**, **LangChain**, **FAISS** and **Streamlit**.

## ✨ What it does
1. Loads every PDF found in `data/`.
2. Slices pages into overlapping text chunks.
3. Embeds the chunks with the `text-embedding-3-small` model.
4. Stores the vectors locally with a FAISS index (`faiss_store/`).
5. Lets you chat with the documents from:
   * a Streamlit web app (`ui.py`)
   * a simple CLI loop (`python main.py`)

The first run builds the index; later runs simply reload it for instant answers.

## 🗂 Repository layout

├── data/ # ← place your PDF files here

├── faiss_store/ # ← auto-generated vector index (index.faiss + index.pkl)

├── main.py # backend utilities & optional CLI

├── ui.py # Streamlit front-end


## ⚙️ Requirements
* Python 3.9+
* An OpenAI API key with access to:
  * `text-embedding-3-small`
  * `gpt-4o-mini` (feel free to change the model name in `main.py`)
* (Optional) `make` for one-line setup commands

## 🏃‍♂️ Quick start
1. Clone and enter the repo
git clone https://github.com/yourname/pdf-chatbot.git
cd pdf-chatbo

2. Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate # Windows: .

3. Install the libraries
pip install -r requirements.txt

4. Add your PDFs
mkdir -p data
cp ~/Downloa

5. Set your OpenAI key (or create a .env file)
export OPENAI_API_KEY="sk-..."

6a. Run the Streamlit app
streamlit run ui.py

visit http://localhost:8501
6b. OR use the CLI
python main.py


On the very first run you will see  
`Vector store missing or incomplete – rebuilding …`  
as the embeddings are generated and saved. Subsequent runs are instant.

## 🔒 Security note (pickle)
`faiss_store/index.pkl` is written with Python’s `pickle`.  
The code **only** loads this file when it already exists locally (i.e., you created it yourself), and does so by explicitly passing
allow_dangerous_deserialization=True


Never replace `faiss_store/` with files from untrusted sources.

## 🔧 Configuration
| Setting                   | Where                         | Default                    |
|---------------------------|-------------------------------|----------------------------|
| OpenAI API key            | `.env` or shell environment   | **required**               |
| PDFs directory            | constant `PDF_DIR` in `main.py` | `data`                   |
| FAISS store directory     | `VECTOR_STORE` in `main.py`     | `faiss_store`            |
| Embedding model           | `OpenAIEmbeddings` call         | `text-embedding-3-small` |
| Chat model                | `ChatOpenAI` call               | `gpt-4o-mini`            |
| Chunk size / overlap      | `load_and_split()`              | 1000 / 100 chars          |

Feel free to change any of these to suit your project.

## 📝 How it works (under the hood)
1. `load_and_split()` reads every PDF page via `PyPDFLoader`, then splits the text with `RecursiveCharacterTextSplitter`.
2. `build_vector_store()` embeds each chunk and saves a FAISS index.
3. `make_chat_chain()` wraps a `ChatOpenAI` model in a `ConversationalRetrievalChain` with `ConversationBufferMemory`.
4. `ui.py` caches the chain with `st.cache_resource` so the session is snappy.

## ❓ Troubleshooting
* **`OPENAI_API_KEY environment variable is not set`**  
  Export the key or create a `.env` file with `OPENAI_API_KEY=...`.
* **Missing `index.faiss`**  
  Delete the partial `faiss_store/` folder and rerun; the index will rebuild.
* **Model access errors**  
  Make sure your OpenAI account is enabled for the specified models, or switch to a model you do have.

## 📄 License
MIT – do anything you want, but don’t blame us if it breaks.

## 🙏 Acknowledgements
Built with  
-  LangChain  
-  FAISS  
-  Streamlit  
-  OpenAI Python SDK  

Happy chatting with your PDFs!


