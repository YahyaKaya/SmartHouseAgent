import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
import datetime
import ddgs

from server import MQTTServer


@function_tool()
async def get_time(context: RunContext) -> str:
    """
    Get the current date and time when asked.
    """
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y at %H:%M:%S")

@function_tool()
async def get_weather(
    context: RunContext,
    city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"{city} şehri için hava durumu: {response.text.strip()}")
            return response.text.strip()   
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"{city} şehri için veri alınamadı."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"{city} için veri almaya çalışırken bir hata oluştu." 

@function_tool()
async def search_web(context: RunContext, query: str) -> dict:
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"query: {query} results: {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"{query} için araştırma yaparken bir hata oluştu."    






async def mqtt_command_handler(topic, payload):
    print("Gelen:", topic, payload)


mqtt_server = MQTTServer(on_command_callback=mqtt_command_handler)
mqtt_server.connect()

@function_tool()
async def close_curtain(context: RunContext) -> str:
    """
    Close the curtains when requested.
    """
    mqtt_server.publish("home/curtain", "OFF")


@function_tool()
async def open_curtain(context: RunContext):
    """
    Open the curtains when requested
    """
    mqtt_server.publish("home/curtain", "ON")

@function_tool
async def turn_on_yellow_light(context: RunContext):
    """
    Turn on the yellow light when requested
    """
    mqtt_server.publish("home/yellow", "ON")

@function_tool
async def turn_off_yellow_light(context: RunContext):
    """
    Turn off the yellow light when requested
    """
    mqtt_server.publish("home/yellow", "OFF")
    
@function_tool
async def turn_on_navy_light(context: RunContext):
    """
    Turn on the navy light when requested
    """
    mqtt_server.publish("home/navy", "ON")
    
@function_tool
async def turn_off_navy_light(context: RunContext):
    """
    Turn off the navy light when requested
    """
    mqtt_server.publish("home/navy", "OFF")
    