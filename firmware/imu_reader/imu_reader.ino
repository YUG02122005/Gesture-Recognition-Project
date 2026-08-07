// ============================================================
// imu_reader.ino — Gesture Wand Main Firmware
// Short Circuit — Gesture Wand Project
//
// Handles two modes:
//   STREAM mode   — continuous CSV output (Module 1)
//   RECORD mode   — triggered 100-sample recording (Module 2)
//
// The mode is selected by uncommenting one #define below.
// ============================================================

#include <Wire.h>
#include "config.h"
#include "mpu6050.h"

// ── Mode Selection ────────────────────────────────────────────
// Uncomment ONE of the following to select the active mode.
// Comment out the other.

// #define MODE_STREAM     // Module 1: continuous CSV output
#define MODE_RECORD        // Module 2: triggered recording

// ── Timing ───────────────────────────────────────────────────
unsigned long lastSample = 0;

// ─────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(BAUD_RATE);
    Serial.println("Gesture Wand — Short Circuit");

    if (!initMPU()) {
        Serial.println("FATAL: MPU6050 init failed. Check wiring.");
        while (1);   // halt — do not proceed with uninitialised hardware
    }

#ifdef MODE_STREAM
    Serial.println("timestamp,ax,ay,az,gx,gy,gz");
#endif

#ifdef MODE_RECORD
    Serial.println("Ready. Send 'r' to start a recording.");
#endif
}

// ─────────────────────────────────────────────────────────────
void loop() {

#ifdef MODE_STREAM
    // ── Continuous stream at SAMPLE_RATE_HZ ──────────────────
    unsigned long now = millis();
    if (now - lastSample >= PERIOD_MS) {
        lastSample = now;
        SensorData d = readMPU();
        Serial.print(now);        Serial.print(",");
        Serial.print(d.ax, 4);    Serial.print(",");
        Serial.print(d.ay, 4);    Serial.print(",");
        Serial.print(d.az, 4);    Serial.print(",");
        Serial.print(d.gx, 4);    Serial.print(",");
        Serial.print(d.gy, 4);    Serial.print(",");
        Serial.println(d.gz, 4);
    }
#endif

#ifdef MODE_RECORD
    // ── Wait for 'r' command, then record RECORD_SAMPLES ─────
    // TODO: Implement the recording mode.
    //
    // Expected behaviour:
    //   1. Check if a byte is available on Serial (Serial.available() > 0).
    //   2. Read the byte with Serial.read().
    //   3. If the byte equals RECORD_CMD ('r'):
    //        a. Print the CSV header: "timestamp,ax,ay,az,gx,gy,gz"
    //        b. Collect exactly RECORD_SAMPLES samples at SAMPLE_RATE_HZ
    //           using the same millis() non-blocking timing from MODE_STREAM.
    //        c. Print each sample as a CSV row.
    //        d. After all samples are printed, send: Serial.println(END_SIGNAL)
    //   4. Return to waiting for the next 'r' command.
    //
    // Hint: Use a local counter variable to count collected samples.
    //       Use a local unsigned long for the per-recording timing baseline.

    // TODO — your implementation here

#endif
}
