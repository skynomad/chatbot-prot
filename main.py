# mcp_client.py
import os
import asyncio
import logging

# MCP 관련 모듈 임포트
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from comm.config import Config
from comm.logger_manager import LoggerManager

# 로깅 설정
logger = LoggerManager.get_logger("main", level=logging.DEBUG)


# GROQ API 키 설정
os.environ["GROQ_API_KEY"] = Config.GROQ_API_KEY

# OpenAI API 키 설정
#os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY

# ChatGroq 모델 사용
model = ChatGroq(model="llama3-8b-8192", temperature=0)
#model = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # 대체 모델 (주석 처리됨)

# MCP 서버 실행을 위한 파라미터 설정
server_params = StdioServerParameters(
    command="python",
    args=["D:\\workspace\\streamlit-workspace\\chat_prot\\math-mcp-server\\math_server_stdio.py"]  
)

# 비동기 함수: MCP 클라이언트를 실행하고 에이전트를 통해 작업 수행
async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 세션 초기화
            await session.initialize()
            logger.info("MCP Session Initialized.")  # 초기화 완료 메시지 출력

            # MCP 도구 로드 (세션을 통해 사용 가능한 도구 목록 가져오기)
            tools = await load_mcp_tools(session)
            logger.debug("================================================================")
            logger.debug(f"Loaded Tools: {[tool.name for tool in tools]}")  # 로드된 도구 이름 출력
            logger.debug("================================================================")

            # ReAct 에이전트 생성 (모델과 도구를 사용)
            agent = create_react_agent(model, tools)
            logger.info("ReAct Agent Created.")  # 에이전트 생성 완료 메시지 출력
            
            # 에이전트에 사용자 쿼리를 전달하여 작업 수행
            logger.info(f"Invoking agent with query")
            try:
                # 요청 데이터 확인
                query = {
                    "messages": [
                        ("user", "What is (7+9)x17, then give me sine of the output recieved and then tell me What's the weather in Toronto, Canada?")
                    ]
                }
                logger.debug(f"Request Query Data: {query}")

                # 에이전트 호출
                response = await agent.ainvoke(query)

                # 응답 확인
                logger.debug(f"Agent Response: {response}")
            except Exception as error:
                # 에러 디버깅
                logger.error(f"Error during agent invocation: {error}")
                return None

            logger.info("Agent invocation complete.")  # 작업 완료 메시지 출력

            # 에이전트 응답의 마지막 메시지(최종 결과)를 반환
            try:
                final_response = response["messages"][-1].content
                logger.debug(f"Final Response: {final_response}")
                return final_response
            except KeyError as key_error:
                logger.error(f"Response structure is invalid: {key_error}")
                return None

# 표준 Python 진입점
if __name__ == "__main__":
    logger.info("Starting MCP Client...")
    result = asyncio.run(run_agent())
    if result:
        logger.info("Agent Final Response:")
        logger.info(result)
    else:
        logger.error("Failed to get a valid response from the agent.")
