import requests

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # You can change this to "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            print(f"Error: {data['message']}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def display_weather(weather_data):
    if weather_data:
        print("\nWeather Information:")
        print(f"Location: {weather_data['name']}, {weather_data['sys']['country']}")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Description: {weather_data['weather'][0]['description']}")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
    else:
        print("Weather data not available.")

if __name__ == "__main__":
    # Replace 'your_api_key' with the API key obtained from OpenWeatherMap
    api_key = 'your_api_key'

    # Get user input for the city
    city = input("Enter the city name: ")

    # Get weather data
    weather_data = get_weather(api_key, city)

    # Display weather information
    display_weather(weather_data)
