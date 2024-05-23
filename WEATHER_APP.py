import requests
import tkinter as tk
from tkinter import ttk

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # You can change the units to "imperial" for Fahrenheit
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        main = weather_data["main"]
        weather_description = weather_data["weather"][0]["description"]
        temperature = main["temp"]
        humidity = main["humidity"]
        return f"Weather in {city}: {weather_description.capitalize()}\nTemperature: {temperature}°C\nHumidity: {humidity}%"
    else:
        return "Error fetching weather data. Please check the city name or API key."

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Weather App")

    # Create a frame for the city entry and button
    city_frame = ttk.LabelFrame(root, text="City")
    city_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Create a variable for the city name
    city_var = tk.StringVar()

    # Create a city entry field
    city_entry = ttk.Entry(city_frame, width=20, textvariable=city_var)
    city_entry.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Create a button to fetch the weather data
    fetch_button = ttk.Button(city_frame, text="Fetch", command=lambda: fetch_weather(city_var.get()))
    fetch_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Create a frame for the weather information
    info_frame = ttk.LabelFrame(root, text="Weather Information")
    info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Create a label to display the weather information
    weather_label = ttk.Label(info_frame, text="")
    weather_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Function to fetch the weather data
    def fetch_weather(city):
        api_key = "Bd5e378503939ddaee76f12ad7a97608"  # Replace with your actual API key
        weather_info = get_weather(city, api_key)
        weather_label.config(text=weather_info)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
