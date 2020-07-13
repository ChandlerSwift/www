---
layout: project
title: Auto-timed Fish Tank Light
excerpt: In which I build a NTP-syncin' LED-blinkin' fish light timer.
date: 2018-11-30
---

My roommates and I have a fish.

[![Sidon is our fish.](/images/sidon-light/sidon-sm.jpg)](/images/sidon-light/sidon.jpg)

We've managed to keep him alive and more or less healthy for the past two
years, but one thing we're not super reliable about is turning on and off the
tank light, which (I'm told) is important for fish circadian rhythms or
something. (I'm not a biologist; ask the roommates!)

To solve this, I used an ESP8266 to automatically turn on the lights in the
morning and turn them off in the evening. Because the ESP doesn't have a
built-in RTC, I sync every ten minutes with the NIST NTP servers (which
likely makes this the most accurate timekeeping device in the house other
than cell phones!) and fade the lights off at 7am and off at 9pm.

Schematic, assembled on perf board:
![the schematic](/images/sidon-light/schematic.png)

I began prototyping with an ESP32, since I couldn't find my USB<->serial
adapter:
[![Tank and breadboard with ESP32](/images/sidon-light/prototyping-1-sm.jpg)](/images/sidon-light/prototyping-1.jpg)

Later, testing the ESP-01 with the newfound serial adapter:
[![Breadboard and more components](/images/sidon-light/prototyping-2-sm.jpg)](/images/sidon-light/prototyping-2.jpg)

Here's the final product, front:
[![The front of the fish tank board, assembled](/images/sidon-light/board-front-sm.jpg)](/images/sidon-light/board-front.jpg)

and back:
[![The back of the fish tank board, assembled](/images/sidon-light/board-back-sm.jpg)](/images/sidon-light/board-back.jpg)

I'm fairly proud of how neat it all turned out, especially in a few places like
the removable ESP8266 for programming, and the outgoing wire strain relief loop!

Because I needed 12V for the LEDs and 3.3V for the ESP8266, I used the
[AMP MATE-N-LOK 1-480424-0 power connector](https://en.wikipedia.org/wiki/Molex_connector#Disk_drive),
often used for PATA hard disks and commonly "the Molex connector", for which
I had a power supply sitting around:

[![The assembled board plus all the power cables](/images/sidon-light/board-with-context-sm.jpg)](/images/sidon-light/board-with-context.jpg)

[Source available on GitHub](https://github.com/ChandlerSwift/FishTankLight)
