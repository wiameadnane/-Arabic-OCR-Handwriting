import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from first_screen import FirstScreen
from second_screen import SecondScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arabic OCR")
        self.setGeometry(500, 100, 550, 540)

        # Create the QStackedWidget
        self.stacked_widget = QStackedWidget()

        # Create the screens
        self.main_screen = FirstScreen(self.stacked_widget)
        self.second_screen = SecondScreen(self.stacked_widget)

        self.main_screen.second_screen = self.second_screen

        # Add screens to the QStackedWidget
        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.second_screen)

        # Set the QStackedWidget as the central widget
        self.setCentralWidget(self.stacked_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())

