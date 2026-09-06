from datetime import datetime
import os
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
import pytz
import requests
from timezonefinder import TimezoneFinder



root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_path(filename):
  return os.path.join(BASE_DIR, filename)


def getWeather():
  city = textfield.get().strip()

  if not city:
    messagebox.showwarning("Input Error", "Please enter a city name.")
    return

  try:
   
    geolocator = Nominatim(user_agent="my_weather_app_v1", timeout=10)
    location = geolocator.geocode(city)

   
    if location is None:
      clock.config(text="")
      name.config(text="")
      t.config(text="")
      c.config(text="")
      w.config(text="...")
      h.config(text="...")
      d.config(text="...")
      p.config(text="...")

      messagebox.showerror(
          "Invalid Location",
          f"Could not find '{city}'. Please check the spelling and try again.",
      )
      return


    tf = TimezoneFinder()

    tz_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)


    local_tz = pytz.timezone(tz_str)
    local_time = datetime.now(local_tz)
    clock.config(text=local_time.strftime("%I:%M %p"))
    name.config(text="CURRENT WEATHER")


    api_key = "b214e0beb94f9638b3f2c7d269f7b79c"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={api_key}&units=metric"

    response = requests.get(url).json()

    if response.get("cod") != 200:
      messagebox.showerror(
          "API Error", response.get("message", "Unable to retrieve weather data.")
      )
      return

  
    condition = response["weather"][0]["main"]
    description = response["weather"][0]["description"]
    temp = int(response["main"]["temp"])
    feels_like = int(response["main"]["feels_like"])
    pressure = response["main"]["pressure"]
    humidity = response["main"]["humidity"]
    wind_speed = response["wind"]["speed"]

 
    t.config(text=f"{temp}°")
    c.config(text=f"{condition} | FEELS LIKE {feels_like}°")
    w.config(text=f"{wind_speed} m/s")
    h.config(text=f"{humidity}%")
    d.config(text=description.capitalize())
    p.config(text=f"{pressure} hPa")

  except Exception as err:
    messagebox.showerror(
        "Connection Error", f"Request timed out or failed:\n{err}"
    )



def on_enter_key(event):
  getWeather()



search_image = PhotoImage(file=get_path("search.png"))
Label(root, image=search_image).place(x=20, y=20)

textfield = tk.Entry(
    root,
    justify="center",
    width=17,
    font=("poppins", 25, "bold"),
    bg="#404040",
    border=0,
    fg="white",
)


textfield.place(x=50, y=40)
textfield.focus()
textfield.bind("<Return>", on_enter_key)



search_icon = PhotoImage(file=get_path("search icon.png"))
search_btn = Button(
    root,
    image=search_icon,
    borderwidth=0,
    cursor="hand2",
    bg="#404040",
    command=getWeather,
)
search_btn.place(x=400, y=34)



logo_image = PhotoImage(file=get_path("weather-app.png")).subsample(3, 3)
Label(root, image=logo_image).place(x=150, y=140)

Frame_image = PhotoImage(file=get_path("box images.png"))
Label(root, image=Frame_image).pack(padx=5, pady=5, side=BOTTOM)



name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)


clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

Label(
    root, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef"
).place(x=120, y=400)
Label(
    root,
    text="HUMIDITY",
    font=("Helvetica", 15, "bold"),
    fg="white",
    bg="#1ab5ef",
).place(x=250, y=400)
Label(
    root,
    text="DESCRIPTION",
    font=("Helvetica", 15, "bold"),
    fg="white",
    bg="#1ab5ef",
).place(x=430, y=400)
Label(
    root,
    text="PRESSURE",
    font=("Helvetica", 15, "bold"),
    fg="white",
    bg="#1ab5ef",
).place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=380, y=150)

c = Label(font=("arial", 15, "bold"))
c.place(x=380, y=250)


w = Label(text="...", font=("arial", 18, "bold"), bg="#1ab5ef", fg="white")
w.place(x=120, y=430)

h = Label(text="...", font=("arial", 18, "bold"), bg="#1ab5ef", fg="white")
h.place(x=250, y=430)

d = Label(text="...", font=("arial", 18, "bold"), bg="#1ab5ef", fg="white")
d.place(x=430, y=430)


p = Label(text="...", font=("arial", 18, "bold"), bg="#1ab5ef", fg="white")
p.place(x=650, y=430)

root.mainloop()