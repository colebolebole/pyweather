import sys
import requests
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt

class WeatherMapApp(QWidget):
    def __init__(self):
        super().__init__()

        self.api_key = '0b37e47e67e63246f5d49cd9ee488ad7'

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Weather Map App')

        main_layout = QHBoxLayout()

        weather_layout = QVBoxLayout()

        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter the city name")
        self.city_input.setStyleSheet("QLineEdit { background-color: #eceff1; border: 1px solid #90a4ae; }")

        self.get_weather_button = QPushButton("Get Weather", self)
        self.get_weather_button.clicked.connect(self.get_weather_and_map)
        self.get_weather_button.setStyleSheet("QPushButton { height: 40px; }")

        self.weather_label = QLabel(self)
        self.weather_label.setAlignment(Qt.AlignTop)

        weather_layout.addWidget(self.city_input)
        weather_layout.addWidget(self.get_weather_button)
        weather_layout.addWidget(self.weather_label)

        map_layout = QVBoxLayout()

        self.web_view = QWebEngineView(self)
        self.web_view.setFixedSize(800, 600)

        map_layout.addWidget(self.web_view)

        main_layout.addLayout(weather_layout)
        main_layout.addLayout(map_layout)

        self.setLayout(main_layout)

        self.show()

    def get_weather_and_map(self):
        city = self.city_input.text()
        weather_data = self.fetch_weather_data(city)

        if weather_data:
            self.display_weather(weather_data)
            self.display_map(weather_data['coord']['lat'], weather_data['coord']['lon'])
        else:
            self.weather_label.setText("<p>Weather data not available.</p>")
            self.web_view.setHtml("<p>Map not available.</p>")

    def fetch_weather_data(self, city):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                return data
            else:
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def display_weather(self, weather_data):
        location = f"Location: {weather_data['name']}, {weather_data['sys']['country']}"
        temperature = f"Temperature: {weather_data['main']['temp']}°C"
        description = f"Description: {weather_data['weather'][0]['description']}"
        humidity = f"Humidity: {weather_data['main']['humidity']}%"
        wind_speed = f"Wind Speed: {weather_data['wind']['speed']} m/s"

        weather_info = f"{location}\n{temperature}\n{description}\n{humidity}\n{wind_speed}"

        self.weather_label.setText(weather_info)

    def display_map(self, lat, lon):
        map_osm = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], popup='Weather Location').add_to(map_osm)
        map_osm.save("map.html")

        with open("map.html", "r") as f:
            map_html = f.read()

        self.web_view.setHtml(map_html)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_map_app = WeatherMapApp()
    sys.exit(app.exec_())
