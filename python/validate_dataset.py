"""
validate_dataset.py — Dataset Quality Checker
Short Circuit — Gesture Wand Project

Usage:
    python validate_dataset.py

Scans every CSV file in the data/ folder and reports:
    - Number of recordings per class
    - Number of recordings with the correct length (100 samples)
    - Min and max sensor values across all six axes
    - Files flagged as potentially problematic

Run this after every data collection session before moving to training.
Fix any flagged recordings before training — bad data produces bad models.
"""

import os
import pandas as pd

DATA_DIR       = "data"
RECORD_SAMPLES = 100
VALID_LABELS   = ["gesture_1", "gesture_2", "gesture_3", "idle"]


# ─────────────────────────────────────────────────────────────
def check_class(label: str) -> dict:
    """
    Checks all recordings in one gesture class folder.

    Args:
        label (str): Class name, e.g. 'gesture_1'

    Returns:
        dict with keys:
            total        (int)  — total number of CSV files found
            correct_len  (int)  — files with exactly RECORD_SAMPLES rows
            flagged      (list) — filenames that failed one or more checks
            ax_range     (tuple)— (min, max) for accelerometer X across all files
            gz_range     (tuple)— (min, max) for gyroscope Z across all files
    """
    folder = os.path.join(DATA_DIR, label)
    if not os.path.exists(folder):
        return {"total": 0, "correct_len": 0, "flagged": [], "ax_range": (0, 0), "gz_range": (0, 0)}

    files      = [f for f in os.listdir(folder) if f.endswith(".csv")]
    total      = len(files)
    correct    = 0
    flagged    = []
    ax_vals    = []
    gz_vals    = []

    for fname in sorted(files):
        path = os.path.join(folder, fname)
        try:
            df = pd.read_csv(path)

            # Check length
            if len(df) == RECORD_SAMPLES:
                correct += 1
            else:
                flagged.append(f"{fname} — wrong length ({len(df)} samples, expected {RECORD_SAMPLES})")

            # Check for constant axes (possible wiring fault)
            for col in ["ax", "ay", "az", "gx", "gy", "gz"]:
                if col in df.columns and df[col].std() < 0.001:
                    flagged.append(f"{fname} — {col} is constant (possible sensor fault)")
                    break

            # Collect value ranges
            if "ax" in df.columns:
                ax_vals.extend(df["ax"].tolist())
            if "gz" in df.columns:
                gz_vals.extend(df["gz"].tolist())

        except Exception as e:
            flagged.append(f"{fname} — could not read file ({e})")

    ax_range = (min(ax_vals), max(ax_vals)) if ax_vals else (0, 0)
    gz_range = (min(gz_vals), max(gz_vals)) if gz_vals else (0, 0)

    return {
        "total":       total,
        "correct_len": correct,
        "flagged":     flagged,
        "ax_range":    ax_range,
        "gz_range":    gz_range,
    }


# ─────────────────────────────────────────────────────────────
def print_report(results: dict):
    """
    Prints a formatted summary report for all gesture classes.

    Args:
        results (dict): Keys are class labels, values are dicts from check_class().
    """
    print("\n" + "=" * 60)
    print("  DATASET VALIDATION REPORT")
    print("=" * 60)

    total_recordings = 0
    all_balanced     = True
    counts           = {}

    for label, r in results.items():
        counts[label] = r["total"]
        total_recordings += r["total"]

        status = "OK" if not r["flagged"] and r["correct_len"] == r["total"] else "ISSUES FOUND"
        print(f"\n  {label.upper()} — {status}")
        print(f"    Recordings   : {r['total']}")
        print(f"    Correct length: {r['correct_len']} / {r['total']}")
        print(f"    ax range     : [{r['ax_range'][0]:.3f}, {r['ax_range'][1]:.3f}] g")
        print(f"    gz range     : [{r['gz_range'][0]:.3f}, {r['gz_range'][1]:.3f}] °/s")

        if r["flagged"]:
            print(f"    Flagged files ({len(r['flagged'])}):")
            for f in r["flagged"]:
                print(f"      ⚠  {f}")

    # Balance check
    if counts:
        min_count = min(counts.values())
        max_count = max(counts.values())
        if max_count > 0 and max_count / max(min_count, 1) > 2:
            all_balanced = False

    print("\n" + "-" * 60)
    print(f"  Total recordings : {total_recordings}")
    print(f"  Class balance    : {'OK' if all_balanced else 'IMBALANCED — some classes have 2x more recordings than others'}")
    print("=" * 60 + "\n")


# ─────────────────────────────────────────────────────────────
def main():
    print("Scanning data/ folder...")
    results = {}
    for label in VALID_LABELS:
        results[label] = check_class(label)
    print_report(results)


if __name__ == "__main__":
    main()
