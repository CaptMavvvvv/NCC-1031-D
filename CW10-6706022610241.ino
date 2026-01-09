#include <ESP8266WiFi.h>
#include "ThingSpeak.h"
#include "DHT.h"

#define DHTPIN D1
#define DHTTYPE DHT22 

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "NCC-1701-E";
const char* password = "bank031132";

unsigned long myChannelNumber = 3223488;
const char* myWriteAPIKey = "OCB1NJQXFU4PCYTP";

WiFiClient client;

unsigned long lastTime = 0;
unsigned long timerDelay = 15000; // ส่งข้อมูลทุก 15 วินาที

float temperatureC;
float humidity;

void setup() {
  Serial.begin(115200);
  delay(1000);

  dht.begin();

  WiFi.mode(WIFI_STA);
  ThingSpeak.begin(client);

  Serial.println("DHT + ESP8266 + ThingSpeak");
}

void loop() {
  if ((millis() - lastTime) > timerDelay) {

    if (WiFi.status() != WL_CONNECTED) {
      Serial.print("Connecting to WiFi");
      while (WiFi.status() != WL_CONNECTED) {
        WiFi.begin(ssid, password);
        delay(5000);
        Serial.print(".");
      }
      Serial.println("\nWiFi connected");
    }

    humidity = dht.readHumidity();
    temperatureC = dht.readTemperature();

    if (isnan(humidity) || isnan(temperatureC)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    Serial.print("Temperature (°C): ");
    Serial.println(temperatureC);
    Serial.print("Humidity (%): ");
    Serial.println(humidity);

    ThingSpeak.setField(1, temperatureC); 
    ThingSpeak.setField(2, humidity); 

    int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);

    if (x == 200) {
      Serial.println("Channel update successful.");
    } else {
      Serial.println("Problem updating channel. HTTP error code " + String(x));
    }

    lastTime = millis();
  }
}