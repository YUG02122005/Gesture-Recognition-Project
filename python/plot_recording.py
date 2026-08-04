"""
plot_recording.py — Gesture Recording Visualiser
Short Circuit — Gesture Wand Project

Usage:
    python plot_recording.py data/gesture_1/recording_001.csv

Plots all six sensor channels (ax, ay, az, gx, gy, gz) of a single
recording so you can visually inspect its quality before training.

What to look for:
    - A clear motion signature (spike, sweep, or rotation) on at least one axis
    - No flat lines (sensor not responding or wand stationary the whole window)
    - No obvious noise spikes that are much larger than the gesture signal
    - The same gesture class should produce a recognisable shape each time
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────────────────────
def load_recording(filepath: str) -> pd.DataFrame:
    """
    Loads one CSV recording into a pandas DataFrame.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Recording with columns [timestamp, ax, ay, az, gx, gy, gz].
                      Returns None if the file cannot be loaded.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


# ─────────────────────────────────────────────────────────────
def plot_recording(df: pd.DataFrame, filepath: str):
    """
    Plots accelerometer and gyroscope channels in two subplots.

    Args:
        df       (pd.DataFrame): Recording loaded from CSV.
        filepath (str):          Used in the figure title.
    """
    label = os.path.basename(os.path.dirname(filepath))
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Accelerometer
    ax1.plot(df["ax"], label="ax", linewidth=1.2)
    ax1.plot(df["ay"], label="ay", linewidth=1.2)
    ax1.plot(df["az"], label="az", linewidth=1.2)
    ax1.set_ylabel("Acceleration (g)")
    ax1.set_title(f"Class: {label}  |  File: {os.path.basename(filepath)}")
    ax1.legend(loc="upper right")
    ax1.grid(True, alpha=0.3)

    # Gyroscope
    ax2.plot(df["gx"], label="gx", linewidth=1.2)
    ax2.plot(df["gy"], label="gy", linewidth=1.2)
    ax2.plot(df["gz"], label="gz", linewidth=1.2)
    ax2.set_ylabel("Angular velocity (°/s)")
    ax2.set_xlabel("Sample index")
    ax2.legend(loc="upper right")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_recording.py <path_to_csv>")
        print("Example: python plot_recording.py data/gesture_1/recording_001.csv")
        sys.exit(1)

    filepath = sys.argv[1]
    df = load_recording(filepath)
    if df is not None:
        print(f"Loaded {len(df)} samples from {filepath}")
        plot_recording(df, filepath)


if __name__ == "__main__":
    main()
