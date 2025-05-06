##Capacitance Measurement Unit Setup##
A Python-based GUI application for calculating the depletion region width of heterojunction diodes using capacitance-voltage (C-V) measurements. Developed as an end-term project for the Microfabrication Lab at Jaypee Institute of Information Technology, this tool provides a standalone Windows executable (CMU Setup.exe) for researchers, students, and engineers to analyze semiconductor junction properties.
Description
This application measures capacitance in heterojunction diodes (e.g., p-Si / n-ZnO) to extract key parameters like built-in potential, carrier concentration, and depletion width. It features a user-friendly GUI built with Tkinter, data processing with pandas and numpy, and graphical visualizations using matplotlib. The app integrates seamlessly with Keysight Source Measure Units (SMUs) for direct hardware interaction and supports CSV/Excel data input for offline analysis.
Key Features

##No Installation Required: Unzip and run CMU Setup.exe on Windows.##
Seamless Hardware Integration: Connects to Keysight SMU for real-time C-V measurements.
Data Visualization: Displays graphs for 1/C² vs. V, C vs. V, G vs. V, and a combined view.
Interactive GUI: Options to load CSV data, display device properties, view calculation steps, and show results.
Collaborative Workflow: Includes a Miro board for visual guidance and user comments (see Project Video).
Data Output: Exports results to CSV/Excel (e.g., CV sweep data.csv, CV sweep data.xlsx).

##Files##

CMU Setup.py: Main Python source code for the GUI and calculations.
CMU Setup.exe: Standalone Windows executable (78.4 MB).
cv.py: Script for C-V sweep functionality.
diode.ico: Custom icon for the application.

Sample Data
CV sweep data.xlsx: Data Extracted from the SMU Keysight B1500A
CV sweep data.csv: Warning!! Data Should be in this Format Befor Uploading
cv.spec: PyInstaller specification file for building the executable.

##Requirements##

For CMU Setup.exe:
Windows 10 or later.
No additional software needed.
Optional: Keysight SMU for hardware integration.


##For running CMU Setup.py or cv.py:##
Python 3.8+.
Install dependencies (see Installation).
Optional: LCR meter or impedance analyzer for data collection.



##Installation (For Developers)##
To run the source code or modify the project:

Clone this repository:git clone https://github.com/AsterioAstrixx/Capacitance-Measurement-Unit-Setup.git
cd Capacitance-Measurement-Unit-Setup


Create a virtual environment (optional but recommended):python -m venv .venv
.venv\Scripts\activate


Install dependencies:pip install pandas numpy matplotlib pillow scipy


Run the main script:python CMU Setup.py



##Usage##

Using the Executable:
Download CMU Setup.exe from the Releases section or the repository.
Unzip and double-click to launch the GUI.
Use the interface to:
Load CSV data (e.g., CV sweep data.csv).
View device properties (e.g., built-in potential, carrier concentration).
Follow calculation steps.
Visualize results (1/C² vs. V, C vs. V, G vs. V).


Connect a Keysight SMU for live measurements (if available).


Using the Source Code:
Follow the Installation steps.
Run CMU Setup.py for the GUI or cv.py for specific C-V sweep tasks.
Import CSV/Excel data or connect to hardware.



##Methodology##
The application performs C-V measurements as follows:

Connect Device: Use a Keysight SMU or LCR meter to apply an AC signal (100 kHz–1 MHz) with DC bias.
Bias Voltage Sweep: Vary DC voltage and measure capacitance.
Plot C-V Characteristics: Generate 1/C² vs. V plot to analyze junction properties.
Extract Parameters:
Built-in Potential (V_bi): From the intercept of 1/C² vs. V.
Carrier Concentration (N_A): From the slope of 1/C² vs. V.
Depletion Width (W): Calculated using the formula:[W = \sqrt{\frac{2\epsilon V_{bi}}{q N_A}}]where (\epsilon) is permittivity, (q) is the electron charge, and (N_A) is carrier concentration.



##Results##

Built-in Potential: ~2.545 V.
Carrier Concentration: ~10¹⁵ cm⁻³.
Linearity: R² ≈ 0.9912 for 1/C² vs. V plot.
Graphs: Visualizations for 1/C² vs. V, C vs. V, G vs. V, and combined plots.
Note: Depletion width calculation requires complete data, but trends confirm expected junction behavior.

##Resources## (For a Better Explanation and understanding Use these Resources :-) ✍️(◔◡◔)

Project Video: https://drive.google.com/file/d/1XP92MULKXaOrRymRVLaaxBXbez6fjpaW/view (Open in Browser)
Miro Board: https://miro.com/app/board/uXjVI96mjk4=/ (Open in Browser)

##Contributing##
Contributions are welcome! Please:

##Fork the repository.##
Create a feature branch (git checkout -b feature/YourFeature).
Commit changes (git commit -m 'Add YourFeature').
Push to the branch (git push origin feature/YourFeature).
Open a Pull Request.

##License##
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Made with Love by Ankur Majumdar <3 <3 (*^_^*) ^_____^
IG -https://www.instagram.com/majumdar.ankur_225/

Supervisor: Dr. Hemant Kumar, Jaypee Institute of Information Technology,Sec - 62,Noida
Lab: Microfabrication Lab.
Tools: Python, PyCharm, PyInstaller, Keysight SMU(B1500A)

