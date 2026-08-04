// ============================================================
// mpu6050.h — MPU6050 Driver Interface
// Short Circuit — Gesture Wand Project
//
// Declares the SensorData struct and the public driver functions.
// Students implement the function bodies in mpu6050.cpp.
// ============================================================

#ifndef MPU6050_H
#define MPU6050_H

#include <Arduino.h>
#include <Wire.h>
#include "config.h"

// ── Data Structure ────────────────────────────────────────────
// Holds one complete set of six-axis sensor readings.
// All values are converted to physical units.
struct SensorData {
    float ax;   // accelerometer X  (g)
    float ay;   // accelerometer Y  (g)
    float az;   // accelerometer Z  (g)
    float gx;   // gyroscope X      (°/s)
    float gy;   // gyroscope Y      (°/s)
    float gz;   // gyroscope Z      (°/s)
};

// ── Function Prototypes ───────────────────────────────────────

/**
 * initMPU()
 *
 * Initialises the I2C bus and verifies that the MPU6050 responds
 * at MPU_ADDRESS. Wakes the sensor from sleep mode by writing to
 * the power management register.
 *
 * Returns: true if initialisation succeeded, false otherwise.
 * On failure: prints a descriptive error to Serial and returns false.
 * The caller should halt (while(1)) if this returns false.
 */
bool initMPU();

/**
 * readMPU()
 *
 * Reads all 14 data bytes from the MPU6050 in one I2C transaction
 * starting at register 0x3B. Combines each high-byte/low-byte pair
 * into a signed 16-bit integer, then converts to physical units
 * using the sensitivity constants from config.h.
 *
 * Returns: a SensorData struct populated with the latest readings.
 */
SensorData readMPU();

#endif // MPU6050_H
