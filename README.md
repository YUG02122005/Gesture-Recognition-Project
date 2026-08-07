<h1 align="center">Gesture Wand</h1>
<p align="center">
  <b>ESP32 · MPU6050 · TensorFlow Lite · Flask</b><br/>
  A complete embedded gesture recognition system built for the Short Circuit program
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-ESP32-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Language-C%2B%2B%20%7C%20Python-informational?style=flat-square"/>
  <img src="https://img.shields.io/badge/Framework-TensorFlow%20Lite-orange?style=flat-square"/>
  <img src="https://img.shields.io/badge/Program-Short%20Circuit-green?style=flat-square"/>
</p>

---

## What the Wand Does

The finished device reads six-axis motion data from an MPU6050 IMU, runs a 1D convolutional neural network directly on the ESP32, and classifies physical hand gestures in real time. Predictions are streamed to a local Flask dashboard where gesture labels and confidence scores are displayed in a browser. The model never leaves the device — all inference happens at the edge.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Gesture Wand                             │
│                                                                 │
│  ┌───────────┐   I2C    ┌──────────────┐   TFLite   ┌────────┐ │
│  │  MPU6050  │─────────▶│    ESP32     │────────────▶│  LED / │ │
│  │   6-axis  │          │  Inference   │            │  OLED  │ │
│  │    IMU    │          │   (on-chip)  │            └────────┘ │
│  └───────────┘          └──────┬───────┘                       │
│                                │ Serial                         │
└────────────────────────────────┼────────────────────────────────┘
                                 │
                          ┌──────▼───────┐
                          │   Python /   │
                          │    Flask     │
                          │  Dashboard   │
                          └──────────────┘
```

---

## Project Modules

| Module | Topic | Key Deliverable | Status |
|--------|--------|-----------------|--------|
| **1** | IMU Data Acquisition | Stream six-axis sensor data at 50 Hz | `firmware/` |
| **2** | Data Collection Pipeline | Record and save labeled gesture datasets | `python/collect_data.py` |
| **3** | Model Training | Train a 1D CNN gesture classifier | `python/train_model.py` |
| **4** | On-Device Inference | Run TFLite model on the ESP32 | *(coming)* |
| **5** | Flask Dashboard | Display predictions in a browser | *(coming)* |

---

## Quick Start

### 1 — Clone the repository
```bash
git clone https://github.com/YugBhimaniii/Gesture-Recognition-Project.git
cd Gesture-Recognition-Project
```

### 2 — Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3 — Open the firmware
- Open `firmware/imu_reader/imu_reader.ino` in Arduino IDE
- Select board: **Tools → Board → ESP32 Dev Module**
- Select port: **Tools → Port → COMx**
- Flash to the ESP32

---

## Repository Structure

```
gesture-wand/
│
├── firmware/                         ← ESP32 Arduino firmware
│   └── imu_reader/
│       ├── config.h                  ← All constants — edit here only
│       ├── mpu6050.h                 ← Driver interface (read this first)
│       ├── mpu6050.cpp               ← Module 1 — TODO: implement driver
│       └── imu_reader.ino            ← Module 1+2 — TODO: stream + record
│
├── python/                           ← All Python tools
│   ├── collect_data.py               ← Module 2 — TODO: data collection tool
│   ├── plot_recording.py             ← Module 2 — visualise a recording
│   ├── validate_dataset.py           ← Module 2 — check dataset quality
│   ├── load_dataset.py               ← Module 3 — TODO: load and preprocess
│   ├── train_model.py                ← Module 3 — TODO: build and train CNN
│   ├── evaluate_model.py             ← Module 3 — TODO: test set evaluation
│   └── experiments.py               ← Module 3 — TODO: data quality experiments
│
├── data/                             ← Gesture recordings (auto-generated)
│   ├── gesture_1/
│   ├── gesture_2/
│   ├── gesture_3/
│   └── idle/
│
├── requirements.txt
└── README.md
```

---

## Module Guide

### Module 1 — IMU Data Acquisition

**Goal:** Read six-axis sensor data from the MPU6050 over I2C and stream it over Serial at 50 Hz.

**Files to implement:**
- `firmware/imu_reader/mpu6050.cpp` — complete `initMPU()` and `readMPU()`
- `firmware/imu_reader/imu_reader.ino` — enable `MODE_STREAM`

**Verify:** Open Serial Monitor at 115200 baud. You should see a continuous CSV stream:
```
timestamp,ax,ay,az,gx,gy,gz
1023,0.0012,-0.0034,1.0021,0.12,-0.04,0.01
...
```

---

### Module 2 — Data Collection Pipeline

**Goal:** Add a triggered recording mode to the firmware and build a Python tool that saves labeled gesture recordings to CSV files.

**Files to implement:**
- `firmware/imu_reader/imu_reader.ino` — enable `MODE_RECORD`, complete the recording loop
- `python/collect_data.py` — complete `trigger_recording()`, `save_recording()`, `plot_recording()`

**Run the data collection tool:**
> ⚠️ Close the Arduino IDE Serial Monitor before running.

```bash
cd python
python collect_data.py
```

**Validate your dataset:**
```bash
python validate_dataset.py
```

**Plot a single recording:**
```bash
python plot_recording.py data/gesture_1/recording_001.csv
```

**Serial message protocol:**

| Message | Direction | Meaning |
|---------|-----------|---------|
| `r` (ASCII 114) | Python → ESP32 | Start one 100-sample recording |
| CSV row | ESP32 → Python | One sample of sensor data |
| `END` | ESP32 → Python | Recording complete |

**Data folder structure:**
```
data/
├── gesture_1/    ← recording_001.csv, recording_002.csv ...
├── gesture_2/
├── gesture_3/
└── idle/
```

---

### Module 3 — Model Training

**Goal:** Load your recorded dataset, normalize it, train a 1D CNN, and evaluate it on held-out test recordings.

**Files to implement:**
- `python/load_dataset.py` — complete `split_dataset()` and `normalize()`
- `python/train_model.py` — complete `build_model()` and `train()`
- `python/evaluate_model.py` — complete `evaluate_model()` and `plot_confusion_matrix()`
- `python/experiments.py` — complete all four experiment functions

**Train the model:**
```bash
cd python
python train_model.py
```

**Evaluate on the test set:**
```bash
python evaluate_model.py
```

**Run the four guided experiments:**
```bash
python experiments.py
```

**Outputs after training:**
```
python/
├── gesture_model.h5      ← saved Keras model
├── mean.npy              ← normalization mean (6 values)
├── std.npy               ← normalization std  (6 values)
└── training_curves.png   ← accuracy and loss plots
```

---

## Label Map

| Class | Integer | Description |
|-------|---------|-------------|
| `gesture_1` | 0 | Your first gesture |
| `gesture_2` | 1 | Your second gesture |
| `gesture_3` | 2 | Your third gesture |
| `idle` | 3 | Wand at rest |

---

## Hardware

| Component | Specification |
|-----------|---------------|
| Microcontroller | ESP32 (240 MHz dual-core, 520 KB SRAM) |
| IMU | MPU6050 — 3-axis accelerometer + 3-axis gyroscope |
| Communication | I2C — SDA: GPIO 21, SCL: GPIO 22 |
| Baud rate | 115200 |
| Sample rate | 50 Hz |
| Recording window | 100 samples (2 seconds) |

---

## Support

Questions? Contact us at **support@shortcct.com**
