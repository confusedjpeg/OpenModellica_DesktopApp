import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
)

class OpenModelicaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main window properties
        self.setWindowTitle("OpenModelica Desktop App")
        self.setGeometry(300, 300, 500, 200)

        # Layout
        layout = QVBoxLayout()

        # Application Selector
        app_layout = QHBoxLayout()
        self.app_label = QLabel("Application:")
        self.app_input = QLineEdit()
        self.app_input.setPlaceholderText("Select executable")
        self.app_button = QPushButton("Browse")
        self.app_button.clicked.connect(self.select_executable)
        app_layout.addWidget(self.app_label)
        app_layout.addWidget(self.app_input)
        app_layout.addWidget(self.app_button)

        # Start Time
        start_time_layout = QHBoxLayout()
        self.start_time_label = QLabel("Start Time:")
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("Enter start time (integer)")
        start_time_layout.addWidget(self.start_time_label)
        start_time_layout.addWidget(self.start_time_input)

        # Stop Time
        stop_time_layout = QHBoxLayout()
        self.stop_time_label = QLabel("Stop Time:")
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setPlaceholderText("Enter stop time (integer)")
        stop_time_layout.addWidget(self.stop_time_label)
        stop_time_layout.addWidget(self.stop_time_input)

        # Execute Button
        self.execute_button = QPushButton("Run Simulation")
        self.execute_button.clicked.connect(self.run_simulation)

        # Adding all widgets to the main layout
        layout.addLayout(app_layout)
        layout.addLayout(start_time_layout)
        layout.addLayout(stop_time_layout)
        layout.addWidget(self.execute_button)
        self.setLayout(layout)

    def select_executable(self):
        # File dialog to select executable
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Executable", "", "Executable Files (*.exe)")
        if file_path:
            self.app_input.setText(file_path)

    def run_simulation(self):
        app_path = self.app_input.text()
        try:
            start_time = int(self.start_time_input.text())
            stop_time = int(self.stop_time_input.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Start time and Stop time must be integers.")
            return

        if not os.path.exists(app_path):
            QMessageBox.critical(self, "Error", "Invalid application path.")
            return
        if not (0 <= start_time < stop_time < 5):
            QMessageBox.critical(self, "Error", "Ensure 0 <= Start Time < Stop Time < 5.")
            return

        # Get the directory of the executable
        executable_dir = os.path.dirname(app_path)

        try:
            process = subprocess.run(
                [app_path, f"-override=startTime={start_time},stopTime={stop_time}"],
                capture_output=True,
                text=True,
                cwd=executable_dir  # Set the working directory
            )
            print("Stdout:", process.stdout)
            print("Stderr:", process.stderr)

            if process.returncode == 0:
                QMessageBox.information(self, "Success", "Simulation ran successfully.")
            else:
                QMessageBox.critical(self, "Error", f"Simulation failed:\n{process.stderr}")
                print(process.stderr)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    # Entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenModelicaApp()
    window.show()
    sys.exit(app.exec())
