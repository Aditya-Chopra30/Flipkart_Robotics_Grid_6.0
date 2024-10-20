// Define the IR sensor pin
const int irSensorPin = 15; // GPIO 15 (can be any digital pin)

// Variables to keep track of object detection
int objectCount = 0;
bool objectDetected = false;

void setup() {
  // Start the serial communication
  Serial.begin(115200);
  
  // Set the IR sensor pin as input
  pinMode(irSensorPin, INPUT);
  
  // Initialize a message
  Serial.println("IR Sensor Object Counter with ESP32");
}

void loop() {
  // Read the value from the IR sensor
  int sensorValue = digitalRead(irSensorPin);

  // Check if the IR sensor detects an obstacle
  if (sensorValue == LOW) {
    // If an object is detected and it wasn't detected in the previous loop
    if (!objectDetected) {
      objectCount++; // Increment the counter
      objectDetected = true; // Update the state
      Serial.print("Object detected! Count: ");
      Serial.println(objectCount);
    }
  } else {
    // If no obstacle is detected, reset the detection state
    objectDetected = false;
  }

  // Wait a bit before reading the sensor again
  delay(100);
}
