import os
import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain import hub
from dotenv import load_dotenv

load_dotenv()

os.environ['GROQ_API_KEY'] =  os.getenv("GROQ_API_KEY")

search=DuckDuckGoSearchRun(name="Search")
prompt=hub.pull("hwchase17/react")
  
st.title("🔎 LangChain - Chat with search")
 
if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assisstant","content":"Hi,I'm a chatbot who can search the web. How can I help you?"} 
    ]
 
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])
 
if prompt:=st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)
 
    model=ChatGroq(model_name="Llama3-8b-8192",streaming=True)
    tools=[search]
    agent = create_react_agent(model, tools, prompt)
 
    search_agent = AgentExecutor(agent=agent, tools=tools)
 
    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response=search_agent.invoke(st.session_state.messages,callbacks=[st_cb]) 
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)