---
title: Microcontroller-Selection
tags:
- tag1
- tag2
---

| ESP Info                                      |  Answer                                                                                                      |
| --------------------------------------------- |  --------------------------------------------------------------------------------------------------------- |
| Model                                          | ESP32-S3         |
| Product Page URL                                    | Found on Espressif.com [link](https://www.espressif.com/en/products/socs/esp32-s3)                                                                                    |
| ESP32-S3-WROOM-1-N4 Datasheet URL                   | [link](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)                                              |
| ESP32 S3 Datasheet URL                              | [link](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)                                                                              |
| ESP32 S3 Technical Reference Manual URL             | [link](https://documentation.espressif.com/esp32-s3_technical_reference_manual_en.pdf )                                                        |
| Vendor link                                         | Digikey, Jameco, etc. [link](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-S3-WROOM-1-N4/16162639)                       |
| Code Examples                                       | [RC car and controller](https://github.com/RawFish69/ESP32-RC-Car), [Quadcopter](https://github.com/ElektroJonas/DIY-Quadcopter)  |
| External Resources URL(s)                           | [ESP Sub](https://www.instructables.com/ESP-DIVE-Build-an-ESP32-RC-Submarine-With-FPV-Came/) [RC transmiter](youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3ZiZHhTamQ5V0FjaDVlZFlNM1NXRUhZclpnd3xBQ3Jtc0trQmU0azdCa25lUjY2eEJqOHdiLXFTUlBYR3hCTHBHVncycXdTWU5JaFFCQzNDSjRYMEZvOFdPaWxhSm42b1ZtcDJIeTN5Tm9LaXE0VEtCblpQNm1qU01XbmFrR1NaYjhjY0VJUmZuR0I1dWwyX0kwVQ&q=https%3A%2F%2Fgithub.com%2FAecert-Robotics%2FArduino-RC-Transmitter&v=g1elHIzqwE4)                    |
| Unit cost                                           | $5.06                                                               |
| Absolute Maximum Current for entire IC              | 0.5A                                                                 |
| Supply Voltage Range                                 | 3V / 3.3V / 3.6V                                                |
| Absolute Maximum current <br> (for entire IC)       | 500 mA                                                                                     |
| Maximum GPIO current <br> (per pin)                 | 20 mA                                                                                     |
| Supports External Interrupts?                       | Yes                                                                                     |
| Required Programming Hardware, Cost, URL            | [link](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/index.html)                                                                                  |

| Module         | # Available | Needed | Associated Pins (or * for any) |
| -------------- | ----------- | ------ | ------------------------------ |
| UART           | 3(UART0-2)           | 1      |     GPIO 17-18                         |
| external SPI | 4(SPI0-3)           | 0      |                              |
| I2C            | 2           | 1      | GPIO 21-22                              |
| GPIO           | 45          | 10      | GPIO 1,2,4,5,6,13,14,15                              |
| ADC            | 2 Units, 20 Channels           | 0      | 0                              |
| LED PWM        | 8           | 2      | GPIO 12-13                             |
| USB Programmer | 1           | 1      | GPIO 19-20                            |




The ESP32-S3 is ideal for my subsystem due to its compact design but powerful internals. Having onboard Wifi/bluetooth is critical for my system to work as intended, which the ESP32-S3 has built in to the chip. In addition to that it has plenty of IO pins to make a funtional controller. I2C is utalized for a OLED display, while its other DC/AC pins can be used for Joystick, D-pads, and buttons. While the final configuration is still being decided, if I end up utalizing a D-pad like system then I would not need any analog pins. I will utalize the PWM pins for the two LEDs to enable futher ways to express status of the subsystem. 