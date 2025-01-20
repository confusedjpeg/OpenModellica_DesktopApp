# OpenModelica Simulation Desktop App

![Animated Demo]("assets/openModellica.gif")

## Description

This application provides a simple graphical user interface (GUI) for running simulations of OpenModelica models. It addresses the requirements of the FOSSEE screening task by allowing users to select a compiled OpenModelica model executable, specify start and stop times for the simulation, and view the output directly within the application.

This tool simplifies the process of interacting with compiled OpenModelica models, making it more accessible for users who prefer a desktop application interface over command-line execution.

## Features

*   **Executable Selection:** Allows users to browse and select the compiled OpenModelica model executable (`.exe` file).
*   **Start and Stop Time Input:** Provides input fields for specifying the simulation start and stop times as integers.
*   **Input Validation:** Ensures that the start and stop times are valid integers and adhere to the constraint `0 <= start time < stop time < 5`.
*   **Simulation Execution:** Executes the selected OpenModelica model with the provided start and stop time parameters.
*   **Output Display:** Captures and displays the standard output (stdout) and standard error (stderr) of the simulation process within the application.
*   **Status Bar:** Provides real-time feedback on the application's status (e.g., "Ready", "Running simulation...", "Simulation completed").
*   **Success/Error Messages:** Displays informative message boxes for successful simulations or errors encountered.
*   **Settings Persistence:** Remembers the last used executable path, start time, and stop time for future use.
*   **Dark Mode Theme:** Features a visually appealing dark mode interface with black and purple accents.
*   **Run Button Icon:** Includes a themed play icon on the "Run Simulation" button.

## Technologies Used

*   **Python 3.6+**
*   **PyQt6**
*   **OpenModelica**
*   **Windows 10/11 OS**

## Installation Instructions

1. **Install Python:** If you don't have Python 3.6 or later installed, download and install it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **Install PyQt6:** Open a command prompt or terminal and run the following command:
    ```bash
    pip install PyQt6
    ```
3. **Install OpenModelica:** This application requires OpenModelica to be installed separately. Download and install OpenModelica from the official website: [https://openmodelica.org/download/](https://openmodelica.org/download/)
4. **Clone the Repository:** Clone this GitHub repository to your local machine.
5. **Verify OpenModelica Files:** The necessary OpenModelica executable and its dependencies are already included in the repository within the `openmodelica_bin` folder. Ensure the following files are present in this folder:
    *   `TwoConnectedTanks.exe`.
    *   All required `.dll` files (these are essential for the executable to run).
    *   `TwoConnectedTanks_init.xml`.
6. **Run the Application:** Navigate to the root directory of the cloned repository in your command prompt or terminal and run the Python script:
    ```bash
    python app.py
    ```

## Usage Instructions

1. **Launch the Application:** Run the `app.py` script. The OpenModelica Desktop App window will appear.
2. **Select Executable:**
    *   Click the "Browse" button next to the "Application" field.
    *   Navigate to the `openmodelica_bin` folder within the repository.
    *   Select the compiled OpenModelica model executable (e.g., `TwoConnectedTanks.exe`) and click "Open".
3. **Enter Start Time:** In the "Start Time" field, enter an integer value between 0 (inclusive) and the stop time (exclusive).
4. **Enter Stop Time:** In the "Stop Time" field, enter an integer value greater than the start time and less than 5.
5. **Run Simulation:** Click the "Run Simulation" button.
6. **View Output:** The output of the simulation (stdout and stderr) will be displayed in the text area at the bottom of the window. The status bar will indicate the progress and outcome of the simulation.
7. **Error Handling:** If there are any issues (e.g., invalid input, executable not found, simulation errors), an appropriate error message will be displayed.

## Explanation of Files

*   **`main.py`:** This is the main Python script containing the PyQt6 GUI application code.
*   **`openmodelica_bin/`:** This folder contains the OpenModelica simulation files:
    *   `TwoConnectedTanks.exe` (or your compiled OpenModelica model executable): The compiled simulation program.
    *   All required `.dll` files: The necessary Dynamic Link Library files for the executable.
    *   `TwoConnectedTanks_init.xml`: The initialization file for the OpenModelica model.
*   **`assets/`:** This folder contains:
    *   `play_icon.png`: The custom purple play icon used for the "Run Simulation" button.
*   **`README.md`:** This file, providing documentation for the application.

## Potential Improvements

*   **More Advanced Styling Options:** Provide options for users to customize the application's theme.
*   **Asynchronous Execution with Progress Bar:** Implement asynchronous execution with a progress bar for long-running simulations to prevent the GUI from freezing.
*   **Platform Independence:** Explore the possibility of making the application cross-platform compatible.
