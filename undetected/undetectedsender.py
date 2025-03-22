### undetected script uses mouse macro to auto send snaps quickly 
### if u get banned its not my fault

### !SET UR PASSWORD AND USER ON LINE 196!


import sys
import ctypes
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QCursor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class ScreenCropper(QDialog):
    def __init__(self):
        super().__init__()
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.5)
        self.setWindowTitle("Screen Cropper Tool")

        self.setGeometry(0, 0, QApplication.primaryScreen().size().width(), QApplication.primaryScreen().size().height())

        self.setStyleSheet("background-color: transparent;")

        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)

        self.is_dragging = False
        self.selected = False
        self.ui_initialized = False
        self.show_instructions()

    def show_instructions(self):
        self.instructions_window = QDialog(self)
        self.instructions_window.setWindowTitle("Instructions")
        layout = QVBoxLayout()

        instructions = QLabel("Instructions:\n"
                              "1. Select the camera UI area in the Snapchat Web\n"
                              "2. Drag your mouse to select the desired area.\n"
                              "3. Confirm the selection to save the coordinates.\n"
                              "4. The coordinates will be saved in a JSON file.")
        layout.addWidget(instructions)

        confirm_button = QPushButton("Got it! Start Selection")
        confirm_button.clicked.connect(self.instructions_window.close)
        layout.addWidget(confirm_button)

        self.instructions_window.setLayout(layout)
        self.instructions_window.exec_()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.selected:
            self.start_x = event.pos().x()
            self.start_y = event.pos().y()
            self.is_dragging = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_dragging and not self.selected:
            self.end_x = event.pos().x()
            self.end_y = event.pos().y()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and not self.selected:
            self.end_x = event.pos().x()
            self.end_y = event.pos().y()
            self.is_dragging = False
            self.selected = True
            self.update()
            self.confirm_selection()

    def paintEvent(self, event):
        if self.start_x and self.start_y and self.end_x and self.end_y:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(255, 0, 0), 5))
            painter.setBrush(QColor(255, 0, 0, 50))
            rect = QRect(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y)
            painter.drawRect(rect)

    def confirm_selection(self):
        self.confirmation_window = QDialog(self)
        self.confirmation_window.setWindowTitle("Confirm Selection")
        layout = QVBoxLayout()

        confirmation_message = QLabel(f"Selected coordinates:\n"
                                      f"Top-left: ({self.start_x}, {self.start_y})\n"
                                      f"Bottom-right: ({self.end_x}, {self.end_y})")
        layout.addWidget(confirmation_message)

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.save_positions)
        layout.addWidget(confirm_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reset_selection)
        layout.addWidget(cancel_button)

        self.confirmation_window.setLayout(layout)
        self.confirmation_window.exec_()

    def reset_selection(self):
        self.start_x = self.end_x = self.start_y = self.end_y = None
        self.selected = False
        self.update()
        self.confirmation_window.close()

    def save_positions(self):
        width = self.end_x - self.start_x
        height = self.end_y - self.start_y

        positions = {
            "Take the photo": (self.start_x + int(width * 0.5), self.start_y + int(height * 0.3)),
            "'Send To' button": (self.start_x + int(width * 0.6), self.start_y + int(height * 0.7)),
            "'Send To' input field": (self.start_x + int(width * 0.4), self.start_y + int(height * 0.1)),
            "First result": (self.start_x + int(width * 0.8), self.start_y + int(height * 0.2)),
            "Send": (self.start_x + int(width * 0.55), self.start_y + int(height * 0.75)),
        }

        file_name = "ButtonPosition.json"
        with open(file_name, "w") as pos_file:
            json.dump(positions, pos_file)

        print(f"Positions saved as {file_name}")
        self.confirmation_window.close()
        self.close()

    def closeEvent(self, event):
        if self.selected:
            event.accept()
        else:
            event.ignore()

class SnapchatAutomation:
    def __init__(self, driver_path, positions_file="ButtonPosition.json"):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.driver.get("https://web.snapchat.com/")
        time.sleep(5)

        self.load_positions(positions_file)

    def load_positions(self, file_name):
        with open(file_name, "r") as f:
            self.positions = json.load(f)

    def login(self, username, password):
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Log in')]").click()

    def take_photo_and_send(self):
        take_photo_button = self.positions["Take the photo"]
        self.click_on_element(take_photo_button)
        time.sleep(1)

        send_to_button = self.positions["'Send To' button"]
        self.click_on_element(send_to_button)
        time.sleep(1)

        first_result = self.positions["First result"]
        self.click_on_element(first_result)
        time.sleep(1)

        send_button = self.positions["Send"]
        self.click_on_element(send_button)

    def click_on_element(self, position):
        x, y = position
        script = f"window.scrollTo({x - 500}, {y - 500});"
        self.driver.execute_script(script)
        time.sleep(0.5)
        self.driver.execute_script(f"document.elementFromPoint({x}, {y}).click();")

    def send_multiple_snaps(self, num_snaps):
        for _ in range(num_snaps):
            self.take_photo_and_send()
            print(f"Snap {_:02d} sent!")
            time.sleep(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cropper = ScreenCropper()
    cropper.show()
    app.exec_()

    automation = SnapchatAutomation(driver_path="path_to_your_chromedriver")
    automation.login(username="your_snapchat_username", password="your_snapchat_password")
    automation.send_multiple_snaps(10)