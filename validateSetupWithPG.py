#use pg db as knowledge store without graphql
import os 
import streamlit as st 

from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain



from langchain.llms import VertexAI
from PIL import Image
from streamlit_chat import message

st.title('DXPloreService')
prompt = st.text_input('Search your transactions') 

# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:@localhost:5432/arnabsaha?options=-csearch_path%3Dsoe",
)

# Create db chain
QUERY = """
Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

{question}
"""
llm = VertexAI()

# Setup the database chain
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
st.session_state['generated'] = []
st.session_state['past'] = []
def get_prompt():
    try:
        question = QUERY.format(question=prompt)
        response = db_chain.run(question)
        st.write(response) 
        st.session_state.past.append(prompt)
        st.session_state.generated.append(response)
        

    except Exception as e:
            print(e)


if prompt: 
    get_prompt()
    
    with st.expander('Conversation History'): 
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    