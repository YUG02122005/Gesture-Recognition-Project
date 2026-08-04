// ============================================================
// config.h — Gesture Wand Project
// Short Circuit
//
// All project constants are defined here.
// Change values in this file only — never hard-code numbers
// in mpu6050.cpp or imu_reader.ino.
// ============================================================

#ifndef CONFIG_H
#define CONFIG_H

// ── I2C ──────────────────────────────────────────────────────
#define MPU_ADDRESS     0x68    // AD0 low (default)
#define SDA_PIN         21
#define SCL_PIN         22

// ── Sampling ─────────────────────────────────────────────────
#define SAMPLE_RATE_HZ  50                        // samples per second
#define PERIOD_MS       (1000 / SAMPLE_RATE_HZ)   // 20 ms between samples
#define RECORD_SAMPLES  100                        // samples per recording (2 s)

// ── Sensitivity (MPU6050 default ranges) ─────────────────────
#define ACCEL_SENSITIVITY   16384.0f   // LSB/g  for ±2g range
#define GYRO_SENSITIVITY    131.0f     // LSB/°/s for ±250°/s range

// ── Serial ───────────────────────────────────────────────────
#define BAUD_RATE       115200
#define RECORD_CMD      'r'            // Python sends this to start a recording
#define END_SIGNAL      "END"          // firmware sends this after 100 samples

#endif // CONFIG_H
