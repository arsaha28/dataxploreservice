from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.utilities import GraphQLAPIWrapper
from langchain.llms import VertexAI
import streamlit as st 
from json2html import *
from streamlit_chat import message
from PIL import Image

llm = VertexAI(temparature=0)
image = Image.open('abhishkar.png')
new_image = image.resize((160, 65))
st.title("DXPloreService")

#st.image(new_image)
tools = load_tools(
    ["graphql"],
    graphql_endpoint="http://localhost:5000/graphql",
    llm=llm,
)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
ql = """  
    allTransactions(condition: {}){
    edges {
      node {
        id
        merchantCity
        merchantName
        sortcode
        transactionDate
        amount
        accountNumber
      }
    }
    }
  
"""
def get_prompt(text):
    try:
        response = agent.run(text + ql)
        st.info(response)
    except Exception as e:
            print(e)

with st.form("my_form"):
    text = st.text_area("Enter text:", "How can I help you?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        get_prompt(text)
    