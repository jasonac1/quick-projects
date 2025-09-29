import sys
import PyQt6
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import * 
import qrcode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWindowGeometry()
        self.initWindowUI()
        self.initUI()
        self.initResources()

    def initWindowGeometry(self):
        width = 1000
        height = 800
        self.setGeometry(0, 0, width, height)

    def initWindowUI(self):
        self.setWindowTitle("QR Code Generator")
        self.setWindowIcon(QIcon("qr.png"))

    def initUI(self):
        # main layout manager
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # buttons layout
        buttons_layout = QHBoxLayout()

        # stylesheet
        styles = """
                QMainWindow {
                    /* gradient coords (0,0) === top left. +x = right, +y = down */
                    color: black;
                    background-color: QLinearGradient(x0: 0, y0: 0, x1: 0, y1: 1, stop: 0 #4CB8C4, stop: 1 #3CD3AD);
                }

                QLabel {
                    color: black;
                    font-family: Inter;
                }

                QLineEdit {
                    color: black;
                    background-color: white;
                    font-family: Inter;
                    font-size: 14px;
                    width: 200px;
                }

                QPushButton {
                    color: white;
                    background-color: black;
                    font-family: Inter;
                    font-size: 18px;
                    padding: 5px;
                    margin-top: 10px;
                    border: 2px solid white;
                    border-radius: 3px;
                }

                QPushButton:hover{
                    background-color: #3a3a3a;
                }
                """
        self.setStyleSheet(styles)
        
        # widgets
        self.label_title = QLabel("QR Code Generator")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(100)
        self.label_title.setGraphicsEffect(shadow)
        self.label_title.setStyleSheet("font-size: 32px;" 
                                    "font-weight: bold;")
        
        self.label_text = QLabel("Input text:")
        self.label_text.setStyleSheet("font-size: 18px;")
        
        self.le_input = QLineEdit()
        
        self.button_generate = QPushButton(text="Generate")
        self.button_generate.clicked.connect(self.generateQR)

        self.button_save = QPushButton(text="Save")
        self.button_save.clicked.connect(self.saveQR)

        self.label_qrpixmap = QLabel()
        self.label_qrpixmap.setStyleSheet(
                                        "font-size: 18px;"
                                        "padding: 3px;"
                                        "margin: 10px;")

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.button_generate)
        buttons_layout.addWidget(self.button_save)
        buttons_layout.addStretch()

        # add widgets
        self.layout.addStretch()

        self.layout.addWidget(self.label_title, alignment=Qt.AlignmentFlag.AlignCenter) # alignment flags align content (such as text) not the widget itself. That is done w/ addStretch()
        self.layout.addWidget(self.label_text, alignment=Qt.AlignmentFlag.AlignCenter) # buttons dont need alignment flags because their content (text) is already centered
        self.layout.addWidget(self.le_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_qrpixmap, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(buttons_layout) # add horizontally centered buttons

        self.layout.addStretch()

    def initResources(self):
        self.current_qr_image = None

    def generateQR(self):
        # check if empty 
        text = self.le_input.text()
        if not text:
            self.label_qrpixmap.setText("Please type some text.")
            return

        # generate qr
        qr_img = qrcode.make(text)

        # open and write image to buffer
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        qr_img.save(buffer)

        # store as current (will be used for saving)
        self.current_qr_image = qr_img

        # display with pixmap
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.data())
        self.label_qrpixmap.setPixmap(pixmap)

        # close buffer
        buffer.close()

    def saveQR(self):
        if not self.current_qr_image:
            self.label_qrpixmap.setText("Please generate a QR code first.")
            return
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Save")
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

        # get file path with getSaveFileName which returns a 2-tuple (path, filter); we want just the first item
        filepath, _ = dialog.getSaveFileName(self, "Save", "qrcode.png", "PNG Image (*.png);; JPEG Image (*.jpg *.jpeg)") # qrcode.png is the default file path

        # then save; if file path empty -> user canceled
        if filepath:
            self.current_qr_image.save(filepath)

def main():
    app = QApplication(sys.argv) # sys.argv to accept terminal args
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
