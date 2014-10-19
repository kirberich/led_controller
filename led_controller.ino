#include "FastLED.h"

#define NUM_LEDS 300
#define DATA_PIN 11

CRGB leds[NUM_LEDS];
unsigned int last_update = 0;

void setup(){
  Serial.begin(115200);
  FastLED.addLeds<NEOPIXEL, DATA_PIN, RGB>(leds, NUM_LEDS);
}

void loop(){
  process_serial();
}

void process_serial() {
  if (Serial.available()) {
    // 'c' starts a command, in the form of 'c00 00 00'
    byte input = Serial.read();
    if (input == 'c') {
      int lamp_index = Serial.parseInt();
      byte red = Serial.parseInt();
      byte green = Serial.parseInt();
      byte blue = Serial.parseInt();
      leds[lamp_index] = CRGB(red, green, blue);
    } else if (input == 's') {
      FastLED.show();
      Serial.println("updating");
    }
  }
}
