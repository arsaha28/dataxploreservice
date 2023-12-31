import streamlit as st
from typing import List, Tuple
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import VertexAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import VertexAI
from PIL import Image

st.title("DataExploreService")

embeddings = VertexAIEmbeddings()
llm = VertexAI()

COLLECTION_NAME = "soe12.help_topics"
CONNECTION_STRING = PGVector.connection_string_from_db_params(
     driver="psycopg2",
     host="localhost",
     port=int(5432),
     database="arnabsaha",
     user="arnabsaha",
     password='',
 )

    
store = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
)

#qa = RetrievalQA.from_chain_type(
#    llm=llm, 
#    chain_type='stuff',
#    retriever=db.as_retriever(),
#)

retriever = store.as_retriever(search_type="similarity", search_kwargs={"k": 2})

qa = RetrievalQA.from_chain_type(
    llm= llm, chain_type="stuff", retriever=retriever, return_source_documents=False
)
def generate_response(input_text):
    print(input_text)   
    result = qa({"query": input_text})
    st.info(result["result"])


with st.form("my_form"):
    text = st.text_area("Enter text:", "How can I help you?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
    