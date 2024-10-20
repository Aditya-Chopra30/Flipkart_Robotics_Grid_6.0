#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

// Define the GPIO pin where the DHT22 data pin is connected
#define DHTPIN 15 

// Define the type of sensor
#define DHTTYPE DHT22   

// Create an instance of the DHT sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // Start serial communication
  Serial.begin(115200);
  // Initialize the DHT sensor
  dht.begin();
  Serial.println("DHT22 sensor initialized");
}

void loop() {
  // Wait a few seconds between measurements
  delay(2000);

  // Read temperature as Celsius
  float temperature = dht.readTemperature();
  // Read humidity
  float humidity = dht.readHumidity();

  // Check if any reads failed
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print the results in the desired format
  Serial.print("Temperature: ");
  Serial.print(temperature, 2); // Print temperature with 2 decimal places
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity, 2);    // Print humidity with 2 decimal places
  Serial.println(" %");
}
