# author: Madhav (https://github.com/madhav-mknc)
# managing the Pinecone vector database

import json
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
    CSVLoader,
    WebBaseLoader
)
from langchain.text_splitter import CharacterTextSplitter


#####################################################
# HELPER FUNCTIONS

# ignore this is helper function used for debugging
x_x_x = 0 
def mknc(text=''):
    global x_x_x
    print("\033[31m", x_x_x, "\033[96m", text, "\u001b[37m")
    x_x_x += 1

TOTAL_IDS = ".stored_files.json"

def read_all_files():
    with open(TOTAL_IDS, "r") as json_file:
        files = json.load(json_file)
        return list(files)

def write_all_files(files):
    with open(TOTAL_IDS, "w") as json_file:
        json.dump(files, json_file)

def update_read_all_files_list(add_file="", remove_file=""):
    files = read_all_files()
    
    if add_file:
        files.append(add_file)
    if remove_file:
        files.remove(remove_file)
        
    write_all_files(files)
#####################################################


# Initialize pinecone
print("[*] Initializing pinecone...\n")
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"]
)

index_name = os.environ["PINECONE_INDEX_NAME"]
print("[+] Index name:\n",index_name)

NAMESPACE = "madhav"
print("[+] Namespace:",NAMESPACE)

# connecting to the index
index = pinecone.GRPCIndex(index_name)
print(index.describe_index_stats())

# embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])


# load and split documents
def load_and_split_document(file_path, isurl=False):
    file_extension = file_path.split('.')[-1].lower()
    
    if isurl:
        url = file_path
        print(url)
        loader = WebBaseLoader(url)
    elif file_extension == "txt":
        loader = TextLoader(file_path)
    elif file_extension == "pdf":
        loader = PyMuPDFLoader(file_path)
    elif file_extension == "doc" or file_extension == "docx":
        loader = Docx2txtLoader(file_path)
    elif file_extension == "csv":
        loader = CSVLoader(file_path)
    else:
        raise TypeError("filetype not in [pdf, txt, doc, docx, csv]")
    
    doc = loader.load()
    docs = CharacterTextSplitter(chunk_size=512, chunk_overlap=1).split_documents(doc)
    return docs


# INDEXING
def add_file(file_name, isurl=False):
    # checking if this file already exists
    files = read_all_files()
    if file_name in files:
        status = f"{file_name} already exists"
        return status

    docs = load_and_split_document(file_name, isurl=isurl)
    texts = []
    metadatas = []
    ids = []
    for i, doc in enumerate(docs):
        texts.append(doc.page_content)
        metadatas.append({'source': file_name})
        ids.append(file_name+str(i))

    res = Pinecone.from_texts(
        index_name=index_name,
        texts=texts,
        embedding=embeddings,
        batch_size=100,
        namespace=NAMESPACE,
        metadatas=metadatas,
        ids=ids
    )

    # save total no. of vectors for this file
    update_read_all_files_list(add_file=file_name)

    status = "ok"
    return status
    

# delete all the vectors from a specific file specified by metadata
def delete_file(file):
    index.delete(
        filter={
            "source": {
                "$eq": file
            }
        },
        namespace=NAMESPACE,
        delete_all=False
    )

    # update files list (which is maintained locally)
    update_read_all_files_list(remove_file=file)

# deletes the namespace
def reset_index():
    index.delete(
        namespace=NAMESPACE,
        delete_all=True
    )

# list source files
def list_files():
    # stats = index.describe_index_stats()
    # sources = stats["namespaces"]
    sources = read_all_files()
    return sources



############## CHATBOT ##############
from chatbot import get_response



# command line interface for bot
def cli_run():
    try:
        while True:
            query = input("\033[0;39m\n[HUMAN] ").strip()
            if query == ".stats":
                print("\033[93m[SYSTEM]",index.describe_index_stats())
            elif query == ".reset_index":
                reset_index()
                write_all_files(files=[])
                print("\033[93m[SYSTEM] deleting index...")
            elif query == ".exit":
                print("\033[93m[SYSTEM] exitting...")
                return
            elif query:
                response = get_response(query)
                print("\033[0;32m[AI]",response)
            else:
                pass
    except KeyboardInterrupt:
        print("\033[31mStopped")
    print("\u001b[37m")

if __name__ == "__main__":
    cli_run()