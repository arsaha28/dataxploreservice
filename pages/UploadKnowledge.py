import streamlit as st
import pandas as pd
from io import StringIO
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import VertexAI
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from io import BytesIO
from pathlib import Path

st.title("DXPloreService")
uploaded_file = st.file_uploader("Choose a file","pdf")
embeddings = VertexAIEmbeddings()
llm = VertexAI(temparature=0.7)

COLLECTION_NAME = "soe12.help_topics"
CONNECTION_STRING = PGVector.connection_string_from_db_params(
     driver="psycopg2",
     host="localhost",
     port=int(5432),
     database="arnabsaha",
     user="arnabsaha",
     password='',
 )


if uploaded_file is not None:
    save_folder = '/Users/arnabsaha/projectai/upload/'
    save_path = Path(save_folder, uploaded_file.name)
    with open(save_path, mode='wb') as w:
        w.write(uploaded_file.getvalue())

    if save_path.exists():
        st.success(f'File {uploaded_file.name} is successfully saved!')


    loader = PyPDFLoader(save_folder+uploaded_file.name)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    print(f"# of documents = {len(docs)}")
    
    db = PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        pre_delete_collection=True
)
    