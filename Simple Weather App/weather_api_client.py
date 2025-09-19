import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout

# stock
api_key = "adab8742d6fcb59fe00fd4ee8cc43792" # OpenWeatherMap

err_msgs = {
    "ConnectionError": "Could not connect to server. Please try again later.",
    "Timeout": "The request timed out. Please try again later.",
    "HTTP401": "Invalid API Key. Please check your key.",
    "HTTP404": "City not found. Maybe there was a typo?"
}

# get weather data for a city
def get_weather_data(city, key=api_key, units="metric"):
    """
    Get weather data for a city using OpenWeatherMap's API

    Args:
        city (str): name of city to get weather for    
        key (str): API key (provided by default)
        units (str): Units of measurement (metric -> Celsius / imperial -> Fahrenheit)

    Returns:
        dict: JSON API data parsed into Python dictionary
        str: Various error messages
    """

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": key,
        "units": units
    }
    
    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()
    except HTTPError as http_e:
        if response.status_code == 401:
            return f"{err_msgs['HTTP401']}"
        elif response.status_code == 404:
            return f"{err_msgs['HTTP404']}"
        else:
            return f"Error: {http_e}"
    except ConnectionError:
        return f"Error: {err_msgs['ConnectionError']}"
    except Timeout:
        return f"Error: {err_msgs['Timeout']}"
    return response.json()