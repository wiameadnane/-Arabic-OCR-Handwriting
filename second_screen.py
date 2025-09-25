from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt

# Import OCR functions
from inference import infer_image
from inference_bm import infer_image2

class SecondScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        # === Background Image (like FirstScreen) ===
        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap("black.png")  # same as FirstScreen background
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)

        # === Main layout ===
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(80, 60, 80, 60)
        self.main_layout.setSpacing(40)

        # === Image display ===
        self.image_label = QLabel()
        self.image_label.setFixedSize(450, 280)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 3px solid #44a2e2;  /* teal border */
                border-radius: 15px;
                background-color: #1c1c1c;
                padding: 10px;
                color: white;
            }
        """)

        # === Greedy Prediction Label ===
        self.greedy_label = QLabel("🔠 <b>التوقع بطريقة Greedy :</b>")
        self.greedy_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.greedy_label.setWordWrap(True)
        self.greedy_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.greedy_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-family: 'Arial';
                color: #ffffff;
                padding: 20px;
                border-radius: 12px;
                background-color: #1e1e1e;
                border: 2px solid #44a2e2;  /* teal border */
            }
        """)

        # === Beam Search Prediction Label ===
        self.beam_label = QLabel("🔠 <b>التوقع بطريقة Beam Search :</b>")
        self.beam_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.beam_label.setWordWrap(True)
        self.beam_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.beam_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-family: 'Arial';
                color: #ffffff;
                padding: 20px;
                border-radius: 12px;
                background-color: #1e1e1e;
                border: 2px solid #44a2e2;  /* teal border */
            }
        """)

        # === Back Button styled like FirstScreen's button ===
        self.main_button = QPushButton("الرجوع إلى الشاشة الرئيسية")
        self.main_button.clicked.connect(self.go_to_main_screen)
        self.main_button.setFixedSize(300, 75)
        self.main_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #44a2e2;  /* teal text */
                font-size: 24px;
                font-family: 'Arial';
                padding: 18px 40px;
                border-radius: 35px;
                border: 3px solid #44a2e2;  /* teal border */
                box-shadow: 0px 6px 16px rgba(22, 160, 133, 0.3);
                transition: all 0.3s ease-in-out;
            }
            QPushButton:hover {
                background-color: #44a2e2;  /* teal background */
                color: #fff;
                border-color: #117a65;
                box-shadow: 0px 10px 25px rgba(17, 122, 101, 0.6);
                transform: scale(1.05);
            }
        """)

        # === Add widgets to layout ===
        self.main_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.greedy_label)
        self.main_layout.addWidget(self.beam_label)
        self.main_layout.addWidget(self.main_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.main_layout)

    def go_to_main_screen(self):
        self.stacked_widget.setCurrentIndex(0)

    def start_prediction(self, image_path):
        # Show the image
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
        else:
            self.image_label.setText("📷 الصورة غير صالحة")

        # Run inference
        prediction_greedy = infer_image(image_path)
        prediction_beam = infer_image2(image_path, method='beam', beam_width=30)

        # Display results with labels styled as above
        self.greedy_label.setText(f"<b>Greedy :</b><br><br>{prediction_greedy}")
        self.beam_label.setText(f"<b>Beam Search :</b><br><br>{prediction_beam}")
