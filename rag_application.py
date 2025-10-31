import streamlit as st
from pdfminer.high_level import extract_text
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
import httpx
import tempfile
import os

# Disable SSL verification (use with caution)
client = httpx.Client(verify=False)

tiktoken_cache_dir =r"C:\Users\GenAICHNSIRUSR47\Downloads"
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir

# validate
assert os.path.exists(os.path.join(tiktoken_cache_dir,"9b5ad71b2ce5302211f9c61530b329a4922fc6a4"))


# LLM and Embedding setup
llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure_ai/genailab-maas-DeepSeek-V3-0324",
    api_key="sk-cXGENbsANV62rD-Yadc5Uw",  # Replace with your actual key
    http_client=client
)

embedding_model = OpenAIEmbeddings(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-text-embedding-3-large",
    api_key="sk-cXGENbsANV62rD-Yadc5Uw",  # Replace with your actual key
    http_client=client
)

# Streamlit UI setup
st.set_page_config(page_title="RAG PDF Summarizer")
st.title("📄 RAG-powered PDF Summarizer")

# File upload
upload_file = st.file_uploader("Upload a PDF", type="pdf")

if upload_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(upload_file.read())
        temp_file_path = temp_file.name

    # Step 1: Extract text from PDF
    raw_text = extract_text(temp_file_path)

    # Step 2: Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(raw_text)

    # Step 3: Embed chunks and store in Chroma DB
    with st.spinner("🔍 Indexing document..."):
        vectordb = Chroma.from_texts(chunks, embedding_model, persist_directory="./chroma_index")
        vectordb.persist()

    # Step 4: Setup Retrieval-Augmented Generation (RAG)
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # Step 5: Summarization prompt
    summary_prompt = "Please summarize this document based on the key topics:"
    with st.spinner("🧠 Running RAG summarization..."):
        result = rag_chain.invoke(summary_prompt)

