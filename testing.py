from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # type: ignore
import httpx

print("Testing Langchain with GenAI Lab Models")
client = httpx.Client(verify=False)

import os

tiktoken_cache_dir = "c:/Users/GenAICHNSIRUSR29/tiktoken_cache"
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir

print("Client created successfully")
print("Creating LLM and Embedding Model instances")
llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure_ai/genailab-maas-DeepSeek-V3-0324",
    api_key="sk-p9OE4-L89M-QMgMJ66JYBQ",  
    http_client=client,
)

print("LLM instance created successfully")

print("Creating Embedding Model instance")
embedding_model = OpenAIEmbeddings(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-text-embedding-3-large",
    api_key="sk-p9OE4-L89M-QMgMJ66JYBQ",  # Replace with your actual API key
    http_client=client,
)

print("Embedding Model instance created successfully")
print("Invoking LLM with a test prompt")

print(llm.invoke("Who is the President of India").content)



# DON'T EDIT THIS FILE


# [SSLError] [SSL: CERTIFICATE_VERIFY_FAILED]
# https://stackoverflow.com/questions/76106366/how-to-use-tiktoken-in-offline-mode-computer
