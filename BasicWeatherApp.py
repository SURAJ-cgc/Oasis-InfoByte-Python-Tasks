import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
from PIL import Image, ImageTk
import io

# List of cities for autocomplete
cities = [
    "New York", "London", "Tokyo", "Paris", "Berlin", "Sydney", "Mumbai", "Beijing", "Dubai", "Moscow",
    "Toronto", "São Paulo", "Seoul", "Singapore", "Hong Kong", "Bangkok", "Istanbul", "Rome", "Madrid",
    "Amsterdam", "Vienna", "Zurich", "Stockholm", "Oslo", "Copenhagen", "Helsinki", "Dublin", "Athens",
    "Lisbon", "Warsaw", "Prague", "Budapest", "Bucharest", "Sofia", "Belgrade", "Bratislava", "Ljubljana",
    "Zagreb", "Reykjavik", "Luxembourg", "Monaco", "San Marino", "Vatican City", "Andorra", "Valletta",
    "Nicosia", "Ankara", "Cairo", "Cape Town", "Johannesburg", "Nairobi", "Casablanca", "Algiers", "Tunis",
    "Tripoli", "Khartoum", "Dakar", "Accra", "Lagos", "Abuja", "Luanda", "Windhoek", "Gaborone", "Harare",
    "Lusaka", "Maputo", "Antananarivo", "Port Louis", "Victoria", "Moroni", "Djibouti", "Asmara", "Mogadishu",
    "Addis Ababa", "Kampala", "Kigali", "Bujumbura", "Dodoma", "Lilongwe", "Lome", "Ouagadougou", "Bamako",
    "Conakry", "Freetown", "Monrovia", "Banjul", "Bissau", "Praia", "São Tomé", "Malabo", "Libreville",
    "Brazzaville", "Kinshasa", "Bangui", "Ndjamena", "Yaounde", "Bata", "Douala", "Bujumbura", "Juba",
    "Khartoum", "Asmara", "Djibouti", "Hargeisa", "Bosaso", "Garowe", "Mogadishu", "Kismayo", "Baidoa",
    "Beledweyne", "Jowhar", "Marka", "Baraawe", "Afgooye", "Wanlaweyn", "Qoryooley", "Buurhakaba", "Bardera",
    "Garbahaarey", "Luuq", "Doolow", "Belet Hawo", "El Wak", "Mandera", "Wajir", "Garissa", "Hola", "Malindi",
    "Lamu", "Mombasa", "Voi", "Machakos", "Nairobi", "Thika", "Nyeri", "Nanyuki", "Meru", "Embu", "Kitui",
    "Machakos", "Makueni", "Kajiado", "Narok", "Kericho", "Bomet", "Nakuru", "Eldoret", "Kitale", "Kakamega",
    "Kisumu", "Homabay", "Migori", "Kisii", "Nyamira", "Narok", "Baringo", "Laikipia", "Nyeri", "Kirinyaga",
    "Murang'a", "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans Nzoia", "Uasin Gishu", "Elgeyo-Marakwet",
    "Nandi", "Bungoma", "Busia", "Siaya", "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi"
]

def get_weather():
    city = com.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return
    
    api_key = '253682c0bd759acfb4255d4aa08c3dd7'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract weather data
        temperature_kelvin = data['main']['temp']
        temperature_celsius = temperature_kelvin - 273.15
        temperature_fahrenheit = (temperature_kelvin - 273.15) * 9/5 + 32
        humidity = data['main']['humidity']
        weather_condition = data['weather'][0]['description'].title()
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        country_code = data['sys']['country']
        city_name = data['name']
        sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
        sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])
        icon_code = data['weather'][0]['icon']
        
        # Get weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url, stream=True)
        icon_data = icon_response.content
        icon_image = Image.open(io.BytesIO(icon_data))
        icon_image = icon_image.resize((100, 100), Image.LANCZOS)
        weather_icon = ImageTk.PhotoImage(icon_image)
        
        # Update the result labels with weather information
        city_label.config(text=f"{city_name}, {country_code}")
        temp_label.config(text=f"{temperature_celsius:.1f}°C / {temperature_fahrenheit:.1f}°F")
        condition_label.config(text=weather_condition)
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind: {wind_speed} m/s")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        sunrise_label.config(text=f"Sunrise: {sunrise.strftime('%H:%M:%S')}")
        sunset_label.config(text=f"Sunset: {sunset.strftime('%H:%M:%S')}")
        
        # Update weather icon
        icon_label.config(image=weather_icon)
        icon_label.image = weather_icon  # Keep a reference
        
        # Change background based on temperature
        if temperature_celsius > 30:
            win.config(bg="#FFCCCC")  # Light red for hot
        elif temperature_celsius > 20:
            win.config(bg="#FFFFCC")  # Light yellow for warm
        elif temperature_celsius > 10:
            win.config(bg="#CCFFCC")  # Light green for mild
        else:
            win.config(bg="#CCFFFF")  # Light blue for cold
            
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Connection Error", f"Failed to connect: {e}")
    except KeyError:
        messagebox.showerror("Data Error", "Invalid city name or data format")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def on_key_release(event):
    value = event.widget.get()
    if value:
        matches = [city for city in cities if value.lower() in city.lower()][:10]  # Show max 10 matches
        listbox_update(matches)
    else:
        listbox_update([])

def listbox_update(matches):
    listbox.delete(0, tk.END)
    for match in matches:
        listbox.insert(tk.END, match)
    # Show or hide listbox based on matches
    if matches:
        listbox.place(x=com.winfo_x(), y=com.winfo_y() + com.winfo_height(), 
                      width=com.winfo_width(), height=min(150, len(matches)*20))
    else:
        listbox.place_forget()

def on_select(event):
    if listbox.curselection():
        selected_city = listbox.get(listbox.curselection())
        com.set(selected_city)
        listbox_update([])

def on_enter(event):
    get_weather()

# Create main window
win = tk.Tk()
win.title("Weather Forecast App")
win.geometry("600x500")
win.config(bg="#f0f8ff")
win.resizable(False, False)

# Set app icon
try:
    win.iconbitmap("weather_icon.ico")
except:
    pass  # Use default icon if custom icon not found

# Style configuration
style = ttk.Style()
style.configure("TCombobox", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12, "bold"), background="#4CAF50", foreground="white")

# Title label
title_label = tk.Label(win, text="Weather Forecast", font=("Arial", 24, "bold"), 
                      bg="#f0f8ff", fg="#2c3e50")
title_label.pack(pady=20)

# City selection frame
input_frame = tk.Frame(win, bg="#f0f8ff")
input_frame.pack(pady=10)

# City label and combobox
city_label = tk.Label(input_frame, text="Select City:", font=("Arial", 12), bg="#f0f8ff")
city_label.grid(row=0, column=0, padx=5, pady=5)

com = ttk.Combobox(input_frame, values=cities, font=("Arial", 12), width=30)
com.grid(row=0, column=1, padx=5, pady=5)
com.bind('<KeyRelease>', on_key_release)
com.bind('<Return>', on_enter)

# Listbox for autocomplete suggestions
listbox = tk.Listbox(win, font=("Arial", 12), height=5)
listbox.bind('<<ListboxSelect>>', on_select)

# Search button
search_button = ttk.Button(win, text="Get Weather", command=get_weather)
search_button.pack(pady=10)

# Weather display frame
weather_frame = tk.Frame(win, bg="#e3f2fd", bd=2, relief="groove")
weather_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Weather icon
icon_label = tk.Label(weather_frame, bg="#e3f2fd")
icon_label.pack(pady=10)

# City name
city_label = tk.Label(weather_frame, font=("Arial", 18, "bold"), bg="#e3f2fd")
city_label.pack(pady=5)

# Temperature
temp_label = tk.Label(weather_frame, font=("Arial", 32, "bold"), bg="#e3f2fd")
temp_label.pack(pady=10)

# Weather condition
condition_label = tk.Label(weather_frame, font=("Arial", 16), bg="#e3f2fd")
condition_label.pack(pady=5)

# Details frame
details_frame = tk.Frame(weather_frame, bg="#e3f2fd")
details_frame.pack(pady=10)

# Humidity
humidity_label = tk.Label(details_frame, font=("Arial", 12), bg="#e3f2fd", anchor="w")
humidity_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Wind speed
wind_label = tk.Label(details_frame, font=("Arial", 12), bg="#e3f2fd", anchor="w")
wind_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Pressure
pressure_label = tk.Label(details_frame, font=("Arial", 12), bg="#e3f2fd", anchor="w")
pressure_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Sunrise
sunrise_label = tk.Label(details_frame, font=("Arial", 12), bg="#e3f2fd", anchor="w")
sunrise_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Sunset
sunset_label = tk.Label(details_frame, font=("Arial", 12), bg="#e3f2fd", anchor="w")
sunset_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Footer
footer_label = tk.Label(win, text="Powered by OpenWeatherMap API", font=("Arial", 10), 
                       bg="#f0f8ff", fg="#7f8c8d")
footer_label.pack(side="bottom", pady=10)

# Start the application
win.mainloop()
