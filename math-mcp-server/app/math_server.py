# FastAPI와 MCP 관련 라이브러리를 가져옵니다.
import math
import requests
from mcp.server.fastmcp import FastMCP

# MCP 인스턴스를 생성합니다.
mcp = FastMCP("Math")

# 더하기 연산을 정의합니다.
@mcp.tool()
def add(a: float, b: float) -> float:
    """
    두 숫자를 더한 결과를 반환합니다.

    Args:
        a (float): 첫 번째 숫자
        b (float): 두 번째 숫자

    Returns:
        float: 두 숫자를 더한 결과
    """
    return a + b

# 빼기 연산을 정의합니다.
@mcp.tool()
def subtract(a: float, b: float) -> float:
    """
    첫 번째 숫자에서 두 번째 숫자를 뺀 결과를 반환합니다.

    Args:
        a (float): 첫 번째 숫자
        b (float): 두 번째 숫자

    Returns:
        float: 첫 번째 숫자에서 두 번째 숫자를 뺀 결과
    """
    return a - b

# 곱하기 연산을 정의합니다.
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    두 숫자를 곱한 결과를 반환합니다.

    Args:
        a (float): 첫 번째 숫자
        b (float): 두 번째 숫자

    Returns:
        float: 두 숫자를 곱한 결과
    """
    return a * b

# 나누기 연산을 정의합니다.
@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    첫 번째 숫자를 두 번째 숫자로 나눈 결과를 반환합니다.
    0으로 나누는 경우 예외를 발생시킵니다.

    Args:
        a (float): 첫 번째 숫자
        b (float): 두 번째 숫자

    Returns:
        float: 첫 번째 숫자를 두 번째 숫자로 나눈 결과

    Raises:
        ValueError: 두 번째 숫자가 0인 경우 예외를 발생시킵니다.
    """
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b

# local : mcp.run(transport="stdio")
if __name__ == "__main__":
    print("MCP Server is running on SSE transport at port 8000.")
    print("You can access the server at http://localhost:8000")
    print("Server is ready to handle requests...")
    
    # Run the MCP server with SSE transport
    mcp.run(transport="sse", port=8000)