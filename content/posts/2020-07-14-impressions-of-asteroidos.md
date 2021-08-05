---
layout: post
title: Impressions of AsteroidOS
IncludeSyntaxStyles: true
---

A solid two days in,
[AsteroidOS on the KingWear KW88]({% post_url 2020-07-12-asteroidos-on-kw88-pro %})
is...absolutely awesome. The watch is plenty functional as a watch, hasn't died
in 48 hours (though currently the battery is `undefined`% so I'm not sure how
long that'll last!) and it scratches every bit of my tinkerer's itch. It's
absolutely thrilling that I can `ssh` in and get a root shell, and that I can
customize or rewrite anything I want to change!

<!--more-->

As an introduction into Qt, in which most of the display and apps are written, I
figured I'd try my hand at modifying a watchface. AsteroidOS has
[good documentation](https://asteroidos.org/wiki/watchfaces-creation/) on the
subject, and together with the fact that I only wanted one slight modification
and that Qt uses Javascript for the imperative bits of the layout, it wound up
being a very quick in-and-out modification and deploy. And now I've achieved one
of my lifelong goals: owning a watch that displays the unix time!

<img alt="A screen recording of my watch, displaying normal time as well as unix time"
     src="/images/unix-time.gif"
     style="width:200px;" />

Here's what I had to do add the unix timestamp under the rest of the clockface:
```
122a123,139
>     Canvas {
>         id: unixTimeCanvas
>         anchors.fill: parent
>         antialiasing: true
>         smooth: true
>         renderStrategy: Canvas.Threaded
> 
>         property var sec: 0
> 
>         onPaint: {
>             var ctx = getContext("2d")
>             prepareContext(ctx)
>             ctx.font = "25 " + height/13 + "px Raleway"
>             ctx.fillText(Math.round(wallClock.time.getTime() / 1000), width*0.5, height*0.7);
>         }
>     }
> 
129a147
>             var sec = wallClock.time.getTime() / 1000
146a168,171
>             if (unixTimeCanvas.sec != sec) {
>                 unixTimeCanvas.sec = sec
>                 unixTimeCanvas.requestPaint()
>             }
166a192,193
>         unixTimeCanvas.sec = sec
>         unixTimeCanvas.requestPaint()
```

To deploy to the watch, run:

```sh 
# copy the file
scp 100-unix-time.qml root@192.168.2.15:/usr/share/asteroid-launcher/watchfaces/
# optionally, restart the session to reload the watchface (only needed if
# modifying an existing watchface)
ssh -t root@192.168.2.15 "systemctl restart user@1000"
```

Here's full source for the new file:

```qml
/*
 * Copyright (C) 2018 - Timo Könnecke <el-t-mo@arcor.de>
 *               2017 - Florent Revest <revestflo@gmail.com>
 * All rights reserved.
 *
 * You may use this file under the terms of BSD license as follows:
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the author nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

import QtQuick 2.1

Item {
    function twoDigits(x) {
        if (x<10) return "0"+x;
        else      return x;
    }

    function prepareContext(ctx) {
        ctx.reset()
        ctx.fillStyle = "white"
        ctx.textAlign = "center"
        ctx.textBaseline = 'middle';
        ctx.shadowColor = "black"
        ctx.shadowOffsetX = 0
        ctx.shadowOffsetY = 0
        ctx.shadowBlur = parent.height*0.0125
    }

    Canvas {
        id: hourCanvas
        anchors.fill: parent
        antialiasing: true
        smooth: true
        renderStrategy: Canvas.Threaded

        property var hour: 0

        onPaint: {
            var ctx = getContext("2d")
            prepareContext(ctx)

            ctx.font = "57 " + height*0.36 + "px Roboto"
            ctx.fillText(twoDigits(hour), width*0.378, height*0.537);
        }
    }

    Canvas {
        id: minuteCanvas
        anchors.fill: parent
        antialiasing: true
        smooth: true
        renderStrategy: Canvas.Threaded

        property var minute: 0

        onPaint: {
            var ctx = getContext("2d")
            prepareContext(ctx)

            ctx.font = "30 " + height * 0.18 + "px Roboto"
            ctx.fillText(twoDigits(minute), width*0.717, height*0.473);
        }
    }

    Canvas {
        id: amPmCanvas
        anchors.fill: parent
        antialiasing: true
        smooth: true
        renderStrategy: Canvas.Threaded
        visible: use12H.value

        property var am: false

        onPaint: {
            var ctx = getContext("2d")
            prepareContext(ctx)
            var ctx = getContext("2d")

            ctx.font = "25 " + height/15 + "px Raleway"
            ctx.fillText(wallClock.time.toLocaleString(Qt.locale("en_EN"), "AP"), width*0.894, height*0.371);
        }
    }

    Canvas {
        id: dateCanvas
        anchors.fill: parent
        antialiasing: true
        smooth: true
        renderStrategy: Canvas.Threaded

        property var date: 0

        onPaint: {
            var ctx = getContext("2d")
            prepareContext(ctx)
            ctx.font = "25 " + height/13 + "px Raleway"
            ctx.fillText(wallClock.time.toLocaleString(Qt.locale(), "d MMM"), width*0.719, height*0.595);
        }
    }

    Canvas {
        id: unixTimeCanvas
        anchors.fill: parent
        antialiasing: true
        smooth: true
        renderStrategy: Canvas.Threaded

        property var sec: 0

        onPaint: {
            var ctx = getContext("2d")
            prepareContext(ctx)
            ctx.font = "25 " + height/13 + "px Raleway"
            ctx.fillText(Math.round(wallClock.time.getTime() / 1000), width*0.5, height*0.7);
        }
    }

    Connections {
        target: wallClock
        onTimeChanged: {
            var hour = wallClock.time.getHours()
            var minute = wallClock.time.getMinutes()
            var date = wallClock.time.getDate()
            var am = hour < 12
            var sec = wallClock.time.getTime() / 1000
            if(use12H.value) {
                hour = hour % 12
                if (hour == 0) hour = 12;
            }
            if(hourCanvas.hour != hour) {
                hourCanvas.hour = hour
                hourCanvas.requestPaint()
            }
            if (minuteCanvas.minute != minute) {
                minuteCanvas.minute = minute
                minuteCanvas.requestPaint()
            }
            if (dateCanvas.date != date) {
                dateCanvas.date = date
                dateCanvas.requestPaint()
            }
            if (amPmCanvas.am != am) {
                amPmCanvas.am = am
                amPmCanvas.requestPaint()
            }
            if (unixTimeCanvas.sec != sec) {
                unixTimeCanvas.sec = sec
                unixTimeCanvas.requestPaint()
            }
        }
    }

    Component.onCompleted: {
        var hour = wallClock.time.getHours()
        var minute = wallClock.time.getMinutes()
        var date = wallClock.time.getDate()
        var am = hour < 12
        if(use12H.value) {
            hour = hour % 12
            if (hour == 0) hour = 12
        }
        hourCanvas.hour = hour
        hourCanvas.requestPaint()
        minuteCanvas.minute = minute
        minuteCanvas.requestPaint()
        dateCanvas.date = date
        dateCanvas.requestPaint()
        amPmCanvas.am = am
        amPmCanvas.requestPaint()
        unixTimeCanvas.sec = sec
        unixTimeCanvas.requestPaint()
    }
}
```
