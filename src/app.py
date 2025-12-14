import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

try:
    from inference import BubbleCropper
except ImportError as e:
    raise RuntimeError(
        f"FATAL: Could not import BubbleCropper from inference module: {e}"
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Bubble Crop")
        self.setMinimumSize(QSize(400, 300))
        
        self.uploaded_file_path = None
        
        try:
            self.cropper = BubbleCropper(
                model_path="models/best.pt",
                config_path="config.json",
                classes_path="classes.json"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize BubbleCropper:\n{e}")
            self.cropper = None
        
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_label = QLabel("Bubble Crop")
        header_font = QFont("Arial", 24, QFont.Weight.Bold)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)
        
        main_layout.addSpacing(20)
        
        self.status_label = QLabel("No file uploaded yet.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        self.upload_button = QPushButton("Upload File (Image/Zip)")
        self.upload_button.clicked.connect(self.upload_file)
        self.upload_button.setFixedSize(200, 40)
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addSpacing(15)

        self.crop_button = QPushButton("Crop")
        self.crop_button.clicked.connect(self.start_crop_process)
        self.crop_button.setFixedSize(200, 40)
        self.crop_button.setEnabled(False) 
        main_layout.addWidget(self.crop_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("""
            color: #2e7d32;
        """)
        self.result_label.setWordWrap(True)
        main_layout.addWidget(self.result_label)


        self.setCentralWidget(central_widget)

    def upload_file(self):
        file_filter = "Zip Files (*.zip);;Image Files (*.png *.jpg *.jpeg);;All Files (*)"
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select a File (Image or ZIP)", 
            "", 
            file_filter
        )
        
        if file_path:
            self.uploaded_file_path = file_path
            self.status_label.setText(f"File Selected: {os.path.basename(file_path)}")
            self.result_label.setText("")
            self.crop_button.setEnabled(True)
        else:
            self.uploaded_file_path = None
            self.status_label.setText("No file uploaded yet.")
            self.crop_button.setEnabled(False)

    def start_crop_process(self):
        if not self.uploaded_file_path:
            QMessageBox.warning(self, "Warning", "Please upload a file first.")
            return

        if not self.cropper:
            QMessageBox.critical(self, "Error", "Application failed to initialize. Check model configuration.")
            return

        try:
            result = self.cropper.process(
                input_path=self.uploaded_file_path
            )
            output_dir = self.cropper.get_default_output_dir()
            self.result_label.setText(
                f"Successfully saved at:\n{output_dir}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error Execution", f"An error occurred while executing the crop process: {e}")

        self.uploaded_file_path = None
        self.status_label.setText("Process complete. Upload a new file.")
        self.crop_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())