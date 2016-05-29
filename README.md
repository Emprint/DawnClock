# DawnClock
Raspberry Pi powered Alarm Clock

Freely inspired by [Matt Dyson's AlarmPi](http://mattdyson.org/projects/alarmpi/)

HifiBerry Amp+ - [Official Site](https://www.hifiberry.com/ampplus/)<br>
GPIO Usage - [Official Guide](https://www.hifiberry.com/guides/gpio-usage-of-the-hifiberry-products/)<br>
GPIO 2 (I2C) and 3 for configuration but can be used by other I2C devices<br>
GPIO 18 to 21 for sound (I2S)

Digital RGB strand (25 leds with WS2801 chip from [Adalight project](https://www.adafruit.com/products/322))<br>
SPI GPIO 10 & 11

Adafruit Servo/PWM Pi Hat on I2C - [Shop](https://www.adafruit.com/product/2327)

Rotary Encoder + Switch - [Shop](https://www.adafruit.com/products/377)<br>
GPIO 14, 15, 23 (Change to 17, 27, 22 to prevent collision with TXD, TXD)

2 Solid State Relay<br>
GPIO 12 & 16

16x02 LCD Display with I2C backpack (Used Adafruit backpack before but installed it in [another project](https://github.com/Emprint/GreenhouseBot) so this one is using a cheaper pack (6$ with postage) that works very well as well but require [another library](https://gist.github.com/DenisFromHR/cc863375a6e19dce359d)

Note to myself, use [Bob Rathbone](http://www.bobrathbone.com/raspberrypi/Raspberry%20Rotary%20Encoders.pdf) class instead of Pi Gaugette for rotary encoder, as the last one is giving non consistent results and I suppose Bob's one with events will work better
