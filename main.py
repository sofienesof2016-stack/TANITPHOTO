import sys
from PIL import Image, ImageEnhance, ImageFilter
from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


class TanitPhoto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TANITPHOTO - Éditeur photo")
        self.resize(1100, 750)
        self.original = None
        self.image = None

        self.preview = QLabel("Bienvenue dans TANITPHOTO\nOuvrez une image pour commencer")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setStyleSheet("background:#20242b;color:white;font-size:22px;")

        open_btn = QPushButton("Ouvrir une image")
        save_btn = QPushButton("Enregistrer")
        rotate_btn = QPushButton("Rotation 90°")
        gray_btn = QPushButton("Noir et blanc")
        sharp_btn = QPushButton("Améliorer la netteté")
        reset_btn = QPushButton("Réinitialiser")

        open_btn.clicked.connect(self.open_image)
        save_btn.clicked.connect(self.save_image)
        rotate_btn.clicked.connect(self.rotate)
        gray_btn.clicked.connect(self.grayscale)
        sharp_btn.clicked.connect(self.sharpen)
        reset_btn.clicked.connect(self.reset)

        self.brightness = QSlider(Qt.Orientation.Horizontal)
        self.brightness.setRange(50, 150)
        self.brightness.setValue(100)
        self.brightness.valueChanged.connect(self.change_brightness)

        toolbar = QHBoxLayout()
        for btn in (open_btn, save_btn, rotate_btn, gray_btn, sharp_btn, reset_btn):
            toolbar.addWidget(btn)

        layout = QVBoxLayout()
        layout.addLayout(toolbar)
        layout.addWidget(QLabel("Luminosité"))
        layout.addWidget(self.brightness)
        layout.addWidget(self.preview)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStyleSheet("""
            QMainWindow {background:#30343b;}
            QPushButton {
                background:#087e9b;color:white;padding:12px;
                border:0;border-radius:5px;
            }
            QPushButton:hover {background:#0aa5c8;}
            QLabel {color:white;}
        """)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir une image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if path:
            self.original = Image.open(path).convert("RGB")
            self.image = self.original.copy()
            self.brightness.setValue(100)
            self.show_image()

    def show_image(self):
        if self.image is None:
            return
        img = self.image.copy()
        img.thumbnail((1000, 550))
        data = img.tobytes("raw", "RGB")
        qimg = QImage(data, img.width, img.height, img.width * 3,
                      QImage.Format.Format_RGB888)
        self.preview.setPixmap(QPixmap.fromImage(qimg.copy()))

    def save_image(self):
        if self.image is None:
            QMessageBox.information(self, "TANITPHOTO", "Ouvrez une image d'abord.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer", "image.png",
            "PNG (*.png);;JPEG (*.jpg)"
        )
        if path:
            self.image.save(path)
            QMessageBox.information(self, "TANITPHOTO", "Image enregistrée.")

    def rotate(self):
        if self.image:
            self.image = self.image.rotate(-90, expand=True)
            self.show_image()

    def grayscale(self):
        if self.image:
            self.image = self.image.convert("L").convert("RGB")
            self.show_image()

    def sharpen(self):
        if self.image:
            self.image = self.image.filter(
                ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)
            )
            self.show_image()

    def change_brightness(self, value):
        if self.original:
            self.image = ImageEnhance.Brightness(self.original).enhance(value / 100)
            self.show_image()

    def reset(self):
        if self.original:
            self.image = self.original.copy()
            self.brightness.setValue(100)
            self.show_image()


app = QApplication(sys.argv)
window = TanitPhoto()
window.show()
sys.exit(app.exec())
