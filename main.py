import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from geopy.geocoders import Nominatim
import requests
import os


# Need to add timezone for a city and some new stuffs


class Window(tk.Tk):
    def __init__(self, geometry="700x700", title="Weather App"):
        super().__init__()
        self.geometry(geometry)
        self.resizable(False, False)
        self.title(title)

        # Instanciate the footer and header
        self.header = HeaderWidget(self)
        self.footer = FooterWidget(self)

        self.mainloop()

    def showData(self):
        city = self.header.input.get()
        geolocator = Nominatim(user_agent="myGeolocator")
        location = geolocator.geocode(city, timeout=10)

        # Check for wrong input and get API
        if location is not None:
            api = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid=f1271f4cf814f56bf623ac74048d6c0f"
            data = requests.get(api).json()

            # Change main picture
            weatherPic = data["weather"][0]["main"]

            # Check if picture exists
            if f"{weatherPic}.png" in os.listdir(os.getcwd()+"/weatherimages"):
                self.changeContent(weatherPic, data)
            else:
                currentPath = "weatherimages/main.png"
                self.currentPic = ImageTk.PhotoImage(
                    file=currentPath)
                self.header.mainPic.config(image=self.currentPic)

        # If picture doesn't exist reset all information in the screen and
        # set main photo as default picture
        else:
            self.footer.resetInput()
            currentPath = "weatherimages/main.png"
            self.currentPic = ImageTk.PhotoImage(
                file=currentPath)
            self.header.mainPic.config(image=self.currentPic)
            self.header.removeText()
            messagebox.showerror("Error", "Invalid input")

    # Change weather information such as temperature,humidity,wind
    def changeContent(self, weatherPic, data):
        currentPath = f"weatherimages/{weatherPic}.png"
        self.currentPic = ImageTk.PhotoImage(
            file=currentPath)
        self.header.mainPic.config(image=self.currentPic)

        self.footer.descriptionAnswer.config(
            text=data["weather"][0]["description"])
        self.footer.temperatureAnswer.config(
            text=str(int(data["main"]["temp"]-273.15))+"°C")
        self.footer.humidityAnswer.config(
            text=str(data["main"]["humidity"])+"%")
        self.footer.windAnswer.config(text=str(data["wind"]["speed"])+" km/h")


class HeaderWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=600, height=400)
        # Get reference to main window
        self.parent = parent

        self.pack()
        self.createHeader()

    def createHeader(self):
        searchImgPath = "weatherimages/search.png"
        mainPicturePath = "weatherimages/main.png"
        self.imgPhoto = ImageTk.PhotoImage(file=searchImgPath)
        self.mainPhoto = ImageTk.PhotoImage(file=mainPicturePath)

        searchBtn = tk.Button(self, image=self.imgPhoto,
                              command=self.parent.showData, cursor="hand2")
        searchBtn.place(x=460, y=47)

        self.input = tk.Entry(self, width=20, font=(
            "Times New Roman", 30))
        self.input.place(x=50, y=50)
        self.input.focus_set()

        self.mainPic = tk.Label(self, image=self.mainPhoto)
        self.mainPic.place(x=150, y=150)

    def removeText(self):
        self.input.delete(0, tk.END)


class FooterWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=600, height=300)
        self.pack()
        self.createFooter()

    def createFooter(self):

        footerBoxPath = "weatherImages/box.png"
        self.footerBox = ImageTk.PhotoImage(file=footerBoxPath)

        # Create and display footer image box
        footerImg = tk.Label(self, image=self.footerBox)
        footerImg.place(x=0, y=100)

        # Humidity
        humidity = tk.Label(self, text="Humidity:",
                            font=("Times New Roman", 15))
        humidity.place(x=10, y=105)

        self.humidityAnswer = tk.Label(
            self, text="....", font=("Times New Roman", 15))
        self.humidityAnswer.place(x=10, y=150)

        # Wind
        wind = tk.Label(self, text="Wind:", font=("Times New Roman", 15))
        wind.place(x=150, y=105)
        self.windAnswer = tk.Label(
            self, text="....", font=("Times New Roman", 15))
        self.windAnswer.place(x=150, y=150)

        # Temperature
        temperature = tk.Label(self, text="Temperature:",
                               font=("Times New Roman", 15))
        temperature.place(x=270, y=105)
        self.temperatureAnswer = tk.Label(
            self, text="....", font=("Times New Roman", 15))
        self.temperatureAnswer.place(x=270, y=150)

        # Description
        description = tk.Label(self, text="Description:",
                               font=("Times New Roman", 15))

        description.place(x=460, y=105)
        self.descriptionAnswer = tk.Label(
            self, text="....", font=("Times New Roman", 15))
        self.descriptionAnswer.place(x=460, y=150)

    def resetInput(self):
        self.windAnswer.config(text="....")
        self.temperatureAnswer.config(text="....")
        self.humidityAnswer.config(text="....")
        self.descriptionAnswer.config(text="....")


window = Window()
