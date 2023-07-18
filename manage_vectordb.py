# managing the Pinecone vector database

import os 
from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import pinecone


# Initialize pinecone
print("[*] Initializing pinecone...")
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"]
)

index_name = os.environ["PINECONE_INDEX_NAME"]
print("[+] Index name:",index_name)

# load documents
print("[*] Loading data...")
# loader = TextLoader("./uploads/sample_data.txt")
loader = DirectoryLoader("./uploads")
documents = loader.load()

# splitting
print("[*] Splitting data into chunks...")
text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=10)
documents = text_splitter.split_documents(documents)

# embeddings
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ["OPENAI_API_KEY"]
)

# llm
# llm = OpenAI(
#     temperature=0, 
#     openai_api_key=os.environ["OPENAI_API_KEY"]
# )
llm = ChatOpenAI(
    model='gpt-3.5-turbo'
)


# # qa using dosearch

# docsearch = Pinecone.from_documents(
#     documents, 
#     embeddings, 
#     index_name=index_name
# )
# # # if you already have an index
# # docsearch = Pinecone.from_existing_index(index_name, embeddings)

# # # query answering 
# def get_response_using_docsearch(query):
#     docs = docsearch.similarity_search(query)
#     return docs


# qa using RetrievalQA

vectordb = Pinecone.from_documents(
    documents, 
    embeddings, 
    index_name=index_name
)

retriever = vectordb.as_retriever()
qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever
)

def get_response_using_RetrievalQA(query):
    response = qa.run(query)
    return response
    

# add more texts to the vectorstore
def add_more_texts(new_text):
    # Adding More Text to an Existing Index
    index = pinecone.Index(index_name)
    print("index...")
    vectorstore = Pinecone(index, embeddings.embed_query, "text")
    print("vectorstore good...")
    print(new_text)
    vectorstore.add_texts("The value of ABC is 7")
    print("\n\nloaded ABC\n")
    for more_text in new_text.split("\n"):
        vectorstore.add_texts(more_text)
        print("Loaded",more_text)
    print("\n\nmore text added\n")





if __name__ == "__main__":
    while True:
        query = input("[Human]: ")
        response = get_response_using_RetrievalQA(query)
        print("[AI]:", response)



# """
# # # Adding More Text to an Existing Index
# # index = pinecone.Index("langchain-demo")
# # vectorstore = Pinecone(index, embeddings.embed_query, "text")
# # vectorstore.add_texts("More text!")
# """
