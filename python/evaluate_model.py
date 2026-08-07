"""
evaluate_model.py — Test Set Evaluator
Short Circuit — Gesture Wand Project  |  Module 3

Loads the saved model and normalization parameters, evaluates the model
on the held-out test set, and generates a confusion matrix.

Run this ONCE after training is completely finished.
Do not use test set results to tune the model — that defeats its purpose.

Usage:
    python evaluate_model.py

Prerequisites:
    gesture_model.h5   — saved by train_model.py
    mean.npy           — saved by train_model.py
    std.npy            — saved by train_model.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
)
from tensorflow import keras

from load_dataset import load_recordings, split_dataset, LABEL_MAP

LABEL_NAMES = list(LABEL_MAP.keys())   # ["gesture_1", "gesture_2", "gesture_3", "idle"]


# ─────────────────────────────────────────────────────────────
def load_artifacts():
    """
    Loads the saved model and normalization parameters from disk.
    Prints an error and exits if any file is missing.

    Returns:
        model (keras.Model):   Trained model loaded from gesture_model.h5
        mean  (np.ndarray):    Per-channel mean, shape (6,)
        std   (np.ndarray):    Per-channel std,  shape (6,)
    """
    required = ["gesture_model.h5", "mean.npy", "std.npy"]
    for f in required:
        if not os.path.exists(f):
            raise FileNotFoundError(
                f"Missing: {f}. Run train_model.py first."
            )
    model = keras.models.load_model("gesture_model.h5")
    mean  = np.load("mean.npy")
    std   = np.load("std.npy")
    print("Model and normalization params loaded.")
    return model, mean, std


# ─────────────────────────────────────────────────────────────
def evaluate_model(model, X_test, y_test):
    """
    Evaluates the model on the held-out test set.

    Args:
        model  (keras.Model):  Trained model.
        X_test (np.ndarray):   Normalized test features, shape (N, 100, 6).
        y_test (np.ndarray):   True integer labels, shape (N,).

    Returns:
        accuracy (float):      Fraction of test recordings classified correctly.
        y_pred   (np.ndarray): Predicted integer class labels, shape (N,).

    TODO: Implement this function.
        Steps:
          1. Call model.predict(X_test) to get raw probability outputs.
             Shape of output: (N, num_classes)
          2. Convert probabilities to class predictions using np.argmax(axis=1).
          3. Compute accuracy: number of correct predictions / total predictions.
          4. Return accuracy and y_pred.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def plot_confusion_matrix(y_true, y_pred, label_names,
                          save_path="confusion_matrix.png"):
    """
    Generates and displays a confusion matrix.

    The diagonal shows correct predictions.
    Off-diagonal values show which classes are confused with which.

    Args:
        y_true      (np.ndarray): True labels.
        y_pred      (np.ndarray): Predicted labels.
        label_names (list of str): Class names in label order.
        save_path   (str):         File path for the saved figure.

    TODO: Implement this function.
        Steps:
          1. Compute the confusion matrix:
               cm = confusion_matrix(y_true, y_pred)
          2. Create a ConfusionMatrixDisplay and plot it:
               disp = ConfusionMatrixDisplay(cm, display_labels=label_names)
               fig, ax = plt.subplots(figsize=(7, 6))
               disp.plot(ax=ax, colorbar=False, cmap='Blues')
          3. Set the title to 'Confusion Matrix — Gesture Wand'.
          4. Save the figure and display it.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Gesture Wand — Model Evaluation")
    print("=" * 50)

    # Load saved artifacts
    model, mean, std = load_artifacts()

    # Reconstruct test set using the same split seed
    print("\nReconstructing test set...")
    X, y          = load_recordings()
    _, _, X_test, _, _, y_test = split_dataset(X, y)
    X_test        = (X_test - mean) / (std + 1e-8)

    # Evaluate
    print(f"\nTest set size: {len(y_test)} recordings")
    accuracy, y_pred = evaluate_model(model, X_test, y_test)

    if accuracy is None:
        print("Error: evaluate_model() returned None. Complete the TODO first.")
        return

    print(f"\nTest Accuracy: {accuracy * 100:.2f}%")

    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=LABEL_NAMES))

    # Confusion matrix
    plot_confusion_matrix(y_test, y_pred, LABEL_NAMES)


if __name__ == "__main__":
    main()
