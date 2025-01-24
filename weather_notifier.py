import requests
import time  # Import time module
from sms_sender import send_sms  # Assuming the send_sms function is defined already
from db_manager import users_collection  # Import users_collection from db_manager

# OpenWeather API Key
API_KEY = '632193275a1c59582d036295c2003b0e' 

def get_weather_alert(location):
    """Fetch the weather information and return an alert if conditions are severe."""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={632193275a1c59582d036295c2003b0e}&units=metric'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.text  

            if 'weather' in data:
                start = data.index('"weather"')  # Find where the weather data starts
                end = data.index('"main"')  # Find where the main weather type ends
                weather_condition = data[start:end].split(":")[1].strip().replace('"', '')

                start = data.index('"temp"')  # Find where the temperature data starts
                end = data.index('"feels_like"')  # Find where the temperature data ends
                temperature = float(data[start:end].split(":")[1].strip())

                # Check for weather conditions that may indicate a disaster or extreme weather
                alert = None
                if weather_condition in ['Thunderstorm', 'Drizzle', 'Rain', 'Snow', 'Mist']:
                    alert = f"ALERT: Severe weather warning! Current conditions: {weather_condition}, Temperature: {temperature}°C"
                elif temperature > 40:
                    alert = f"ALERT: Extreme heat warning! Current temperature: {temperature}°C"
                elif temperature < 0:
                    alert = f"ALERT: Freezing temperatures! Current temperature: {temperature}°C"

                return alert

            else:
                return "Weather information is unavailable."

        else:
            return "Could not fetch weather data. Please try again later."

    except Exception as e:
        return f"Error: {str(e)}"


def start_monitoring(phone):
    """Start disaster monitoring for a specific user."""
    user = users_collection.find_one({"phone": phone, "is_active": True})
    if not user:
        print("Error: User not activated.")
        return

    location = user['location']
    print(f"Monitoring started for {phone} in {location}.")

    while True:
        alert = get_weather_alert(location)  # Fetch weather alert
        if alert:
            send_sms(phone, alert)  # Send alert via SMS
            print(f"Alert sent to {phone}: {alert}")
        time.sleep(60)  # Check every minute
