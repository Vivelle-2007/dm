import requests
import time  
from sms_sender import send_sms  
from db_manager import users_collection 


API_KEY = '632193275a1c59582d036295c2003b0e' 

def get_weather_alert(location):
    """Fetch the weather information and return an alert if conditions are severe."""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={632193275a1c59582d036295c2003b0e}&units=metric'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.text  

            if 'weather' in data:
                start = data.index('"weather"')  
                end = data.index('"main"')  
                weather_condition = data[start:end].split(":")[1].strip().replace('"', '')

                start = data.index('"temp"')  
                end = data.index('"feels_like"')  
                temperature = float(data[start:end].split(":")[1].strip())

              
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
        alert = get_weather_alert(location)  
        if alert:
            send_sms(phone, alert)  
            print(f"Alert sent to {phone}: {alert}")
        time.sleep(60)  
