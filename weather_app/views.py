import datetime

import requests
from django.shortcuts import render
import os
# Create your views here.
def index(request):
    #API_KEY = os.getenv("API_KEY")
    API_KEY= "3c7ca3a08e9a3455816efeb6a7c863bf"
    base_url = "https://api.openweathermap.org/data/2.5"
    current_weather_url = f"{base_url}/weather?q={{}}&appid={{}}"
    forecast_url = f"{base_url}/forecast?q={{}}&appid={{}}"
   
    city1 = request.POST.get("city1", "Dakar")
    city2 = request.POST.get("city2", "Paris")

    weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)
    if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
    else:
            weather_data2, daily_forecasts2 = None, None

    context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2

        }
    return render(request, "index.html", context)
    
        
   
        

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city,api_key)).json()
    #lat, lon = response["coord"]["lat"], response["coord"]["lon"]
    forecast_response = requests.get(forecast_url.format(city, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": round(response["main"]["temp"] - 273.15, 2),
        "description": response["weather"][0]["description"],
        "icon": response["weather"][0]["icon"]
    }

    daily_forecasts = []
    for daily_data in forecast_response["daily"][:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
            "min_temp": round(daily_data["temp"]["min"] -273.15, 2),
            "max_temp": round(daily_data["temp"]["max"] -273.15, 2),
            "description": daily_data["weather"][0]["description"],
            "icon": daily_data["weather"][0]["icon"]
        })
    return weather_data, daily_forecasts