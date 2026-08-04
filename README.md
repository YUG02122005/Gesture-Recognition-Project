# Gesture Wand Project
**Short Circuit — Gesture Recognition on ESP32**

A step-by-step project that teaches students to build a complete gesture recognition system using an ESP32 microcontroller, MPU6050 IMU, TensorFlow Lite, and a Python Flask dashboard.

---

## Repository Structure

```
gesture-wand/
├── arduino/
│   └── imu_reader/
│       ├── imu_reader.ino      — main firmware (stream + record modes)
│       ├── config.h            — all constants (edit this file only)
│       ├── mpu6050.h           — driver interface
│       └── mpu6050.cpp         — driver skeleton (students implement this)
├── python/
│   ├── collect_data.py         — data collection tool (students implement TODOs)
│   ├── plot_recording.py       — visualise a single recording
│   └── validate_dataset.py     — check dataset quality
├── data/
│   ├── gesture_1/              — recordings go here automatically
│   ├── gesture_2/
│   ├── gesture_3/
│   └── idle/
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/short-circuit-edu/gesture-wand.git
cd gesture-wand
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Open the firmware in Arduino IDE
- Open `arduino/imu_reader/imu_reader.ino`
- Install the **Wire** library (built-in with Arduino IDE)
- Select your ESP32 board: **Tools → Board → ESP32 Dev Module**
- Select the correct port: **Tools → Port**

---

## Module 1 — IMU Data Acquisition

**Goal:** Read six-axis sensor data from the MPU6050 and stream it over Serial at 50 Hz.

**Student tasks:**
1. Implement `initMPU()` in `mpu6050.cpp`
2. Implement `readMPU()` in `mpu6050.cpp`
3. In `imu_reader.ino`, uncomment `#define MODE_STREAM`

**Verify:** Open the Serial Monitor at 115200 baud. You should see a continuous CSV stream of timestamped sensor readings.

---

## Module 2 — Data Collection Pipeline

**Goal:** Build a triggered recording mode and collect a labeled gesture dataset.

### Firmware setup
1. In `imu_reader.ino`, uncomment `#define MODE_RECORD` (comment out `MODE_STREAM`)
2. Implement the recording mode in the `#ifdef MODE_RECORD` block (see TODO comments)
3. Flash the firmware to your ESP32

### Running the data collection tool
**Close the Arduino IDE Serial Monitor before running the Python tool.**

```bash
cd python
python collect_data.py
```

The tool will:
1. List available Serial ports — enter the one your ESP32 is connected to
2. Ask for a gesture label — type one of: `gesture_1`, `gesture_2`, `gesture_3`, `idle`
3. Send 'r' to the ESP32 and capture 100 samples
4. Save the recording automatically to `data/<label>/recording_XXX.csv`
5. Offer to plot the recording for visual inspection

### Student tasks
Complete the TODO functions in `collect_data.py`:
- `trigger_recording()` — sends 'r', reads CSV rows until 'END'
- `save_recording()` — writes rows to CSV file, returns DataFrame
- `plot_recording()` — plots all six channels in two subplots

### Serial message protocol
| Message | Direction | Meaning |
|---|---|---|
| `r` (ASCII 114) | Python → ESP32 | Start one 100-sample recording |
| CSV row | ESP32 → Python | One sample of sensor data |
| `END` | ESP32 → Python | Recording complete |

### Validating your dataset
```bash
python validate_dataset.py
```
Run this after every collection session. Fix flagged files before training.

### Plotting a single recording
```bash
python plot_recording.py data/gesture_1/recording_001.csv
```

---

## Data Folder Structure

```
data/
├── gesture_1/
│   ├── recording_001.csv
│   ├── recording_002.csv
│   └── ...
├── gesture_2/
├── gesture_3/
└── idle/
```

Each CSV file contains 100 rows with columns: `timestamp, ax, ay, az, gx, gy, gz`

---

## Support

Questions? Contact us at support@shortcct.com
