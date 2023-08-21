#Upload a PDF to vector db and perform a search
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import VertexAI
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores.pgvector import PGVector

#Add a location where PDF is available
loader = PyPDFLoader("/Users/arnabsaha/projectai/help.pdf")
documents = loader.load()
llm = VertexAI(temparature=0.7)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
print(f"# of documents = {len(docs)}")

embeddings = VertexAIEmbeddings()

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
    embedding=embeddings,
    documents=docs,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    pre_delete_collection=True
)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})

qa = RetrievalQA.from_chain_type(
    llm= llm, chain_type="stuff", retriever=retriever
)

query = "Why my transaction was declined?"
result = qa.run(query)
print(result)
