const int irSensorPin = 5;
int sensorValue = 0;
int count = 0;


void setup() {
  pinMode(irSensorPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  sensorValue = digitalRead(irSensorPin);
  
  if (sensorValue == LOW) {
    count++;
    Serial.println("Object detected");
    delay(500);
  } 
  else {
    Serial.println("No object detected");
  }
  Serial.println(count);

  delay(500);
}
