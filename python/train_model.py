"""
train_model.py — 1D CNN Trainer
Short Circuit — Gesture Wand Project  |  Module 3

Builds a 1D convolutional neural network, trains it on the gesture
dataset, plots accuracy and loss curves, and saves the trained model
and normalization parameters to disk.

Usage:
    python train_model.py

Outputs (saved to python/ folder):
    gesture_model.h5   — trained Keras model
    mean.npy           — per-channel normalization mean (shape: 6,)
    std.npy            — per-channel normalization std  (shape: 6,)
    training_curves.png — accuracy and loss plots
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from load_dataset import load_recordings, split_dataset, normalize, LABEL_MAP

# ── Training Hyperparameters ──────────────────────────────────
EPOCHS      = 50
BATCH_SIZE  = 32
NUM_CLASSES = len(LABEL_MAP)   # 4
INPUT_SHAPE = (100, 6)         # 100 timesteps, 6 sensor channels


# ─────────────────────────────────────────────────────────────
def build_model(input_shape=INPUT_SHAPE, num_classes=NUM_CLASSES):
    """
    Builds and compiles a 1D CNN for gesture classification.

    Architecture (implement this):
        Input → Conv1D(32, 3, relu) → MaxPool(2)
               → Conv1D(64, 3, relu) → MaxPool(2)
               → Flatten
               → Dense(64, relu) → Dropout(0.3)
               → Dense(num_classes, softmax)

    Args:
        input_shape (tuple): Shape of one recording — (100, 6).
        num_classes (int):   Number of gesture classes — 4.

    Returns:
        model (keras.Model): Compiled model ready for training.

    TODO: Implement this function.
        Steps:
          1. Use keras.Sequential() to build the model.
          2. Add layers in the order shown in the architecture above.
          3. Compile with:
               optimizer = 'adam'
               loss      = 'sparse_categorical_crossentropy'
               metrics   = ['accuracy']
          4. Return the compiled model.

    Hint: The first layer must include input_shape=input_shape.
          Conv1D and MaxPooling1D are in tensorflow.keras.layers.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def train(model, X_train, y_train, X_val, y_val,
          epochs=EPOCHS, batch_size=BATCH_SIZE):
    """
    Trains the model and returns the training history.

    Args:
        model       (keras.Model):  Compiled model from build_model().
        X_train     (np.ndarray):   Training features, shape (N, 100, 6).
        y_train     (np.ndarray):   Training labels,   shape (N,).
        X_val       (np.ndarray):   Validation features.
        y_val       (np.ndarray):   Validation labels.
        epochs      (int):          Number of training epochs.
        batch_size  (int):          Recordings per weight update.

    Returns:
        history (keras.callbacks.History): Training history object.
            Access accuracy with history.history['accuracy']
            Access loss with      history.history['loss']

    TODO: Implement this function.
        Steps:
          1. Call model.fit() with:
               x              = X_train
               y              = y_train
               validation_data= (X_val, y_val)
               epochs         = epochs
               batch_size     = batch_size
          2. Return the History object that model.fit() returns.
    """
    # TODO — your implementation here
    pass


# ─────────────────────────────────────────────────────────────
def plot_history(history, save_path="training_curves.png"):
    """
    Plots training and validation accuracy and loss curves side by side.
    Saves the figure to disk and displays it.

    This function is fully implemented — no changes needed.

    Args:
        history   (keras.callbacks.History): Returned by model.fit().
        save_path (str): File path for the saved figure.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Accuracy
    ax1.plot(history.history["accuracy"],     label="Train",      linewidth=1.5)
    ax1.plot(history.history["val_accuracy"], label="Validation", linewidth=1.5, linestyle="--")
    ax1.set_title("Accuracy")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Loss
    ax2.plot(history.history["loss"],     label="Train",      linewidth=1.5)
    ax2.plot(history.history["val_loss"], label="Validation", linewidth=1.5, linestyle="--")
    ax2.set_title("Loss")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.suptitle("Training Results — Gesture Wand 1D CNN", fontsize=13)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"Training curves saved to {save_path}")
    plt.show()


# ─────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Gesture Wand — Model Training")
    print("=" * 50)

    # ── Load and prepare data
    print("\n[1/4] Loading recordings...")
    X, y = load_recordings()

    print("\n[2/4] Splitting dataset...")
    X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(X, y)

    print("\n[3/4] Normalizing sensor channels...")
    X_train, X_val, X_test, mean, std = normalize(X_train, X_val, X_test)

    # Save normalization params — required for inference
    np.save("mean.npy", mean)
    np.save("std.npy",  std)
    print("  Normalization params saved → mean.npy, std.npy")

    # ── Build and train
    print("\n[4/4] Building and training model...")
    model = build_model()
    if model is None:
        print("Error: build_model() returned None. Complete the TODO first.")
        return

    model.summary()
    history = train(model, X_train, y_train, X_val, y_val)

    if history is None:
        print("Error: train() returned None. Complete the TODO first.")
        return

    # ── Plot results
    plot_history(history)

    # ── Save model
    model.save("gesture_model.h5")
    print("\nModel saved → gesture_model.h5")
    print("\nDone. Run evaluate_model.py to test on held-out recordings.")


if __name__ == "__main__":
    main()
