# author: Madhav (https://github.com/madhav-mknc)
# managing the Pinecone vector database

import json
import os 
from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA

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


#####################################################
# HELPER FUNCTIONS

# ignore this is helper function used for debugging
x_x_x = 0 
def mknc(text=''):
    global x_x_x
    print("\033[31m", x_x_x, "\033[96m", text, "\u001b[37m")
    x_x_x += 1

TOTAL_IDS = "ids_track.json"

def all_vectors():
    with open(TOTAL_IDS, "r") as json_file:
        return json.load(json_file)

def update_all_vectors(updated_ids):
    with open(TOTAL_IDS, "w") as json_file:
        json.dump(updated_ids, json_file)
    
def save_total_vectors_for_file(file, total):
    total_vectors = all_vectors()
    total_vectors[file] = total 
    with open(TOTAL_IDS, "w") as json_file:
        json.dump(total_vectors, json_file)
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
        print("\n[error]\n")
        print("filetype not in [pdf, txt, doc, docx, csv]")
    
    doc = loader.load()
    docs = CharacterTextSplitter(chunk_size=512, chunk_overlap=1).split_documents(doc)
    return docs


# INDEXING
def add_file(file_name, isurl=False):
    docs = load_and_split_document(file_name, isurl=isurl)
    texts = []
    metadatas = []
    ids = []
    for i, doc in enumerate(docs):
        texts.append(doc.page_content)
        metadatas.append({'source': file_name})
        ids.append(file_name+str(i))
    
    # save total no. of vectors for this file
    save_total_vectors_for_file(file=file_name, total=ids)

    res = Pinecone.from_texts(
        index_name=index_name,
        texts=texts,
        embedding=embeddings,
        batch_size=100,
        namespace=NAMESPACE,
        metadatas=metadatas,
        ids=ids
    )

# delete all the vectors (from a specific file)
def delete_file(file):
    # index.delete(namespace=file) # deletion with namespace
    # index.delete(filter={"source": {"$eq": file}}) # deletion with metadata
    try:
        ids = all_vectors()[file]
        index.delete(ids=ids, namespace=NAMESPACE)
        updated = all_vectors()
        updated.pop(file)
        update_all_vectors(updated)
    except Exception as e:
        mknc(e)
    

# reset index => delete -> create_new
def reset_index():
    pinecone.delete_index(index_name)
    metadata_config = {"indexed": ["source"]}
    pinecone.create_index(index_name, dimension=1536, metadata_config=metadata_config)


# list source files
def list_files():
    # stats = index.describe_index_stats()
    # sources = stats["namespaces"]
    sources = all_vectors().keys()
    return sources



############## Question Answering ##############
llm = OpenAI(temperature=0.3)

GENIEPROMPT = "You are an Ecommerce expert/mentor. Your users are beginners in this field. You provide accurate and descriptive answers to user questions, after researching through the vector DB. Provide additional descriptions of any complex terms being used in the response \n\nUser: {question}\n\nAi: "
prompt_template = PromptTemplate.from_template(GENIEPROMPT)

chain = load_qa_chain(llm, chain_type="stuff", verbose=False)
docsearch = Pinecone.from_existing_index(index_name, embeddings)

# query index
def get_response(query):
    docs = docsearch.similarity_search(
        query=query,
        namespace=NAMESPACE
    )

    for i in docs:
        mknc()
        for j in i:
            mknc(j)
        mknc()

    if not docs:
        return "No relevant data found."
    
    response = chain(
        {
            "input_documents": docs,
            "question": prompt_template.format(question=query)
        },
        return_only_outputs=True
    )
    return response["output_text"]



# command line interface for bot
def cli_run():
    try:
        while True:
            query = input("\033[0;39m\n[HUMAN] ").strip()
            if query == ".stats":
                print("\033[93m[SYSTEM]",index.describe_index_stats())
            elif query == ".reset_index":
                reset_index()
                print("\033[93m[SYSTEM] deleting index...")
            elif query == ".exit":
                reset_index()
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