# 🧪 Capacitance Measurement Unit Setup

A Python-based GUI application for calculating the depletion region width of heterojunction diodes using **C-V measurements**. Developed as an end-term project for the **Microfabrication Lab at Jaypee Institute of Information Technology**, this tool provides a standalone Windows executable for researchers, students, and engineers.

![CMU GUI Demo](demo.gif) <!-- Add a GIF or screenshot here -->

---

## 📌 Description

This application analyzes **capacitance in heterojunction diodes** (e.g., p-Si / n-ZnO) to extract:

- Built-in potential  
- Carrier concentration  
- Depletion width  

Built with:
- `Tkinter` (GUI)
- `pandas`, `numpy` (data processing)
- `matplotlib` (graphical visualization)  
- **Keysight SMU integration**  
- **Offline CSV/Excel analysis support**

---

## ✨ Key Features

- ✅ **No Installation Required:** Unzip and run `CMU Setup.exe`
- 🔌 **Hardware Integration:** Connects to Keysight SMUs for real-time C-V data
- 📊 **Visual Analytics:** Plots `1/C² vs V`, `C vs V`, `G vs V`, and combo views
- 🧑‍💻 **Interactive GUI:** Load CSV, view device properties, calculation steps, and export results
- 🧠 **Collaborative Tools:** Includes [Miro Board](https://miro.com/app/board/uXjVI96mjk4=/) & [Project Video](https://drive.google.com/file/d/1XP92MULKXaOrRymRVLaaxBXbez6fjpaW/view)
- 📤 **Data Export:** Save outputs as `.csv` or `.xlsx`

---

## 📁 Files Included

| File | Description |
|------|-------------|
| `CMU Setup.py` | Main Python script |
| `CMU Setup.exe` | Standalone Windows executable (78.4 MB) |
| `cv.py` | C-V sweep control script |
| `diode.ico` | Custom application icon |
| `CV sweep data.xlsx` | Sample extracted data |
| `CV sweep data.csv` | ⚠️ Must follow this format before uploading |
| `cv.spec` | PyInstaller spec file |

---

## 💻 Requirements

### For `CMU Setup.exe`:
- ✅ Windows 10 or later  
- 🔌 Optional: Keysight SMU  

### For running `CMU Setup.py` or `cv.py`:
- Python 3.8+
- Dependencies:
  ```bash
  pip install pandas numpy matplotlib pillow scipy

## 🚀 Usage

### Using the Executable:
- Download `CMU Setup.exe` from the [Releases](https://github.com/AsterioAstrixx/Capacitance-Measurement-Unit---Parameter-Extraction-Setup/releases)
- Unzip and double-click it
- Use the GUI to:
  - Load CSV (e.g., `CV sweep data.csv`)
  - View built-in potential, carrier concentration
  - Visualize 1/C², C, and G vs Voltage
  - Export results

### Using the Source Code:
- Run `CMU Setup.py` or `cv.py` directly
- Can work with real-time Keysight SMU or offline data

---

## 🧠 Methodology

- **Hardware**: Connect diode with a Keysight SMU or LCR meter  
- **Sweep Voltage**: Apply DC bias with AC frequency (100 kHz–1 MHz)  
- **C-V Plot**: Visualize 1/C² vs V  

### Extract Parameters:
- **Built-in Potential (V_bi)** – Intercept of 1/C² vs V  
- **Carrier Concentration (N_A)** – Slope of 1/C² vs V  
- **Depletion Width (W)**:

## 📊 Results

| Parameter              | Value            |
|------------------------|------------------|
| Built-in Potential     | ~2.545 V         |
| Carrier Concentration  | ~10¹⁵ cm⁻³       |
| Linearity (R²)         | ≈ 0.9912         |

✅ Includes all 3 plots:  
✔ 1/C² vs V | ✔ C vs V | ✔ G vs V

---

## 🎥 Resources

- 📹 **Project Video**: [Watch here](https://drive.google.com/file/d/1XP92MULKXaOrRymRVLaaxBXbez6fjpaW/view)
- 🧭 **Miro Board**: [Explore here](https://miro.com/app/board/uXjVI96mjk4=/)

---

## 🤝 Contributing

1. **Fork** the repo  
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/YourFeature

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

**Made with ❤️ by Ankur Majumdar**  
🔗 IG: [@majumdar.ankur_225](https://www.instagram.com/majumdar.ankur_225)

**Supervisor**: Dr. Hemant Kumar  
**Institute**: Jaypee Institute of Information Technology  
**Lab**: Microfabrication Lab  
**Tools**: Python, PyCharm, PyInstaller, Keysight B1500A


