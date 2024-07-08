#include <Servo.h>

// Initializing the DC motor and servo motor
Servo myDC, myServo;

// Initializes the throttle as the center
int throttle = 1500;
int steer = 90;

// Initialize the max and the min of the throttle and steer
int throttle_max = 2000;
int throttle_min = 1000;
int steer_max = 180;
int steer_min = 0;

void setup() {
  Serial.begin(115200);

  // DC Motor in PIN 9
  myDC.attach(9);

  // Servo Motor in PIN 10
  myServo.attach(10);
}

void loop() {

  // Sends a message back to the Jetson to confirm that there is a connection
  Serial.println(String(throttle));

  // Checks if there are serial messages waiting
  if (Serial.available() > 0) {

    // Reads the serial string and finds where the comma is
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');

    // Checks if the comma is in the message
    if (commaIndex > 0) {

      // Gets the strings of the message before and after the comma to get the throttle and steer
      String str_throttle = data.substring(0, commaIndex);
      String str_steer = data.substring(commaIndex + 1);

      // Converts the strings of the throttle and steer to integers
      int throttle = str_throttle.toInt();
      int steer = str_steer.toInt();

      // Checks that the throttle is within the max and min before writing it to the motor
      if (throttle >= throttle_min && throttle <= throttle_max) {
        myDC.writeMicroseconds(throttle);
      }

      // Checks that the steering is within the max and min before writing it to the motor
      if (steer >= steer_min && steer <= steer_max) {
        myServo.write(steer);
      }
    }
  }

}
