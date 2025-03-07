#include <Wire.h>

void setup() {
    Serial.begin(115200);
    Wire.begin(21, 22);  // SDA = GPIO 21, SCL = GPIO 22
    Serial.println("I2C Scanner - Searching for devices...");
}

void loop() {
    byte error, address;
    int nDevices = 0;
    
    Serial.println("Scanning...");

    for (address = 1; address < 127; address++) {
        Wire.beginTransmission(address);
        error = Wire.endTransmission();

        if (error == 0) {
            Serial.print("I2C device found at address 0x");
            Serial.println(address, HEX);
            nDevices++;
        }
    }

    if (nDevices == 0) {
        Serial.println("No I2C devices found.");
    } else {
        Serial.println("Scan complete.");
    }

    delay(5000);
}
