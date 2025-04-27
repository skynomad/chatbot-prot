# 필요한 라이브러리를 가져옵니다.
import os  # 환경 변수를 가져오기 위한 라이브러리
import logging  # 로깅을 위한 라이브러리
import requests  # HTTP 요청을 보내기 위한 라이브러리

from typing import List
from mcp.server.fastmcp import FastMCP
from mcp.server import Server

from config import Config
from logger_manager import LoggerManager

# 로깅 설정
logger = LoggerManager.get_logger("weather_server", level=logging.DEBUG)

# MCP 서버 인스턴스를 생성합니다.
# "Weather"는 MCP 서버의 이름입니다.
mcp = FastMCP("Weather")

# 날씨 정보를 가져오는 도구를 정의합니다.
@mcp.tool()
async def get_weather(location: str) -> str:
    """
    주어진 위치의 날씨 정보를 반환합니다. (Echo)

    Args:
        location (str): 날씨 정보를 가져올 위치의 이름

    Returns:
        str: 위치의 날씨 정보 (예: "The weather in {location} is sunny")
    """
    logger.debug(f"Fetching weather for location: {location}")
    return f"The weather in {location} is sunny"

# 특정 도시의 날씨 정보를 가져오는 도구를 정의합니다.
@mcp.tool()
async def get_city_weather(city: str) -> dict:
    """
    WeatherAPI.com을 사용하여 주어진 도시의 현재 날씨 정보를 가져옵니다.
    도시 이름, 온도(섭씨), 날씨 상태를 포함한 정보를 반환합니다.

    Args:
        city (str): 날씨 정보를 가져올 도시의 이름

    Returns:
        dict: 도시의 날씨 정보
            - city (str): 도시 이름
            - region (str): 지역 이름
            - country (str): 국가 이름
            - temperature_C (float): 현재 온도 (섭씨)
            - condition (str): 현재 날씨 상태
    """
    logger.debug(f"Server received weather request: {city}")  # 요청 로그를 출력합니다.

    # API 요청시 필요한 인수값 정의
    payload = "?q=" + city + "&" + "appid=" + Config.OPEN_WEATHER_API_KEY  #"lang=kr" 옵션을 추가하면 날씨설명을 한글로 받을 수 있음.
    url = Config.OPEN_WEATHER_API_URL + payload
    logger.debug(f"Open Weather Request URL: {url}")  # 요청 URL을 로그에 출력합니다.

    # WeatherAPI.com의 API URL을 구성합니다.
    #url = f"http://api.weatherapi.com/v1/current.json?key={Config.WEATHER_API_KEY}&q={city}"

    # HTTP GET 요청을 보냅니다.
    response = requests.get(url)

    # 요청이 실패한 경우 에러 메시지를 반환합니다.
    if response.status_code != 200:
        return {"error": f"Failed to fetch weather for {city}. reason: {response.status_code} {response.text}"}

    # API 응답 데이터를 JSON 형식으로 파싱합니다.
    weather_datas = response.json()

    # Refer : https://m.blog.naver.com/chgy2131/222469207294
    logging.debug("========================================================")
    logging.debug("도시명 : %r" % weather_datas['name'])
    logging.debug("========================================================")
    logging.debug("날씨 : %r" % weather_datas['weather'][0]['main'])
    logging.debug("날씨상세 : %r" % weather_datas['weather'][0]['description'])
    logging.debug("아이콘 : %r  (사이트참조: https://openweathermap.org/weather-conditions)" % weather_datas['weather'][0]['icon'])
    logging.debug("========================================================")
    logging.debug("현재온도 : %r" % str(int(weather_datas['main']['temp'])-273.15))
    logging.debug("체감온도 : %r" % str(int(weather_datas['main']['feels_like'])-273.15))
    logging.debug("최저온도 : %r" % str(int(weather_datas['main']['temp_min'])-273.15))
    logging.debug("최고온도 : %r" % str(int(weather_datas['main']['temp_max'])-273.15))
    logging.debug("습도 : %r" % weather_datas['main']['humidity'])
    logging.debug("기압 : %r" % weather_datas['main']['pressure'])
    logging.debug("========================================================")
    logging.debug("가시거리 : %r" % weather_datas['visibility'])
    logging.debug("풍속 : %r" % weather_datas['wind']['speed'])
    logging.debug("풍향 : %r" % weather_datas['wind']['deg'])
    logging.debug("========================================================")
    #print("강수량 : %r (시간당)" % weather_datas['rain']['1h']) #비 올때만 생김
    logging.debug("========================================================")
    logging.debug("구름 : %r " % weather_datas['clouds']['all'])
    logging.debug("일출 : %r " % weather_datas['sys']['sunrise'])
    logging.debug("일몰 : %r " % weather_datas['sys']['sunset'])
    logging.debug("========================================================")

    # 날씨 정보를 반환합니다.
#    return {
#        "city": data["location"]["name"],  # 도시 이름
#        "region": data["location"]["region"],  # 지역 이름
#        "country": data["location"]["country"],  # 국가 이름
#        "temperature_C": data["current"]["temp_c"],  # 현재 온도 (섭씨)
#        "condition": data["current"]["condition"]["text"]  # 현재 날씨 상태
#    }

    return {
        "city": weather_datas['name'],  # 도시 이름
        "region": weather_datas['sys']['country'],  # 지역 이름
        "country": weather_datas['sys']['country'],  # 국가 이름
        "temperature_C": str(int(weather_datas['main']['temp'])-273.15),  # 현재 온도 (섭씨)
        "condition": weather_datas['weather'][0]['description']  # 현재 날씨 상태
    }

# MCP 서버를 실행합니다.
if __name__ == "__main__":
    # SSE(Server-Sent Events) 방식으로 MCP 서버를 실행하며, 포트는 7000번으로 설정합니다.
    mcp.run(transport="sse", port=7000)