"""
Eve: A Minimal Function-Calling AI Assistant using LLaMA 3B

Overview:
---------
Eve is a lightweight AI assistant that understands natural language,
extracts intent, and dynamically routes user queries to appropriate
Python functions using a function-calling mechanism.

Powered by the LLaMA 3 3B model via Ollama, Eve can:
- Fetch weather data for any city
- Retrieve news on a specific topic
- Perform Google-like searches

Key Features:
-------------
✓ Natural language understanding via LLaMA 3
✓ Simple function registry for easy extensibility
✓ Clear separation of prompt logic and execution
✓ Designed for education, demos, and blog publishing

Use Cases:
----------
Eve is ideal for:
- Learning about function-calling in LLMs
- Prototyping intelligent assistants
- Building educational blog content
- Demonstrating LLM-based input routing
Author: Piyush Bhatt
Project: EVE – Function Calling Assistant
"""


# ------------------------------ Imports ------------------------------
# Importing custom error handler and output formatting utilities
from handler import ErrorHandler, output_json

# Importing the requests library for making HTTP requests to external APIs
import requests

# Importing os module to interact with the operating system (e.g., environment variables, paths)
import os,ollama,json ,re

# Importing BeautifulSoup for parsing and extracting data from HTML (used in web scraping)
from bs4 import BeautifulSoup
from dotenv import load_dotenv
# Importing date and timedelta for working with and calculating date ranges (used in news filtering, etc.)
from datetime import date, timedelta

load_dotenv()
pattern = r"\{(?:[^{}]|(?=\{[^{}]*\}))*\}" #to match json


# Weather Module:
# --------------
# Inherits from ErrorHandler and provides weather-related functionality
# using the WeatherAPI. It fetches current conditions and daily forecast
# for a given location and formats the output into a human-readable string.
class Weather(ErrorHandler):
    def __init__(self):
        super().__init__()
        self._description = "Fetches current weather and forecast for a given location using WeatherAPI."
        self._api_key = os.getenv('WEATHER_API_KEY')
        self._url = "http://api.weatherapi.com/v1/forecast.json?key={}&q={}&aqi=no"

    def _fetch_weather(self, location):
        url = self._url.format( self._api_key, location)
        data = requests.get(url)
        if data.status_code == 200:
            return data.json()
        raise RuntimeError(f"Weather Module doesn't work with status code {data.status_code} and content {data.json()['error']}")

    def _format_data(self, data):
        location = data['location']['name']
        
        condition = data['current']['condition']['text']
        temp = data['current']['temp_c']
        feels_like = data['current']['feelslike_c']
        humidity = data['current']['humidity']
        
   
        forecast_today = data['forecast']['forecastday'][0]['day']
        max_temp = forecast_today['maxtemp_c']
        min_temp = forecast_today['mintemp_c']
        chance_of_rain = forecast_today.get('daily_chance_of_rain', 0)
        forecast_condition = forecast_today['condition']['text']

        return (
            f"Currently, it's {condition.lower()} in {location} with {temp}°C (feels like {feels_like}°C) "
            f"and humidity at {humidity}%. "
            f"Today's forecast: {forecast_condition.lower()}, highs of {max_temp}°C and lows of {min_temp}°C. "
            f"Chance of rain is {chance_of_rain}%."
        )


    def main(self, location="india"):
        data = self._format_data(self._fetch_weather(location))
        if isinstance(data,dict) and data.get('success') is False:
            return output_json(success=False,result=data.get('error'))
        return output_json(success=True,result=data)
    
# News Module:
# ------------
# This class connects to NewsAPI and fetches the latest news articles 
# on a given topic. It extracts and formats the top 10 headlines 
# and descriptions into a string suitable for output.
class News(ErrorHandler):
    def __init__(self):
        super().__init__()
        self._description = "Fetches the latest news articles based on a specific topic using NewsAPI."
        self._api_url="https://newsapi.org/v2/everything?q={}&from={}&sortBy=publishedAt&apiKey={}"
        self._api_key=os.getenv('NEWS_API_KEY')
    
    def _news_format(self,news):
        return f"*{news['source']['name']}*\n {news['description']}\nLink:- {news['url']}\n"
        
    def _filter_data(self,data):
        data=data['articles']
        return "\n".join(list(map(self._news_format,data[:10])))
            
    def _fetch_news(self, topic):
        url = self._api_url.format(topic,(date.today()-timedelta(days=1)).isoformat(), self._api_key)
        response = requests.get(url)
        if response.status_code == 200:
            return self._filter_data(response.json())
        try:
            error_message = response.json().get('message', 'No message provided')
        except Exception:
            error_message = response.content.decode('utf-8')

        raise RuntimeError(
            f"News API Error:\n"
            f"Topic: '{topic}'\n"
            f"Status Code: {response.status_code}\n"
            f"Message: {error_message}"
    )


    def main(self,topic="india"):
        data=self._fetch_news(topic)
        if isinstance(data,dict) and data.get('success') is False:
            return output_json(success=False,result=data.get('error'))
        return output_json(success=True,result=data)
    
    
# Google Search Module:
# ---------------------
# Performs a Google search scoped to Wikipedia using Google's Custom Search API.
# After retrieving the top result, it scrapes the textual content of the Wikipedia page
# using BeautifulSoup and returns a concise text summary.
class GoogleSearch(ErrorHandler):
    def __init__(self):
        super().__init__()
        self._description = "Performs a Google search and scrapes Wikipedia content for the search topic. use when the user explcitly asks for google search"
        self._api_key = os.getenv("SEARCH_API_KEY")
        self._cx = os.getenv("SEARCH_CSX_ID")
        
        
    def _scrape_webpage(self,data):
        soup=BeautifulSoup(data,'html.parser')
        results = soup.find('div', id='mw-content-text')
        results=results.find_all('p')
        results=list(map(lambda x:x.text ,results))
        return '\n'.join([item for item in results if len(item)>50])
        
        
        
    def _get_webpage(self,link):
        response=requests.get(link)
        return self._scrape_webpage(response.content.decode('utf-8'))
    
    def _do_google_search(self, topic):
        url = f"https://www.googleapis.com/customsearch/v1?key={self._api_key}&cx={self._cx}&q={topic} wikipedia"
        response = requests.get(url)
        if response.status_code==200:
            return self._get_webpage(response.json()['items'][0]['formattedUrl'])
        else:
            raise RuntimeError(f"Error in Google search with status code : {response.status_code} Message : {response.content.decode('utf-8')}")
    
    def main(self, topic=''):
        data=self._do_google_search(topic)
        if isinstance(data,dict) and data.get('success') is False:
            return output_json(success=False,result=data.get('error'))
        return output_json(success=True,result=data)




# ------------------------------ Initialize and check module working ------------------------------


# Instantiate the GoogleSearch module for performing Google + Wikipedia-based searches
google = GoogleSearch()

# Instantiate the Weather module for fetching current weather and forecast data
weather = Weather()

# Instantiate the News module to fetch recent news articles on any given topic
news = News()

# Execute a Google search for "Elon Musk" and return Wikipedia summary
print(google.main('elon musk'))

# Get current weather and forecast for "Chandigarh"
print(weather.main('chandigarh'))

# Retrieve top recent news related to "terrorist" from NewsAPI
print(news.main('terrorist'))



class Eve(ErrorHandler):
    """
    Eve is an intelligent AI assistant class that routes user queries
    to appropriate tools (weather, news, search) using system prompts
    and LLM reasoning, then processes and returns helpful responses.
    """

    def __init__(self):
        """
        Initialize Eve assistant by setting up:
        - Model name from environment
        - Tool routing prompt
        - Dictionary of available tool functions
        - Responder prompt to format final response
        """
        super().__init__()
        print("Initializing Eve")
        self.MODEL = os.getenv('MODEL')
        self.SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT_TOOL')
        self.SYSTEM_PROMPT_RESPONDER = os.getenv('SYSTEM_PROMPT_RESPONDER')

        # Map tool names to their corresponding handler functions
        self.TOOLS = {
            'get_weather': weather.main,
            'get_news': news.main,
            'get_search': google.main
        }

        print("System prompt : ", self.SYSTEM_PROMPT)
        print("System prompt responder : ", self.SYSTEM_PROMPT_RESPONDER)

    def _call_module(self, tool_dict, user_input=''):
        """
        Internal method to call the appropriate tool function.

        Parameters:
        - tool_dict (dict): Dictionary with 'tool' and 'input'
        - user_input (str): Optional fallback input

        Returns:
        - dict: Response from the tool
        """
        tool_name = tool_dict.get('tool')
        input_value = tool_dict.get('input', user_input)

        if tool_name in self.TOOLS:
            tool_func = self.TOOLS[tool_name]
            response = tool_func(input_value)
            return response
        else:
            return {"success": False, "data": "unknown function called"}

    def _generate_response(self, tool_response, user_text, data=''):
        """
        Uses the responder system prompt to generate a final response
        based on user input and tool output.

        Parameters:
        - tool_response (bool): Tool success flag
        - user_text (str): Original user input
        - data (str): Data returned from the tool
        """
        response = ollama.chat(self.MODEL, [
            {"role": "system", "content": self.SYSTEM_PROMPT_RESPONDER},
            {"role": "user", "content": f"User Input :-\n{user_text}\nTool Response :-\n{tool_response} Data :- {data if len(data) < 300 else 'Data is too long just say heres some additional info'}"}
        ], stream=True)

        text = ""
        for message in response:
            token = message['message']['content']
            text += token
            print(token, end="", flush=True)

        print("\n```\nData :-", data[:1000], '\n')

    def _extract_json(self, generated_text, user_text=''):
        """
        Attempts to extract a JSON tool call from the LLM output and
        route it to the correct function.

        Parameters:
        - generated_text (str): Text returned by initial LLM prompt
        - user_text (str): Original user input
        """
        pattern = r'\{.*?"tool"\s*:\s*".*?".*?\}'  # Regex to extract JSON object with "tool"
        match = re.search(pattern, generated_text)

        if match:
            tool = json.loads(match.group())
            print("Tool :-", tool)
            response = self._call_module(tool, user_text)
            print('Response : ', response)
            succes = response['success']
            data = response['data']
            self._generate_response(succes, user_text, data)
        else:
            print("Medusa :-", generated_text)

    def run(self):
        """
        Starts an interactive chat loop with Eve.
        On each user input:
        - LLM is queried for whether a tool is needed
        - If a tool is called, the result is used to generate a final reply
        - Loop continues until user types 'break'
        """
        while True:
            print()
            user_input = input('Chat with Eve :-')
            if user_input == 'break':
                break

            text = ""
            response = ollama.chat(self.MODEL, [
                {'role': 'system', 'content': self.SYSTEM_PROMPT},
                {'role': 'user', 'content': user_input}
            ], stream=True)

            for message in response:
                token = message['message']['content']
                print(token, end="", flush=True)
                text += token

            print('\n')
            self._extract_json(text, user_input)


# Launch Eve assistant
eve = Eve()
print("Eve Started Successfully :-\n")
eve.run()
