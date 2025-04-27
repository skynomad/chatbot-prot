# mcp_client.py
import getpass
import os
import asyncio
import logging

from mcp import ClientSession, StdioServerParameters, SseServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from comm.config import Config

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_client")

# Set your API key (replace with your actual key or use environment variables)

if "GROQ_API_KEY" not in os.environ:
    #os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    os.environ["GROQ_API_KEY"] = Config.GROQ_API_KEY

# Set your OpenAI API key (replace with your actual key or use environment variables)
#os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY

# Initialize the LLM model
#model = ChatGroq(model="llama3-8b-8192", temperature=0)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

# model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

server_params = StdioServerParameters(
    command="python", # Command to execute
    args=["mcp_server.py"] # Arguments for the command (our server script)
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("MCP Session Initialized.")
            tools = await load_mcp_tools(session)
            print("=====================================================")
            print(f"Loaded Tools: {[tool.name for tool in tools]}")
            print("=====================================================")
            
            agent = create_react_agent(llm, tools)
            print("ReAct Agent Created.")
            
            print(f"Invoking agent with query")
            try:
                response = await agent.ainvoke({
                    "messages": [("user", "What is (7+9)x17, then give me sine of the output recieved and then tell me What's the weather in Toronto, Canada?")]
                })
            except Exception as e:
                logger.error(f"Error during agent invocation: {e}")
                return {"messages": [{"content": "An error occurred during the agent invocation."}]}
                
            print("Agent invocation complete.")
            # Return the content of the last message (usually the agent's final answer)
            return response["messages"][-1].content

# Standard Python entry point check
if __name__ == "__main__":
# Run the asynchronous run_agent function and wait for the result
    print("Starting MCP Client...")
    result = asyncio.run(run_agent())
    print("\nAgent Final Response:")
    print(result)
