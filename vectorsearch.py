from typing import List, Tuple
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
from vertexai.language_models import TextEmbeddingModel
from langchain.embeddings import VertexAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import VertexAI

loader = TextLoader("/Users/arnabsaha/projectai/help.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
embeddings_service = VertexAIEmbeddings()
llm = VertexAI(temparature=0.7)

#CONNECTION_STRING = "postgresql+psycopg2://postgres:@localhost:5432/arnabsaha?options=-csearch_path%3Dsoe"
COLLECTION_NAME = "soe12.help_topics"
CONNECTION_STRING = PGVector.connection_string_from_db_params(
     driver="psycopg2",
     host="localhost",
     port=int(5432),
     database="arnabsaha",
     user="arnabsaha",
     password='',
 )
db = PGVector.from_documents(
    embedding=embeddings_service,
    documents=docs,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    pre_delete_collection=True
)

#store = PGVector(
#    collection_name=COLLECTION_NAME,
#    connection_string=CONNECTION_STRING,
#    embedding_function=embeddings_service,
#)

#query = "Why my payment didnot went through?"
query1 = "Why my card transaction was declined?"
qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type='stuff',
    retriever=db.as_retriever(search_type="similarity", search_kwargs={"k": 2}),
    verbose=True)

result = qa({"query": query1})
print(result)

