from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.utilities import GraphQLAPIWrapper
from langchain.llms import VertexAI
import streamlit as st 

llm = VertexAI()
from PIL import Image
from streamlit_chat import message

image = Image.open('logo1.png')
new_image = image.resize((75, 50))

#st.image(new_image)
st.title('LBG GPT')
prompt = st.text_input('Search your transactions') 
st.session_state['generated'] = []
st.session_state['past'] = []
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
      }
    }
    }
  
"""
suffix = "Search for the transactions in London for account number 10003"

def get_prompt():
    try:
        response = agent.run(prompt + ql)
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
    