import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

PDF_DIR      = "data"
VECTOR_STORE = "faiss_store"   

def load_and_split(pdf_paths, chunk=1_000, overlap=100):
    """
    Read a list of PDFs and break them into Document chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    pages = []
    for path in pdf_paths:
        loader = PyPDFLoader(path)
        pages.extend(loader.load())

    return splitter.split_documents(pages)


def build_vector_store(docs, store_path=VECTOR_STORE):
    """
    Create a FAISS index from Documents and save it to disk.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb = FAISS.from_documents(docs, embeddings)
    vectordb.save_local(store_path)
    return vectordb


def get_vector_store(pdf_dir=PDF_DIR, store_path=VECTOR_STORE):
    """
    Load an existing FAISS index if it is completely present;
    otherwise rebuild it from the PDFs.
    """
    required = {"index.faiss", "index.pkl"}
    store_ok = Path(store_path).is_dir() and required.issubset(
        {p.name for p in Path(store_path).iterdir()}
    )

    if not store_ok:
        print("Vector store missing or incomplete – rebuilding …")
        pdfs = [
            str(Path(pdf_dir, f))
            for f in os.listdir(pdf_dir)
            if f.lower().endswith(".pdf")
        ]
        if not pdfs:
            raise FileNotFoundError(
                f"No PDFs found in '{pdf_dir}'. Add files and retry."
            )

        docs = load_and_split(pdfs)
        vectordb = build_vector_store(docs, store_path)
    else:
        vectordb = FAISS.load_local(
            store_path,
            OpenAIEmbeddings(),
            allow_dangerous_deserialization=True,  # we trust our own file
        )

    return vectordb


def make_chat_chain(vectordb):
    """
    Build a ConversationalRetrievalChain that remembers dialogue.
    """
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True
    )
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(),
        memory=memory,
        verbose=False,
    )



def main():
    vectordb = get_vector_store()
    chain = make_chat_chain(vectordb)

    print("PDF Chatbot – type 'exit' to quit.\n")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"exit", "quit"}:
            break
        result = chain({"question": query})
        print("Bot:", result["answer"])


if __name__ == "__main__":
    main()
