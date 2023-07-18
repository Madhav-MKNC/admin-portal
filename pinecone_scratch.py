import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from pinecone_datasets import load_dataset


import numpy as np

import os
from dotenv import load_dotenv
load_dotenv()


# Loading Dataset
dataset = load_dataset("squad-text-embedding-ada-002")
dataset.head()
len(dataset)
# we drop sparse_values as they are not needed for this example
dataset.documents.drop(['sparse_values', 'blob'], axis=1, inplace=True)
dataset.head()


# Initialize pinecone
print("[*] Initializing pinecone...")
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"]
)
index_name = os.environ["PINECONE_INDEX_NAME"]

# connect to the index
index = pinecone.GRPCIndex(index_name)
index.describe_index_stats()

# upsert into db
index.upsert_from_dataframe(
    df=dataset.documents,
    batch_size=100
)
index.upsert(
    vectors=list(),
    batch_size=100
)

# embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=os.environ["OPENAI_API_KEY"]
)

# switch back to normal index for langchain
index = pinecone.Index(index_name)
vectorstore = Pinecone(
    index,
    embeddings,
    "text"
)

# stats
print(index.describe_index_stats())
input("end")

########################
##### From scratch #####
########################


""" Indexing """
data = data.reset_index(drop=True)
data = data.reset_index()
batch_size = 100

for i in tqdm(range(0, len(data), batch_size)):
    i_end = min(len(data), i+batch_size)
    batch = data.iloc[i:i_end]
    metadatas = [
        {
            'text': record[0],  # 'text' will contain the same data as 'context'
            'name': record[1]
        } for record in batch.itertuples(index=False)
    ]
    
    documents = batch['context'].tolist()
    embeds = embed.embed_documents(documents)
    ids = batch['index'].astype(str).tolist()
    index.upsert(vectors=list(zip(ids, embeds, metadatas))) # add everything to pinecone

index = pinecone.Index(index_name)
vectorstore = Pinecone(index, embed.embed_query, "text")
     

""" Initializing the Conversational Agent """
query = "Tell me what do you know?"
vectorstore.similarity_search(
    query,  
    k=3
)





