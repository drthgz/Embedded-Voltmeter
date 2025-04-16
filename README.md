# Embedded-Voltmeter

## Overview
In this project, I started by transferring the provided circuit diagram onto a breadboard within a simulation environment, ensuring all connections are precise and controlled. Followed it by developing MicroPython code capable of reading analogue inputs from various sources, converting these readings to digital format, and displaying the calculated values on a four-digit seven-segment display.

The measurement process will be initiated by a button press. I handled this input by using an edge-triggered interrupt, incorporating proper button debouncing techniques to ensure accurate readings.

A button press initiates the process of reading analog inputs, converting them to digital, and updating the display. Concurrently, a timer-based logic periodically refreshes the seven-segment display, ensuring it shows the latest calculated value continuously. This ensures the values are kept up to date and shown without flicker.

## Components
Here is a list of the circuit components needed to complete this project in Wokwi:
- Breadboard
- Half Breadboard
- Raspberry Pi Pico
- 7 Segment
- Pushbutton
- Slide potentiometer
- Photoresistor sensor
- NTC temperature sensor
- VCC
- GND ​

## Completed Implementation
![image](https://github.com/user-attachments/assets/6310e2db-d79d-4b06-8328-5ae3c7655b29)
