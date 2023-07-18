# managing the Pinecone vector database

import os 
from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings.openai import OpenAIEmbeddings

import pinecone
from langchain.vectorstores import Pinecone

from langchain.document_loaders import ( 
    PyMuPDFLoader, 
    TextLoader,
    Docx2txtLoader, 
    WebBaseLoader,
    CSVLoader
)
from langchain.text_splitter import CharacterTextSplitter

import pandas as pd
from pathlib import Path
from tqdm.auto import tqdm


# Initialize pinecone
print("[*] Initializing pinecone...\n")
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"]
)

index_name = os.environ["PINECONE_INDEX_NAME"]
print("[+] Index name:\n",index_name)

# connecting to the index
index = pinecone.GRPCIndex(index_name)
print(index.describe_index_stats())
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
# vectorstore = Pinecone(index, embeddings.embed_query, "text")


# load and split documents
def load_and_split_document(file_path):
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == "txt":
        loader = TextLoader(file_path)
    elif file_extension == "pdf":
        loader = PyMuPDFLoader(file_path)
    elif file_extension == "doc" or file_extension == "docx":
        loader = Docx2txtLoader(file_path)
    elif file_extension == "csv":
        loader = CSVLoader(file_path)
    elif file_extension == "url":
        with open(file_path, 'r') as something:
            url = something.read()
        loader = WebBaseLoader(url)

    doc = loader.load()
    docs = CharacterTextSplitter(chunk_size=512, chunk_overlap=10).split_documents(doc)
    return docs


# INDEXING
def add_file(file_path):
    documents = load_and_split_document(file_path)
    source = file_path.split("/")[-1]
    data = ""
    for _doc in documents:
        data = data + "\n" + _doc.page_content

    batch_size = 100
    for i in tqdm(range(0, len(data), batch_size)):
        i_end = min(len(data), i+batch_size)
        batch = data[i:i_end]
        metadatas = [
            {
                'source': source
            } for _ in batch
        ]
        embeds = embeddings.embed_documents(batch)
        ids = f"id_{i}"
        index.upsert(vectors=list(zip(ids, embeds, metadatas)), namespace=source) # add everything to pinecone


# delete all the vectors (from a specific file)
def delete_file(file):
    index.delete(delete_all=True, namespace=file)


# reset index => delete -> create_new
def reset_index():
    pinecone.delete_index(index_name)
    metadata_config = {"indexed": ["source"]}
    pinecone.create_index(index_name, dimension=1536, metadata_config=metadata_config)


def list_files():
    stats = index.describe_index_stats()
    sources = stats["namespaces"]
    return sources



