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

<!-- Final product:
![]()
TODO: add photo -->
