import requests

def get_weather_info(city):
    # Construct the URL for the OpenWeatherMap API
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=98246bf2e267e0fbc581c7466eff124f"

    # Send a GET request to the API and parse the JSON response
    response = requests.get(URL).json()

    # Extract the relevant information from the response
    temp_celsius = response['main']['temp'] - 273.15
    wind_speed = response['wind']['speed']
    latitude = response['coord']['lat']
    longitude = response['coord']['lon']
    description = response['weather'][0]['description']

    # Create a formatted string with the weather information
    weather_info = f'Temperature: {round(temp_celsius,2)}°C\nWind Speed: {wind_speed} m/s\nLatitude: {latitude}\nLongitude: {longitude}\nDescription: {description}'

    return {
            'status': 1,
            'response': weather_info
        }

# # Get the city name from the user
# CITY = input("Enter the place: ")

# # Call the function and print the weather information
# weather_info = get_weather_info(CITY)
# print(weather_info['response'])