# managing the Pinecone vector database

import os 
from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
import pinecone


# load documents
loader = TextLoader("./uploads/sample_data.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=10)
documents = text_splitter.split_documents(documents)

# embeddings
embeddings = OpenAIEmbeddings()

# Initialize pinecone
print("[*] Initializing pinecone...")
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"]
)
index_name = os.environ["PINECONE_INDEX_NAME"]

# doc search on pinecone
docsearch = Pinecone.from_documents(
    documents, 
    embeddings, 
    index_name=index_name
)

# if you already have an index, you can load it like this
# docsearch = Pinecone.from_existing_index(index_name, embeddings)

# query answering 
query = "what is the value of XYZ"
docs = docsearch.similarity_search(query)
result = docs[0].page_content
print(result)





# Adding More Text to an Existing Index
index = pinecone.Index("langchain-demo")
vectorstore = Pinecone(index, embeddings.embed_query, "text")
vectorstore.add_texts("More text!")