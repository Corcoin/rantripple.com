//Software Environment
//Arduino IDE: For programming the drones.
//Python or Processing: For creating a control interface on the computer.

//Use RF modules like nRF24L01 for communication. One Arduino will act as the master, connected to the computer, while others will be slaves.

//Master Drone Code (Arduino)

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN
const byte address[6] = "00001";

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    radio.write(&command, sizeof(command));
  }
}

//Slave Drone Code

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>

RF24 radio(9, 10); // CE, CSN
const byte address[6] = "00001";

Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();

  // Initialize motors
  motor1.attach(3);
  motor2.attach(5);
  motor3.attach(6);
  motor4.attach(9);
}

void loop() {
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    Serial.println(text);

    // Parse and execute command
    String command = String(text);
    if (command.startsWith("THROTTLE")) {
      int throttle = command.substring(8).toInt();
      motor1.writeMicroseconds(throttle);
      motor2.writeMicroseconds(throttle);
      motor3.writeMicroseconds(throttle);
      motor4.writeMicroseconds(throttle);
    }
  }
}
//Computer Interface
//Create a simple interface to send commands to the master drone. This example uses Python with the (pyserial) library.

import serial
import time

# Replace 'COM3' with the appropriate port for your setup
ser = serial.Serial('COM3', 115200, timeout=1)

def send_command(command):
    ser.write((command + '\n').encode())

while True:
    command = input("Enter command (e.g., THROTTLE1000): ")
    send_command(command)
    time.sleep(0.1)
//Resources
//RF24 Library Documentation
//Python pyserial Documentation

