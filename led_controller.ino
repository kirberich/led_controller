#include "FastLED.h"

#define NUM_LEDS 300
#define DATA_PIN 11

CRGB leds[NUM_LEDS];
unsigned int last_update = 0;
int lamp_index = 0;
int current_color_index = 0; // 0=red, 1=green, 2=blue
byte red = 0;
byte green = 0;
byte blue = 0;
void setup(){
  Serial.begin(115200);
  FastLED.addLeds<NEOPIXEL, DATA_PIN, RGB>(leds, NUM_LEDS);
}

void loop(){
  process_serial();
}

void process_serial() {
  while (Serial.available()) {
    // 1 starts a command, 2 updates the screen, everything else is interpreted as r/g/b values
    byte input = Serial.read();
    if (input == 1) {
      lamp_index = current_color_index = red = green = blue = 0;
    } else if (input == 2) {
      FastLED.show();
      Serial.println("updating");
    } else { 
      switch (current_color_index) {
        case 0:
          red = input;
          current_color_index = 1;
          break;
        case 1:
          green = input;
          current_color_index = 2;
          break;
        case 2:
          blue = input;
          leds[lamp_index] = CRGB(red, green, blue);
          lamp_index++;
          current_color_index = 0;
          break;
      }
    }
  }
}
