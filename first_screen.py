from PyQt6.QtWidgets import (
    QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel,
    QSpacerItem, QSizePolicy, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush


class FirstScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.second_screen = None  # To be set externally

        # === Background Image ===
        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap("black.png")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)

        # === Main Layout ===
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(80, 60, 80, 60)
        main_layout.setSpacing(40)

        # === Spacer Top ===
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # === Title Layout ===
        title_container = QVBoxLayout()
        title_container.setSpacing(10)

        self.title_label = QLabel("كلمتي")  # "My Word"
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 92px;
                font-family: 'Amiri', 'Arial', sans-serif;
                font-weight: 800;
                color: #ffffff;
                letter-spacing: 3px;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.6);
            }
        """)
        title_container.addWidget(self.title_label)

        self.description_label = QLabel("Arabic OCR")  # Arabic OCR description
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setStyleSheet("""
            QLabel {
                font-size: 31px;
                font-family: 'Arial';
                color: #44a2e2;  /* New teal color */
                font-weight: 600;
                letter-spacing: 1px;
            }
        """)
        title_container.addWidget(self.description_label)

        title_frame = QFrame()
        title_frame.setLayout(title_container)
        main_layout.addWidget(title_frame)

        # === Spacer Between Title and Button ===
        main_layout.addSpacerItem(QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # === Upload Button Layout ===
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        upload_button = QPushButton("تحميل صورة")  # Upload Image
        upload_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #44a2e2;  /* teal-ish text */
                font-size: 24px;
                font-family: 'Arial';
                padding: 18px 40px;
                border-radius: 35px;
                border: 3px solid #44a2e2;  /* subtle teal outline */
                box-shadow: 0px 6px 16px rgba(22, 160, 133, 0.3);
                transition: all 0.3s ease-in-out;
            }
            QPushButton:hover {
                background-color: #44a2e2;  /* teal background on hover */
                color: #fff;
                border-color: #44a2e2;  /* darker teal border on hover */
                box-shadow: 0px 10px 25px rgba(17, 122, 101, 0.6);
                transform: scale(1.05);
            }
        """)
        upload_button.setFixedSize(280, 75)
        upload_button.clicked.connect(self.open_file_dialog)
        button_layout.addWidget(upload_button)

        main_layout.addLayout(button_layout)

        # === Spacer Bottom ===
        main_layout.addSpacerItem(QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(main_layout)
        self.setGeometry(100, 100, 900, 1000)

    def open_file_dialog(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "اختر صورة",  # Choose an image
                "",
                "Image Files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;All Files (*)",
            )

            if file_path:
                if self.is_image_file(file_path):
                    print(f"✅ Selected image path: {file_path}")
                    self.go_to_second_screen(file_path)
                else:
                    print("❌ نوع الملف غير صالح. الرجاء اختيار صورة.")
        except Exception as e:
            print(f"⚠ حدث خطأ: {e}")

    @staticmethod
    def is_image_file(file_path):
        image_extensions = [".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"]
        return any(file_path.lower().endswith(ext) for ext in image_extensions)

    def go_to_second_screen(self, file_path):
        if self.second_screen:
            self.second_screen.start_prediction(file_path)
            self.stacked_widget.setCurrentIndex(1)
        else:
            print("⚠ SecondScreen غير متصل.")
