import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
    QTextEdit, QFormLayout, QStatusBar
)
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtCore import QSettings

class OpenModelicaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("FOSSEE", "OpenModelicaDesktopApp")
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        # Main window properties
        self.setWindowTitle("OpenModelica Desktop App")
        self.setGeometry(300, 300, 600, 400)

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
        time_layout = QFormLayout()
        self.start_time_label = QLabel("Start Time:")
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("Enter start time (integer)")
        self.start_time_input.setValidator(QIntValidator()) 
        time_layout.addRow(self.start_time_label, self.start_time_input)

        # Stop Time
        stop_time_layout = QHBoxLayout()
        self.stop_time_label = QLabel("Stop Time:")
        self.stop_time_input = QLineEdit()
        self.stop_time_input.setPlaceholderText("Enter stop time (integer)")
        self.start_time_input.setValidator(QIntValidator()) 
        time_layout.addRow(self.stop_time_label, self.stop_time_input)

        # Execute Button
        self.execute_button = QPushButton("Run Simulation")
        self.execute_button.clicked.connect(self.run_simulation)
        self.execute_button.setIcon(QIcon("assets\play_icon.png"))

        # Output Area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)  # Make it read-only

        # Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")

        # Adding all widgets to the main layout
        layout.addLayout(app_layout)
        layout.addLayout(time_layout)
        layout.addWidget(self.execute_button)
        layout.addWidget(self.output_text)
        layout.addWidget(self.status_bar)
        self.setLayout(layout)

        # Apply a basic stylesheet
        self.setStyleSheet("""
QWidget {
    background-color: #1e1e1e; /* Very dark gray, almost black */
    color: #f8f8f2; /* Off-white for text */
    font-family: "Consolas", "Menlo", monospace;
    font-size: 10pt;
}

QLabel {
    color: #E2A0FF; /* Cool purple for labels */
    font-weight: bold;
}

QLineEdit {
    background-color: #333333; /* Dark gray for input fields */
    color: #f8f8f2;
    border: 1px solid #666666;
    padding: 5px;
    selection-background-color: #aa7ecf; /* Purple selection */
}

QPushButton {
    background-color: #E2A0FF; /* Purple-ish for buttons */
    color: #1E1E1E;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 10pt;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #9a67ea; /* Lighter purple on hover */
}

QPushButton:pressed {
    background-color: #5a4469; /* Darker purple when pressed */
}

QTextEdit {
    background-color: #333333;
    color: #f8f8f2;
    border: 1px solid #666666;
    selection-background-color: #aa7ecf;
}

QStatusBar {
    background-color: #282a36; /* Slightly lighter dark for status bar */
    color: #b0bec5;
}

QMenuBar {
    background-color: #282a36;
    color: #f8f8f2;
}

QMenuBar::item {
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #6c567b;
}

QMenu {
    background-color: #282a36;
    color: #f8f8f2;
    border: 1px solid #44475a;
}

QMenu::item:selected {
    background-color: #6c567b;
}
""")

    def load_settings(self):
        self.app_input.setText(self.settings.value("app_path", ""))
        self.start_time_input.setText(self.settings.value("start_time", ""))
        self.stop_time_input.setText(self.settings.value("stop_time", ""))

    def save_settings(self):
        self.settings.setValue("app_path", self.app_input.text())
        self.settings.setValue("start_time", self.start_time_input.text())
        self.settings.setValue("stop_time", self.stop_time_input.text())

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

    def select_executable(self):
        # File dialog to select executable
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Executable", "", "Executable Files (*.exe)")
        if file_path:
            self.app_input.setText(file_path)

    def run_simulation(self):
        app_path = self.app_input.text()
        start_time_text = int(self.start_time_input.text())
        stop_time_text = int(self.stop_time_input.text())
        try:
            start_time = int(start_time_text)
            stop_time = int(stop_time_text)
        except ValueError:
            QMessageBox.critical(self, "Error", "Start time and Stop time must be integers.")
            return

        if not os.path.exists(app_path):
            QMessageBox.critical(self, "Error", "Invalid application path: '{app_path}' not found.")
            return
        if not (0 <= start_time < stop_time < 5):
            QMessageBox.critical(self, "Error", "Ensure 0 <= Start Time < Stop Time < 5.")
            return

        # Get the directory of the executable
        executable_dir = os.path.dirname(app_path)

        self.output_text.clear()
        self.status_bar.showMessage("Running simulation...", 0)
        self.execute_button.setText("Running...")
        self.execute_button.setEnabled(False)

        try:
            process = subprocess.run(
                [app_path, f"-override=startTime={start_time},stopTime={stop_time}"],
                capture_output=True,
                text=True,
                cwd=executable_dir  # Set the working directory
            )

            self.output_text.append(f"Stdout:\n{process.stdout}")
            self.output_text.append(f"Stderr:\n{process.stderr}")

            if process.returncode == 0:
                self.status_bar.showMessage("Simulation completed successfully.", 5000)
                QMessageBox.information(self, "Success", "Simulation ran successfully.")
            else:
                error_message = f"Simulation failed with return code {process.returncode}:\n{process.stderr}"
                self.status_bar.showMessage("Simulation failed.", 5000)
                QMessageBox.critical(self, "Error", error_message)
        except FileNotFoundError:
            self.status_bar.showMessage(f"An error occurred: {str(e)}", 5000)
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")
            self.output_text.append(f"Error: {str(e)}")
        finally:
            self.execute_button.setText("Run Simulation")
            self.execute_button.setEnabled(True)

# Entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenModelicaApp()
    window.show()
    sys.exit(app.exec())
