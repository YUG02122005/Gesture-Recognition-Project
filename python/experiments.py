"""
experiments.py — Data Quality Experiments
Short Circuit — Gesture Wand Project  |  Module 3

Runs four guided experiments that demonstrate how data quality affects
model performance. Each experiment modifies one aspect of the training
process and compares the result against a correctly-trained baseline.

Usage:
    python experiments.py

After running, compare each experiment's validation and test accuracy
against the baseline. Write a short paragraph for each explaining
what changed and why.

Experiments:
    1. No Normalization     — train without normalizing sensor channels
    2. Wrong Labels (30%)  — randomly shuffle 30% of training labels
    3. Imbalanced Dataset   — oversample idle, undersample gesture classes
    4. Overlapping Splits   — include test recordings in the training set
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from load_dataset import load_recordings, split_dataset, normalize, LABEL_MAP
from train_model  import build_model, train


# ─────────────────────────────────────────────────────────────
def _quick_test_accuracy(model, X_test, y_test, mean=None, std=None):
    """Helper: normalise if params given, then return test accuracy."""
    if mean is not None and std is not None:
        X_test = (X_test - mean) / (std + 1e-8)
    probs  = model.predict(X_test, verbose=0)
    y_pred = np.argmax(probs, axis=1)
    return accuracy_score(y_test, y_pred)


# ─────────────────────────────────────────────────────────────
def run_baseline(X, y):
    """
    Baseline: correctly split, normalized, and trained model.
    This is the reference — all experiments compare against this.

    Args:
        X (np.ndarray): Full dataset, shape (N, 100, 6).
        y (np.ndarray): Full labels,  shape (N,).

    Returns:
        dict with keys 'val_acc' and 'test_acc' (floats).

    This function is fully implemented — no changes needed.
    """
    X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(X, y)
    X_train, X_val, X_test, mean, std = normalize(X_train, X_val, X_test)

    model   = build_model()
    history = train(model, X_train, y_train, X_val, y_val)
    val_acc  = max(history.history["val_accuracy"])
    test_acc = _quick_test_accuracy(model, X_test, y_test, mean, std)
    return {"val_acc": val_acc, "test_acc": test_acc}


# ─────────────────────────────────────────────────────────────
def experiment_no_normalization(X, y):
    """
    Experiment 1 — Train without normalizing the sensor channels.

    Expected observation:
        Training is slower or fails to converge. Gyroscope channels
        (values in hundreds of °/s) dominate the loss, and the model
        may ignore the accelerometer channels entirely.

    Args:
        X (np.ndarray): Full dataset, shape (N, 100, 6).
        y (np.ndarray): Full labels,  shape (N,).

    Returns:
        dict with keys 'val_acc' and 'test_acc'.

    TODO: Implement this function.
        Steps:
          1. Split the dataset using split_dataset(X, y).
          2. DO NOT normalize — use the raw split arrays directly.
          3. Build a model and train it.
          4. Compute val_acc and test_acc WITHOUT applying normalization.
          5. Return {'val_acc': val_acc, 'test_acc': test_acc}.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def experiment_wrong_labels(X, y):
    """
    Experiment 2 — Randomly shuffle 30% of training labels.

    Expected observation:
        Training accuracy stays low because the model receives contradictory
        examples. Validation accuracy drops close to chance (25% for 4 classes).

    Args:
        X (np.ndarray): Full dataset, shape (N, 100, 6).
        y (np.ndarray): Full labels,  shape (N,).

    Returns:
        dict with keys 'val_acc' and 'test_acc'.

    TODO: Implement this function.
        Steps:
          1. Split and normalize using the standard functions.
          2. Corrupt 30% of y_train:
               a. Choose 30% of indices at random using np.random.choice.
               b. For each chosen index, replace the label with a random
                  integer in range [0, NUM_CLASSES) that is not the original.
          3. Train on corrupted y_train.
          4. Return val_acc and test_acc (evaluated on uncorrupted y_test).
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def experiment_imbalanced(X, y):
    """
    Experiment 3 — Heavily oversample the idle class.

    Expected observation:
        Overall accuracy appears high because the model learns to predict
        idle most of the time. Recall on gesture classes is very low.
        The confusion matrix shows most gestures misclassified as idle.

    Args:
        X (np.ndarray): Full dataset, shape (N, 100, 6).
        y (np.ndarray): Full labels,  shape (N,).

    Returns:
        dict with keys 'val_acc' and 'test_acc'.

    TODO: Implement this function.
        Steps:
          1. Find all recordings where y == 3 (idle class).
          2. Duplicate them 4 times — add them 4 more times to X and y.
             Use np.concatenate to combine arrays.
          3. Shuffle the dataset after duplication.
          4. Split, normalize, train, and return val_acc and test_acc.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def experiment_overlapping_splits(X, y):
    """
    Experiment 4 — Include test recordings in the training set (data leakage).

    Expected observation:
        Validation accuracy appears very high because the model has already
        seen the test recordings during training. Real-world performance
        (on genuinely new recordings) would be much lower.

    Args:
        X (np.ndarray): Full dataset, shape (N, 100, 6).
        y (np.ndarray): Full labels,  shape (N,).

    Returns:
        dict with keys 'val_acc' and 'test_acc'.

    TODO: Implement this function.
        Steps:
          1. Split the dataset using split_dataset(X, y).
          2. Combine X_train and X_test into one training array.
             Combine y_train and y_test into one training label array.
          3. Normalize using statistics from the combined training set.
          4. Train on the combined set.
          5. Evaluate on X_test (which was in the training set — this is leakage).
          6. Return val_acc and test_acc. Note how high test_acc is.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  Gesture Wand — Data Quality Experiments")
    print("=" * 60)

    print("\nLoading dataset...")
    X, y = load_recordings()

    experiments = [
        ("Baseline (correct)",       run_baseline),
        ("1 — No Normalization",     experiment_no_normalization),
        ("2 — Wrong Labels (30%)",   experiment_wrong_labels),
        ("3 — Imbalanced Dataset",   experiment_imbalanced),
        ("4 — Overlapping Splits",   experiment_overlapping_splits),
    ]

    results = {}
    for name, fn in experiments:
        print(f"\nRunning: {name} ...")
        try:
            r = fn(X, y)
            results[name] = r if r is not None else {"val_acc": 0.0, "test_acc": 0.0}
        except Exception as e:
            print(f"  Error: {e}")
            results[name] = {"val_acc": 0.0, "test_acc": 0.0}

    # ── Results table
    print("\n" + "=" * 60)
    print(f"  {'Experiment':<35} {'Val Acc':>10} {'Test Acc':>10}")
    print("=" * 60)
    baseline_test = results.get("Baseline (correct)", {}).get("test_acc", 0)
    for name, r in results.items():
        delta = r["test_acc"] - baseline_test
        sign  = "+" if delta >= 0 else ""
        print(
            f"  {name:<35} {r['val_acc']:>10.4f} {r['test_acc']:>10.4f}"
            + (f"  ({sign}{delta:.4f})" if name != "Baseline (correct)" else "")
        )
    print("=" * 60)
    print("\nWrite a short paragraph for each experiment explaining what changed and why.")


if __name__ == "__main__":
    main()
