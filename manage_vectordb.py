# managing the Pinecone vector database

import os 
from dotenv import load_dotenv
load_dotenv()

from utils import load_and_split_document
from langchain.embeddings.openai import OpenAIEmbeddings

import pinecone
from langchain.vectorstores import Pinecone


# Initialize pinecone
print("[*] Initializing pinecone...")
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"]
)

index_name = os.environ["PINECONE_INDEX_NAME"]
print("[+] Index name:",index_name)

metadata_config = {
    "indexed": ["source"]
}

pinecone.create_index(index_name,
                      dimension=1535,
                      metadata_config=metadata_config
)


# connecting to the index
index = pinecone.GRPCIndex(index_name)
index.describe_index_stats()

# load and split documents
documents = load_and_split_document("./uploads/sample_data.txt")

# texts
texts = []
for _doc in documents:
    texts.append(_doc.page_content)

# embeddings
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ["OPENAI_API_KEY"]
)

# embedding texts
res = embeddings.embed_documents(texts)




