import sys
import PyQt6
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QLabel, QLineEdit,
                             QPushButton, QWidget,
                             QVBoxLayout, QHBoxLayout)
from PyQt6.QtGui import QIcon 
from PyQt6.QtCore import Qt
from weather_api_client import get_weather_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGeometry()
        self.initUI()
        self.initWindowUI()
        
    def initWindowUI(self):
        self.setWindowTitle("Weather")
        self.setWindowIcon(QIcon("weather.jpeg"))

    def initGeometry(self):
        width = 1000
        height = 800
        self.setGeometry(0, 0, width, height)

    def initUI(self):
        # main layout manager
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # BG
        styles = "background-color: white; color black"
        self.setStyleSheet(styles)

        # enter city label
        self.label_enter_city = QLabel(text="Enter city")
        self.label_enter_city.setStyleSheet("color: black;"
                                            "font-family: Inter;"
                                            "font-size: 24px")

        # line edit
        self.lineedit_enter_city = QLineEdit()
        self.lineedit_enter_city.setStyleSheet("color: black;"
                                            "font-family: Inter;"
                                            "font-size: 18px")

        # get weather button
        self.get_weather_button = QPushButton(text="Get Weather")
        self.get_weather_button.setStyleSheet("color: black;"
                                            "font-family: Inter;"
                                            "font-size: 18px")
        self.get_weather_button.clicked.connect(self.getWeather)

        # weather label
        self.label_weather = QLabel(text="")
        self.label_weather.setStyleSheet("color: black;"
                                            "font-family: Inter;"
                                            "font-size: 30px")

        # add to layout
        layout.addStretch() # push widgets down

        layout.addWidget(self.label_enter_city, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lineedit_enter_city, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.get_weather_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_weather, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch() # push widgets up
    
    def getWeather(self):
        city = self.lineedit_enter_city.text()
        if not city: # checks if not None
            self.label_weather.setText("Please enter a city.")
            return

        weather_data = get_weather_data(city=city, units="metric")

        # check for errors (str)
        if not isinstance(weather_data, dict):
            self.label_weather.setText(f"{weather_data}")
            return

        temp = weather_data["main"]["temp"]
        weather = weather_data["weather"][0]["main"]
        weather_data_text = f"{city}\n{temp}°C\n{weather}"
        self.label_weather.setText(f"{weather_data_text}")
        return
    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()