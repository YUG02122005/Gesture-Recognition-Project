// ============================================================
// mpu6050.cpp — MPU6050 Driver Implementation
// Short Circuit — Gesture Wand Project
//
// TODO: Implement the two functions below.
// Read mpu6050.h for the expected inputs, outputs, and behaviour
// of each function before writing any code.
// ============================================================

#include "mpu6050.h"

// ── Register Addresses ────────────────────────────────────────
// These are defined in the MPU6050 Register Map document.
// Reference them here rather than hard-coding numbers in functions.
#define REG_PWR_MGMT_1  0x6B   // write 0x00 to wake the sensor
#define REG_DATA_START  0x3B   // first of 14 consecutive data bytes

// ─────────────────────────────────────────────────────────────
// TODO: Implement initMPU()
//
// Steps (in order):
//   1. Call Wire.begin(SDA_PIN, SCL_PIN) to initialise the I2C bus.
//   2. Start a transmission to MPU_ADDRESS and call endTransmission().
//      Check the return value — if it is not 0, print an error and
//      return false. The device did not acknowledge its address.
//   3. Write 0x00 to REG_PWR_MGMT_1 to clear the sleep bit.
//      Use beginTransmission → write(register) → write(value) → endTransmission(true).
//   4. Print a success message and return true.
//
// Hint: Wire.endTransmission() returns 0 on success.
// ─────────────────────────────────────────────────────────────
bool initMPU() {

    // TODO — your implementation here

    return false; // replace with true after successful init
}

// ─────────────────────────────────────────────────────────────
// TODO: Implement readMPU()
//
// Steps (in order):
//   1. Point the MPU6050's internal register pointer to REG_DATA_START:
//        Wire.beginTransmission(MPU_ADDRESS);
//        Wire.write(REG_DATA_START);
//        Wire.endTransmission(false);   // false = repeated start
//   2. Request 14 bytes: Wire.requestFrom(MPU_ADDRESS, 14, true);
//   3. Read and combine bytes in order:
//        int16_t raw = (int16_t)(Wire.read() << 8 | Wire.read());
//      Repeat for ax, ay, az, then skip 2 temperature bytes, then gx, gy, gz.
//   4. Convert raw integers to physical units using ACCEL_SENSITIVITY
//      and GYRO_SENSITIVITY from config.h.
//   5. Populate and return a SensorData struct.
//
// Hint: You must read all 14 bytes even if you discard temperature.
//       Failing to read them leaves stale bytes in the Wire buffer.
// ─────────────────────────────────────────────────────────────
SensorData readMPU() {
    SensorData data = {0, 0, 0, 0, 0, 0};

    // TODO — your implementation here

    return data;
}
