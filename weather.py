from datetime import datetime, timedelta, timezone
import io
import os
from tkinter import Button, Entry, Label, Tk, messagebox
from PIL import Image, ImageTk
import requests

# App Configuration

WINDOW_WIDTH = 1050
WINDOW_HEIGHT = 650
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_KEY = "b214e0beb94f9638b3f2c7d269f7b79c"


def get_asset_path(filename):
  """Constructs absolute path for UI assets."""
  return os.path.join(BASE_DIR, filename)


def load_image_asset(filename):
  """Safely loads Tkinter PhotoImage asset without crashing on missing files."""
  filepath = get_asset_path(filename)
  if os.path.exists(filepath):
    try:
      return ImageTk.PhotoImage(file=filepath)
    except Exception as err:
      print(f"Error loading asset {filename}: {err}")
  return None


def fetch_city_photo(city_name):
  """Retrieves a representative photo for the searched location."""
  try:
    url = f"https://picsum.photos/seed/{city_name}/360/220"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
      img = Image.open(io.BytesIO(response.content))
      return ImageTk.PhotoImage(img)
  except Exception as err:
    print(f"Failed to retrieve city image: {err}")
  return None


def fetch_weather():
  city = search_input.get().strip()

  if not city:
    messagebox.showwarning("Input Error", "Please enter a city name.")
    return

  try:
    endpoint = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(endpoint).json()

    if data.get("cod") != 200:
      messagebox.showerror(
          "City Not Found", f"Could not locate '{city}'. Please check spelling."
      )
      return


    temp = int(data["main"]["temp"])
    feels_like = int(data["main"]["feels_like"])
    condition = data["weather"][0]["main"]
    description = data["weather"][0]["description"].capitalize()
    wind_speed = data["wind"]["speed"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]


    utc_offset = data.get("timezone", 0)
    local_time = datetime.now(timezone.utc) + timedelta(seconds=utc_offset)


    city_label.config(text=city.upper())
    clock_label.config(text=local_time.strftime("%I:%M %p"))
    temp_label.config(text=f"{temp}°")
    condition_label.config(text=f"{condition} | FEELS LIKE {feels_like}°")


    wind_value.config(text=f"{wind_speed} m/s")
    humidity_value.config(text=f"{humidity}%")
    desc_value.config(text=description)
    pressure_value.config(text=f"{pressure} hPa")


    city_photo = fetch_city_photo(city)
    if city_photo:
      photo_display.config(image=city_photo)
      photo_display.image = city_photo

  except Exception as err:
    messagebox.showerror("Error", f"Could not fetch weather data:\n{err}")


# Main Window Setup


app = Tk()
app.title("Weather Dashboard")
app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+200+100")
app.resizable(False, False)


# Search Bar


search_bg = load_image_asset("search.png")
if search_bg:
  Label(app, image=search_bg).place(x=80, y=20)

search_input = Entry(
    app,
    justify="center",
    width=17,
    font=("poppins", 25, "bold"),
    bg="#404040",
    fg="white",
    bd=0,
)
search_input.place(x=110, y=40)
search_input.focus()
search_input.bind("<Return>", lambda e: fetch_weather())

search_icon = load_image_asset("search icon.png")
search_button = Button(
    app,
    image=search_icon if search_icon else None,
    text="Search" if not search_icon else "",
    borderwidth=0,
    cursor="hand2",
    bg="#404040",
    fg="white" if not search_icon else "black",
    command=fetch_weather,
)
search_button.place(x=460, y=34)


# City Information


city_label = Label(app, font=("arial", 18, "bold"))
city_label.place(x=50, y=105)

clock_label = Label(app, font=("Helvetica", 16))
clock_label.place(x=50, y=135)

photo_display = Label(app, bg="#202020")
photo_display.place(x=50, y=170, width=360, height=220)

# Temperature Panel
temp_label = Label(app, font=("arial", 70, "bold"), fg="#ee666d")
temp_label.place(x=470, y=180)

condition_label = Label(app, font=("arial", 15, "bold"))
condition_label.place(x=470, y=290)


# Metric Bottom Bar Overlay


frame_bg = load_image_asset("box images.png")
if frame_bg:
  Label(app, image=frame_bg).pack(padx=5, pady=10, side="bottom")


# Metric Headers


header_font = ("Helvetica", 15, "bold")
Label(app, text="WIND", font=header_font, fg="white", bg="#1ab5ef").place(
    x=160, y=520
)
Label(app, text="HUMIDITY", font=header_font, fg="white", bg="#1ab5ef").place(
    x=320, y=520
)
Label(
    app, text="DESCRIPTION", font=header_font, fg="white", bg="#1ab5ef"
).place(x=520, y=520)
Label(app, text="PRESSURE", font=header_font, fg="white", bg="#1ab5ef").place(
    x=760, y=520
)

# Metric Values


val_font = ("arial", 18, "bold")
wind_value = Label(
    app, text="...", font=val_font, bg="#1ab5ef", fg="white"
)
wind_value.place(x=160, y=555)

humidity_value = Label(
    app, text="...", font=val_font, bg="#1ab5ef", fg="white"
)
humidity_value.place(x=320, y=555)

desc_value = Label(
    app, text="...", font=val_font, bg="#1ab5ef", fg="white"
)
desc_value.place(x=520, y=555)

pressure_value = Label(
    app, text="...", font=val_font, bg="#1ab5ef", fg="white"
)
pressure_value.place(x=760, y=555)

app.mainloop()









