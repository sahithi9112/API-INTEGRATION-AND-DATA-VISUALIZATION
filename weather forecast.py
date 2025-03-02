import requests
import matplotlib.pyplot as plt
from datetime import datetime


API_KEY = '7293d905fe913688c3cc1059feb32fa6'  
city = 'London'
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'

# Function to fetch weather data
def fetch_weather_data(city):
    # Get the weather data for the city
    geo_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(geo_url)
    
    if response.status_code != 200:
        print(f"Error fetching city data: {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    lat = data['coord']['lat']
    lon = data['coord']['lon']
    
    # Fetch 3-hour forecast data for the next 5 days
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching forecast data: {response.status_code} - {response.text}")
        return None
    
    return response.json()

# Function to visualize the data
def visualize_weather(data):
    dates = []
    temperatures = []
    
    for entry in data['list']:
        date = datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        dates.append(date)
        temperatures.append(temp)
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temperatures, marker='o')
    plt.title(f'5-Day Weather Forecast for {city}')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == '__main__':
    weather_data = fetch_weather_data(city)
    if weather_data:
        visualize_weather(weather_data)
