# /temp /test scripts

print("Booting script...")

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

from langchain.callbacks import get_openai_callback


# vector database
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"]
)
index_name = os.environ["PINECONE_INDEX_NAME"]
index = pinecone.GRPCIndex(index_name)

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
def get_response(query, chat_history=[]):
    docs = docsearch.similarity_search(
        query=query,
        namespace="madhav"
    )

    prompt = {
        "input_documents": docs,
        "question": prompt_template.format(question=query, history=chat_history)
    }
    print(prompt)

    response = chain(prompt, return_only_outputs=True)
    return response["output_text"]

# check tokens for each call
def cli_run():
    try:
        while True:
            query = input("\033[0;39m\n[HUMAN] ").strip()
            if not query: continue

            with get_openai_callback() as cb:
                response = get_response(query)
            
            print("\033[0;32m[AI]",response)
            print("\033[31m[USAGE]",cb)
    except KeyboardInterrupt:
        print("\033[31mStopped")
    print("\u001b[37m")



# main
if __name__ == "__main__":
    cli_run()