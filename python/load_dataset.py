"""
load_dataset.py — Dataset Loader and Preprocessor
Short Circuit — Gesture Wand Project  |  Module 3

Loads all gesture recordings from the data/ folder, maps class names
to integers, and splits the dataset into training, validation, and
held-out test sets. Computes normalization statistics from the
training set only and applies them to all three sets.

Usage:
    Import the functions from train_model.py and evaluate_model.py.
    Do not run this file directly — it is a shared module.

Output arrays:
    X — shape (N, 100, 6)   float32   N recordings, 100 timesteps, 6 channels
    y — shape (N,)          int32     one integer class label per recording
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# ── Configuration ─────────────────────────────────────────────
RECORD_SAMPLES = 100
CHANNELS       = 6
DATA_DIR       = os.path.join(os.path.dirname(__file__), "..", "data")

# Class label → integer mapping.
# This mapping must stay consistent across training, saving, and inference.
LABEL_MAP = {
    "gesture_1": 0,
    "gesture_2": 1,
    "gesture_3": 2,
    "idle":      3,
}

SENSOR_COLS = ["ax", "ay", "az", "gx", "gy", "gz"]


# ─────────────────────────────────────────────────────────────
def load_recordings(data_dir: str = DATA_DIR):
    """
    Walks through data/ and loads every valid CSV recording.

    A recording is valid if:
      - It contains exactly RECORD_SAMPLES rows
      - It contains all six sensor columns

    Invalid files are skipped with a warning printed to the terminal.

    Args:
        data_dir (str): Path to the data/ folder.

    Returns:
        X (np.ndarray): shape (N, 100, 6), dtype float32
        y (np.ndarray): shape (N,),        dtype int32
    """
    X, y = [], []

    for label, class_id in LABEL_MAP.items():
        folder = os.path.join(data_dir, label)
        if not os.path.exists(folder):
            print(f"  Warning: folder not found — {folder}")
            continue

        files = sorted([f for f in os.listdir(folder) if f.endswith(".csv")])
        for fname in files:
            fpath = os.path.join(folder, fname)
            try:
                df = pd.read_csv(fpath)
                if not all(col in df.columns for col in SENSOR_COLS):
                    print(f"  Skip: missing columns — {fname}")
                    continue
                arr = df[SENSOR_COLS].values.astype(np.float32)
                if arr.shape != (RECORD_SAMPLES, CHANNELS):
                    print(f"  Skip: wrong shape {arr.shape} — {fname}")
                    continue
                X.append(arr)
                y.append(class_id)
            except Exception as e:
                print(f"  Skip: could not read {fname} — {e}")

    if len(X) == 0:
        raise ValueError(
            "No valid recordings found. "
            "Run collect_data.py first and check the data/ folder."
        )

    print(f"Loaded {len(X)} recordings across {len(LABEL_MAP)} classes.")
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)


# ─────────────────────────────────────────────────────────────
def split_dataset(X, y, val_size=0.15, test_size=0.15, random_state=42):
    """
    Splits X and y into non-overlapping training, validation, and test sets.

    The same recording must never appear in more than one set.
    Splitting is stratified — each set contains a proportional mix of classes.

    Args:
        X            (np.ndarray): Full dataset, shape (N, 100, 6).
        y            (np.ndarray): Full labels,  shape (N,).
        val_size     (float):      Fraction of full dataset for validation.
        test_size    (float):      Fraction of full dataset for test.
        random_state (int):        Seed for reproducibility.

    Returns:
        X_train, X_val, X_test  (np.ndarray): Feature arrays.
        y_train, y_val, y_test  (np.ndarray): Label arrays.

    TODO: Implement this function.
        Steps:
          1. Split X, y into (trainval, test) using test_size.
             Use train_test_split with stratify=y and random_state.
          2. Compute the fraction of trainval needed for validation.
             val_fraction = val_size / (1.0 - test_size)
          3. Split trainval into (train, val) using val_fraction.
          4. Print the size of each split to the terminal.
          5. Return X_train, X_val, X_test, y_train, y_val, y_test.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def normalize(X_train, X_val, X_test):
    """
    Applies z-score normalization using statistics from X_train only.

    Z-score: X_normalized = (X - mean) / (std + epsilon)
    mean and std are computed per channel (axis 0 and 1 of X_train).
    The same mean and std are applied to X_val and X_test.

    Args:
        X_train (np.ndarray): Training set,   shape (N_train, 100, 6).
        X_val   (np.ndarray): Validation set, shape (N_val,   100, 6).
        X_test  (np.ndarray): Test set,       shape (N_test,  100, 6).

    Returns:
        X_train_norm (np.ndarray): Normalized training set.
        X_val_norm   (np.ndarray): Normalized validation set.
        X_test_norm  (np.ndarray): Normalized test set.
        mean         (np.ndarray): Per-channel mean, shape (6,). Save this.
        std          (np.ndarray): Per-channel std,  shape (6,). Save this.

    TODO: Implement this function.
        Steps:
          1. Compute mean = X_train.mean(axis=(0, 1))   — shape (6,)
          2. Compute std  = X_train.std(axis=(0, 1))    — shape (6,)
          3. Normalize each set:  X_norm = (X - mean) / (std + 1e-8)
          4. Print mean and std values for each sensor channel.
          5. Return all five values.

    Hint: mean and std must be saved to disk in train_model.py so that
          the same values can be applied during inference on the ESP32.
    """
    # TODO — your implementation here
    pass
