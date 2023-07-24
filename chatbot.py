# author: Madhav (https://github.com/madhav-mknc)
# managing the Pinecone vector database

import os 
from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

import pinecone
from langchain.vectorstores import Pinecone


#####################################################
# HELPER FUNCTIONS
# ignore this is helper function used for debugging
x_x_x = 0 
def mknc(text=''):
    global x_x_x
    print("\033[31m", x_x_x, "\033[96m", text, "\u001b[37m")
    x_x_x += 1
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

# using OpenAI llm
llm = OpenAI(temperature=0.3, presence_penalty=0.6)

# custom prompt
GENIEPROMPT = """
You are an Ecommerce expert/mentor. Your users are beginners in this field.
You provide accurate and descriptive answers to user questions, after and only researching through the input documents and the context provided to you.
Just output 'No relevant data found' if the query is irrelevant to the context provided even if the query is very common.
Do not forget if the query if not relevant with the context and input documents you have then just output 'No relevant data found', this is very important.
Do not output to irrelevant query if the documents provided to you doest give you context, no matter how much common the query is.
Provide additional descriptions of any complex terms being used in the response \n\nUser: {question}\n\nAi: 
"""

prompt_template = PromptTemplate.from_template(GENIEPROMPT)

# chain
chain = load_qa_chain(
    llm=llm,
    chain_type="stuff",
    verbose=False
)

# for searching relevant docs
docsearch = Pinecone.from_existing_index(
    index_name,
    embeddings
)

# query index
def get_response(query):
    docs = docsearch.similarity_search(
        query=query,
        namespace=NAMESPACE
    )

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
