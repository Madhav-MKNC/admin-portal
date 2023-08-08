# author: Madhav (https://github.com/madhav-mknc)
# managing the Pinecone vector database

import os 
from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import OpenAI

from langchain.prompts import PromptTemplate

from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationChain

import pinecone
from langchain.vectorstores import Pinecone


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
You could also use the conversation history provided to you.

Just output 'No relevant data found' if the query is irrelevant to the context provided or the conversation even if the query is very common.
Do not output to irrelevant query if the documents provided to you or the conversation history doesn't give you context, no matter how much common the query is.

Provide additional descriptions of any complex terms being used in the response

Current conversation:
{history}
User: {question}
Ai: 
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
def get_response(query, chat_history):
    docs = docsearch.similarity_search(
        query=query,
        namespace=NAMESPACE
    )
    response = chain(
        {
            "input_documents": docs,
            "question": prompt_template.format(question=query, history=chat_history)
        },
        return_only_outputs=True
    )
    return response["output_text"]
