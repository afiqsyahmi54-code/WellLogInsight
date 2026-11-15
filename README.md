# WellLog Insight

A desktop application for petrophysical well log analysis. Load a LAS file and instantly visualise Gamma Ray, Density, Neutron, and Resistivity logs — with automatic calculations for Vshale, Porosity, Water Saturation, and Reservoir identification.

---

## Features

- **Well Log Viewer** — View raw log tracks (GR, Density/Neutron, Resistivity) in a scrollable, depth-aligned display
- **Vshale Analysis** — Automatically calculates shale volume from Gamma Ray using the linear method
- **Porosity Analysis** — Density-Neutron crossplot porosity calculation
- **Water Saturation** — Archie's equation (adjustable m and n parameters)
- **Reservoir Identification** — Detects potential reservoir intervals using GR cut-off method and highlights them across all tracks
- **PDF Export** — Generates a professional multi-track petrophysical report as PDF
- **AI Module** *(in progress)* — Curve name recognition and data quality checking

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Kivy + KivyMD | Cross-platform UI framework |
| Matplotlib | Well log track plotting |
| NumPy + Pandas | Data processing |
| lasio | LAS file reading |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/afiqsyahmi54-code/WellLogInsight.git
cd WellLogInsight
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python main.py
```

### 5. Run the tests (optional)

```bash
pip install -r requirements-dev.txt
pytest
```

The tests cover the petrophysical calculations (reservoir interval detection, Vshale, porosity and Archie's equation), including a check against a straightforward reference implementation.

---

## How to Use

1. Launch the app and click **Get Started**
2. Enter well name, location, and depth range (optional)
3. Click **Upload LAS File** to load your well log file
4. Click **View Log** to see the raw log tracks
5. Navigate to **Interpretation** to run petrophysical analysis:
   - **Vshale** — Shale volume track
   - **Porosity** — Density-Neutron porosity track
   - **Water Saturation** — Sw track with hydrocarbon zone highlight
   - **Full Log Interpretation** — All tracks with reservoir intervals and adjustable Archie parameters
6. Use the **Save as PDF** button to export the report

---

## Project Structure

```
welllogapp/
├── main.py                        # App entry point
├── requirements.txt               # Python dependencies
├── ai_welllog.py                  # AI curve recognition module (in progress)
├── screens/                       # Screen logic (Python)
│   ├── start_screen.py
│   ├── welllog_screen.py
│   ├── viewlog_screen.py
│   ├── interpretation_screen.py
│   ├── vshale_screen.py
│   ├── porosity_screen.py
│   ├── water_saturation_screen.py
│   └── reservoir_screen.py
├── kv_files/                      # UI layouts (Kivy language)
├── utils/                         # Shared utilities
│   ├── android_file_utils.py      # LAS file reader
│   ├── calculations.py            # Vshale, porosity, Sw, reservoir intervals
│   ├── plot_utils.py              # Matplotlib plot helpers
│   └── constants.py               # Colour palette
├── tests/                         # Unit tests for the calculations
└── assets/                        # Icons and images
```

---

## Author

**Afiq Syahmi** — Final Year Project II (FYP II)
