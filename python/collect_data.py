"""
collect_data.py — Gesture Data Collection Tool
Short Circuit — Gesture Wand Project

Usage:
    python collect_data.py

What this tool does:
    1. Opens the Serial port connected to the ESP32.
    2. Prompts the student to select a gesture label.
    3. Sends 'r' to the ESP32 to trigger one recording.
    4. Receives exactly RECORD_SAMPLES CSV rows from the ESP32.
    5. Saves the recording to data/<label>/recording_XXX.csv
    6. Offers to plot the saved recording.
    7. Repeats until the student types 'quit'.

Serial message protocol:
    Python → ESP32 : 'r'   (single byte, triggers one recording)
    ESP32 → Python : CSV rows (one per sample, 100 total)
    ESP32 → Python : 'END' (signals recording is complete)
"""

import os
import sys
import serial
import serial.tools.list_ports
import pandas as pd

# ── Configuration ─────────────────────────────────────────────
BAUD_RATE      = 115200
RECORD_SAMPLES = 100
DATA_DIR       = "data"
VALID_LABELS   = ["gesture_1", "gesture_2", "gesture_3", "idle"]
CSV_HEADER     = ["timestamp", "ax", "ay", "az", "gx", "gy", "gz"]


# ─────────────────────────────────────────────────────────────
def list_ports():
    """
    Lists all available Serial ports on the current computer.
    Prints each port name and description so the student can
    identify which port the ESP32 is connected to.
    """
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No Serial ports found. Check USB connection.")
        return
    print("\nAvailable ports:")
    for p in ports:
        print(f"  {p.device} — {p.description}")
    print()


# ─────────────────────────────────────────────────────────────
def open_port(port: str) -> serial.Serial:
    """
    Opens the Serial port at BAUD_RATE with a 5-second timeout.

    Args:
        port (str): Serial port name, e.g. 'COM3' or '/dev/ttyUSB0'

    Returns:
        serial.Serial: Open Serial connection ready for read/write.

    Raises:
        SystemExit: If the port cannot be opened (wrong name, in use, etc.)
    """
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=5)
        print(f"Opened {port} at {BAUD_RATE} baud.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening port: {e}")
        print("Close the Arduino IDE Serial Monitor and try again.")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
def next_filename(label: str) -> str:
    """
    Returns the next available filename for a given gesture label.
    Files are numbered sequentially: recording_001.csv, recording_002.csv ...

    Args:
        label (str): Gesture class name, e.g. 'gesture_1'

    Returns:
        str: Full path to the next file, e.g. 'data/gesture_1/recording_003.csv'
    """
    folder = os.path.join(DATA_DIR, label)
    os.makedirs(folder, exist_ok=True)
    existing = [f for f in os.listdir(folder) if f.endswith(".csv")]
    index = len(existing) + 1
    return os.path.join(folder, f"recording_{index:03d}.csv")


# ─────────────────────────────────────────────────────────────
def trigger_recording(ser: serial.Serial) -> list:
    """
    Sends the 'r' command to the ESP32 and collects the response.
    Reads CSV rows line by line until 'END' is received.

    Args:
        ser (serial.Serial): Open Serial connection to the ESP32.

    Returns:
        list of str: Raw CSV rows received before 'END'.
                     Each string is one complete CSV line.

    TODO: Implement this function.
        Steps:
          1. Flush any bytes already in the input buffer: ser.reset_input_buffer()
          2. Send the record command:  ser.write(b'r')
          3. Read the header line first (the ESP32 sends the CSV header).
          4. Read lines in a loop using ser.readline().decode().strip()
          5. Stop when you receive the string 'END'.
          6. Return the list of data rows (not the header, not 'END').
          7. If fewer than RECORD_SAMPLES rows are received, print a warning.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def save_recording(rows: list, filepath: str) -> pd.DataFrame:
    """
    Saves the raw CSV rows to a file and returns a DataFrame.

    Args:
        rows     (list of str): Raw CSV rows from trigger_recording().
        filepath (str):         Full path where the file should be saved.

    Returns:
        pd.DataFrame: The recording as a DataFrame with columns from CSV_HEADER.

    TODO: Implement this function.
        Steps:
          1. Write the header (CSV_HEADER joined by commas) as the first line.
          2. Write each row in rows as a line.
          3. Read the file back into a pandas DataFrame using pd.read_csv().
          4. Print the filepath so the student can confirm where it was saved.
          5. Return the DataFrame.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def plot_recording(df: pd.DataFrame, label: str, filepath: str):
    """
    Plots all six sensor channels of one recording.
    Accelerometer channels (ax, ay, az) in one subplot.
    Gyroscope channels (gx, gy, gz) in a second subplot.

    Args:
        df       (pd.DataFrame): Recording loaded from CSV.
        label    (str):          Gesture class name for the plot title.
        filepath (str):          File path shown in the plot title.

    TODO: Implement this function.
        Steps:
          1. Import matplotlib.pyplot as plt inside the function (or at top of file).
          2. Create a figure with two vertically stacked subplots (fig, (ax1, ax2)).
          3. Plot df['ax'], df['ay'], df['az'] on ax1. Label each line.
          4. Plot df['gx'], df['gy'], df['gz'] on ax2. Label each line.
          5. Set axis titles: 'Accelerometer (g)' and 'Gyroscope (°/s)'.
          6. Set x-axis label to 'Sample index'.
          7. Add a legend and a figure title showing label and filepath.
          8. Call plt.tight_layout() and plt.show().
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def main():
    list_ports()
    port = input("Enter Serial port (e.g. COM3 or /dev/ttyUSB0): ").strip()
    ser  = open_port(port)

    # Discard startup messages from ESP32
    import time
    time.sleep(2)
    ser.reset_input_buffer()
    print("Connected. Type a label to start recording, or 'quit' to exit.")
    print(f"Valid labels: {', '.join(VALID_LABELS)}\n")

    while True:
        label = input("Gesture label: ").strip().lower()

        if label == "quit":
            print("Exiting.")
            ser.close()
            break

        if label not in VALID_LABELS:
            print(f"Invalid label. Choose from: {', '.join(VALID_LABELS)}")
            continue

        input(f"  Prepare to perform '{label}'. Press Enter to record...")

        rows = trigger_recording(ser)
        if rows is None:
            print("  Recording failed. Try again.")
            continue

        filepath = next_filename(label)
        df       = save_recording(rows, filepath)

        if df is not None:
            print(f"  Saved: {filepath}  ({len(df)} samples)")
            show = input("  Plot this recording? (y/n): ").strip().lower()
            if show == "y":
                plot_recording(df, label, filepath)

        print()


if __name__ == "__main__":
    main()
