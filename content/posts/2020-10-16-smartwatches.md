---
title: Smartwatches
layout: post
tags: asteroidos
---

I've owned two smartwatches, across 3 OS's. They're all terrible. Here's why.

<!--more-->

### Samsung Galaxy Watch Active

In June 2019 I bought a Samsung Galaxy Watch Active. It's a very slick device,
and checked off the few checkboxes I had specifically selected it for:
 * Decent battery life: Unlike many ~~Android Wear~~ WearOS devices, I typically
   get two, sometimes three days of battery life with low-moderate use.
 * Offline Spotify playback: This was purchased specifically as a device to take
   running when I didn't want a phone, that I could listen to music through.
   Spotify playback when offline, however, is pretty buggy, especially with
   newer updates. Spotify on WearOS doesn't have this capability. As far as I
   know, offline playback on WearOS is limited to Google Play Music, which has,
   I believe, been deprecated in favor of some YouTube offering.
 * Compact: At the time of purchase, I think this may have been the smallest
   non-Apple full smartwatch[^full-smartwatch] on the market. I don't want to
   strap a huge device to my wrist; I'm trying to get away from my huge devices!

[^full-smartwatch]: For this comparison, I'm not counting Fitbit watches and
    other similar watches, since they won't do music playback, although they do
    excel at the time-telling and fitness-tracking portions of my use case.
    Basically, "can I write and install an app" is probably the defining
    question for this.

With all the features, though, I've found that I want my watch to do three
things, and this does none of them exceptionally well:

 1. I want it to be able to play music. Local music is flawless, but Spotify
    stutters and often outright crashes when disconnected from the phone.
    Recently, it started indicating that songs are saved offline, but then
    saying "Song not available" when I try to play it. Connecting to Bluetooth
    earbuds is not difficult, but doesn't always work the first time either.
 2. Fitness tracking. This may be its best point; it's pretty decent. However,
    it requires Samsung's "Samsung Health" app, and doesn't offer good
    integration with other platforms. If you're on a Samsung phone, it's
    convenient; if not, it's a bit more of a hassle. (Supposedly Strava support
    is also okay, but I haven't tested this.)
 3. I just want to know the dang time! Ironically, this device is quite poor at
    that, compared to the ~~dumb~~ supremely cool
    [Timex Expedition digital watches](https://web.archive.org/web/20160808024828/https://www.target.com/p/timex-expedition-digital-watch-with-fast-wrap-nylon-strap-blue-gray-t49660jt/-/A-12278865)
    that lasted me _years_ as a kid[^lifespan]. The battery life is pretty
    bad if I use the always-on display, but the raise-to-wake feature doesn't
    always work, especially if I'm laying down. And "I'm sorry, I don't know
    what time it is because I forgot to charge my watch"...just seems a bit
    silly!

[^lifespan]: As I recall, with only occasional backlight use, I tended to get
    between two and three years of battery life out of each iteration of this or
    a similar watch. At the end, the battery would die, I'd replace it, but once
    the waterproof seal on the back cover was broken, it would last maybe three
    to six months before failing in a light rainstorm. This sequence repeated
    three or four times between third grade and high school.

A fourth, less tangible point is the ability to _do what I want_ with it.
It's running Samsung's locked down OS; I can't easily develop or install Android
apps for it since it's running some Tizen-based OS, and of course I don't have
root access on it. Samsung is reputable enough that they're _probably_ not
shipping off all my biometrics to China, but that's not a sure bet either.

One thing that it _does_ do well is notifications. My phone is now nearly
always on silent mode, and important notifications (select texts and calls,
mostly) buzz my watch. Bluetooth range is good throughout the house if I leave
my phone on my centrally located desk, so it's not uncommon for me to go a full
day or two without knowing where my phone is. And if I _do_ lose my phone,
the find-my-phone feature is nice as well---no more "lost my phone, can you call
it please?"!


### KingWear KW88 Pro

I've been peripherally aware of the
[AsteroidOS Project](https://asteroidos.org/) for a few years now, but hadn't
ever taken the plunge to try it out. I purchased a
[KingWear KW88 Pro](https://www.gearbest.com/smart-watch-phone/pp_009129768431.html)
from GearBest in November of 2019, when it was on sale for $79.99---reasonable
enough, I figure, that even if it never works for me, it's not a $200+
experiment like many other watches. Also, it had some unique features that drew
my attention:

 * A speaker that, on testing, is as loud as most smartphones.
 * 1GB RAM, 16GB ROM, when many WearOS smartwatches come with 512M/4GB.
 * Camera! It's a bit gimmicky and not particularly high quality, but it's
   a camera.
 * It does have a heart rate monitor, which many low-end watches seem to lack.
 * While I don't plan to use this, there's a 3G modem and SIM slot, so I could
   use it for placing calls and texts without a phone.
 * Decent display: full circle (no flat tire); quite bright, decent size,
   400x400px.

I wouldn't even consider using the version of Android that came with this watch,
however. I don't have words to express how bad it is. As far as I can tell, they
took the full smartphone Android and made as many tweaks as was necessary to get
it to compile on the watch (and no more), and shipped it. The menus are mostly
English, but the text that isn't included in stock Android looks like it hasn't
been proofread by a native English-speaking proofreader[^proofread]---lots of
phrases like "Please waiting for update..." or "No notification" rather than 
"No notifications". It's running an ancient version of Android, last patched in
2017, and with a 3.18.x Linux kernel. The apps' support for hardware is good
(camera, accelerometer, etc. all work), with the exception of the display: apps
made for a square display haven't been modified, so important buttons are
offscreen.

[^proofread]: Though, credit where it's due, I can nearly always tell what
    they're trying to say, and their localization (like MM-DD-YYYY for USA, and
    options for imperial units in addition to metric) is pretty good.

Check out this quick screen capture for an idea of what I mean. Nothing is
unusable, or even _that_ remarkable by itself, but after using it for a while
it's definitely a death-by-a-thousand-cuts UI disaster. The black overlay around
the outside shows where the screen ends. Play Store and Maps seem to be the
worst offenders, with both displaying important controls and information outside
of the visible area. Other apps are (mostly) better, but suffer from their own
localization, discoverability, and functionality issues. (The Contacts app, for
example, seemed prone to random crashes.)

<!--
for posterity:
x264 doesn't work in new Chrome apparently (but does in Edge?). Turns out now
AV1 is supported everywhere but Firefox on Android, and I'll take that hit
(even though I use Firefox on Android!). Plus compression is quite a bit better.
I didn't really notice a significant difference (except in fast moving subtle
shading changes) between even the best and the worst, so I ended up going with
the smallest:
-rw-r--r-- 1 chandler chandler 732K Oct 16 14:00 ui-demo-AV1-q30.webm
-rw-r--r-- 1 chandler chandler 701K Oct 16 14:00 ui-demo-AV1-q31.webm
-rw-r--r-- 1 chandler chandler 674K Oct 16 13:59 ui-demo-AV1-q32.webm
-rw-r--r-- 1 chandler chandler 642K Oct 16 13:59 ui-demo-AV1-q33.webm
-rw-r--r-- 1 chandler chandler 619K Oct 16 13:59 ui-demo-AV1-q34.webm
-rw-r--r-- 1 chandler chandler 593K Oct 16 13:59 ui-demo-AV1-q35.webm
-rw-r--r-- 1 chandler chandler 572K Oct 16 13:59 ui-demo-AV1-q36.webm
-rw-r--r-- 1 chandler chandler 549K Oct 16 14:18 ui-demo-AV1-q37.webm
-rw-r--r-- 1 chandler chandler 529K Oct 16 13:59 ui-demo-AV1-q38.webm
-rw-r--r-- 1 chandler chandler 508K Oct 16 13:59 ui-demo-AV1-q39.webm
-rw-r--r-- 1 chandler chandler 490K Oct 16 14:18 ui-demo-AV1-q40.webm
-rw-r--r-- 1 chandler chandler 472K Oct 16 14:18 ui-demo-AV1-q41.webm
-rw-r--r-- 1 chandler chandler 454K Oct 16 14:18 ui-demo-AV1-q42.webm
-rw-r--r-- 1 chandler chandler 436K Oct 16 14:18 ui-demo-AV1-q43.webm
-rw-r--r-- 1 chandler chandler 421K Oct 16 14:17 ui-demo-AV1-q44.webm
-rw-r--r-- 1 chandler chandler 405K Oct 16 14:38 ui-demo-AV1-q45.webm
-rw-r--r-- 1 chandler chandler 389K Oct 16 14:37 ui-demo-AV1-q46.webm
-rw-r--r-- 1 chandler chandler 378K Oct 16 14:37 ui-demo-AV1-q47.webm
-rw-r--r-- 1 chandler chandler 367K Oct 16 14:37 ui-demo-AV1-q48.webm
-rw-r--r-- 1 chandler chandler 355K Oct 16 14:37 ui-demo-AV1-q49.webm
-rw-r--r-- 1 chandler chandler 344K Oct 16 14:37 ui-demo-AV1-q50.webm
-rw-r--r-- 1 chandler chandler 333K Oct 16 14:37 ui-demo-AV1-q51.webm
-rw-r--r-- 1 chandler chandler 323K Oct 16 14:37 ui-demo-AV1-q52.webm
-rw-r--r-- 1 chandler chandler 313K Oct 16 14:37 ui-demo-AV1-q53.webm
-rw-r--r-- 1 chandler chandler 303K Oct 16 14:37 ui-demo-AV1-q54.webm
-rw-r--r-- 1 chandler chandler 294K Oct 16 14:37 ui-demo-AV1-q55.webm
-rw-r--r-- 1 chandler chandler 282K Oct 16 14:37 ui-demo-AV1-q56.webm
-rw-r--r-- 1 chandler chandler 274K Oct 16 14:37 ui-demo-AV1-q57.webm
-rw-r--r-- 1 chandler chandler 263K Oct 16 14:37 ui-demo-AV1-q58.webm
-rw-r--r-- 1 chandler chandler 252K Oct 16 14:37 ui-demo-AV1-q59.webm
-rw-r--r-- 1 chandler chandler 241K Oct 16 14:36 ui-demo-AV1-q60.webm

Single:
ffmpeg -i test2.mp4 -i frame.png -filter_complex "overlay=0:0" -ss 0.1 -t 60 -c:v libaom-av1 -crf 60 -b:v 0 ui-demo.mkv

Batch mode for quality testing:
for i in {30..60}; do
  ffmpeg -i test2.mp4 \
         -i frame.png -filter_complex "overlay=0:0" \
         -ss 0.1 -t 60 -async 1 \
         -c:v libaom-av1 -crf $i -b:v 0 \
         ui-demo-AV1-q$i.mkv \
         -nostdin -hide_banner -nostats -loglevel panic &
done
-->
<video controls height="300" style="display: block; margin: auto; padding: 20px;">
    <source src="/images/smartwatches/ui-demo.webm" type="video/webm">
</video>

<div style="display: flex; flex-wrap: wrap; justify-content: center;">
    <img alt="About the watch (screen 1)" width="250" src="/images/smartwatches/settings-1.png">
    <img alt="About the watch (screen 2)" width="250" src="/images/smartwatches/settings-2.png">
</div>

There's an app that goes along with it. They don't provide a Play Store link,
just [a link to a download page](http://www.weitetech.cn/Custom/WIITE/C7/apk_download.htm).
The app won't start without location, camera/microphone, and file access
permissions, and suffers from similar UI issues as the watch, though at least
all of the important buttons are on screen. And then there's permissions: The
app won't even let you connect to the watch unless it can:
 * Take pictures and record video
 * Access this device's location
 * Access photos, media, and files on your device

It _does_ seemingly allow you to bypass call log, contacts, phone, display over
other apps, and notification permissions, but I had to put in some effort to
make that happen. 

Now, these all make some sense as to why they might be necessary. That said, for
an app specifically downloaded outside of the Play Store from a manufacturer
I've never heard of, I'm a bit hesitant to grant pretty much every major
permission on my device.

### KingWear KW88 Pro, AsteroidOS
[AsteroidOS is lovely]({{< ref 2020-07-14-impressions-of-asteroidos >}}). I
can `ssh` in to a root shell, and run lots of neat things[^neat-things] on it!
But it's nowhere near mature enough where I'd consider it ready for daily use,
particularly not on this watch. I'm attempting to
[contribute](/projects/asteroidos.html) to get it to a more stable and
feature-complete state, but the going is slow. 

[^neat-things]: So far, `vim` and a lightweight web server, a standard POSIX
    environment, [Quake 1](https://github.com/MagneFire/lp-public), a Minecraft
    server (only kinda-sorta-working), and probably others I'm not recalling. No
    [k8s cluster](https://twitter.com/jkrippy/status/932800484703862784) yet!

I'm still missing, at a minimum:
 * Some kind of fitness tracking---I like to know time, pace, and distance when
   I'm running. Heart rate, GPS tracks, cadence, step count are all nice, but
   not strictly necessary. I also really like having music support over
   Bluetooth headphones.
 * A stable Bluetooth connection---Right now I can connect things to the watch,
   but generally only for a few seconds at a time, and it'll disconnect, which
   I haven't fixed yet. This applies to both the BLE connection to my phone and
   full-fat Bluetooth connections to game controllers, headsets, and the like.
 * Wifi connection---I currently have to plug the watch into my computer to
   connect to a network. Wifi seems to be in worse shape than Bluetooth;
   scanning for networks works, but `wpa_supplicant` keeps `DEAUTH`ing itself.
 * Better battery life. It seems intermittent; sometimes I get nearly two days,
   and sometimes it doesn't last a day. May have something to do with whether
   Wifi and Bluetooth are active and scanning?

### Conclusions
In addition to the watches I've used, I've spent some time with plain old
digital watches (which I generally quite like), a Huawei Watch 1, which was
impressive in its day but lackluster compared to newer offerings, and a Ticwatch
S, which was good for its price point, and offered a nice Android Wear
experience. I have _not_ tried either a Fitbit or an Apple Watch, though I hear
encouraging things about both. I definitely see a lot of flaws in the smartwatch
ecosystem, but I also see a lot of progress! I'm genuinely excited to see what
watches will look like in a few years, as technology continues to improve.

For all the watches: Notifications on my wrist are really, _really_ nice. It
feels to me like I've finally moved from polling to interrupts, and anything
that can reduce the amount of time I spend looking at my phone is good in my
book!

Currently, AsteroidOS seems most strongly on track to provide the experience I
want, and unlike the other options, I can actually fix what I don't like about
AsteroidOS. Both proprietary options are okay, but have gripes that simply can't
be fixed, and I can't use the tools I'm used to to develop for or use them. (I
was stunned to find out that `rsync` Just Worked&trade; to copy my media over;
now all I have to do is write a music player!) Perhaps a sub-conclusion---it's
amazing how much more comfortable I feel working on these projects when I have
a familiar POSIX-ish environment everywhere!

Besides the practicalities, AsteroidOS provides some nice intangibles too. I
like the community, and I've felt welcome and appreciated as I've tried to step
up and contribute to the project. I like the design philosophy; Linux and
Wayland and DBus and BlueZ and all the other things I use on my desktop work on
my watch too, just on a smaller scale. I may not be running Firefox and Sway...
but I could if I wanted to! (I _have_ contemplated a terminal, if I can get a
bluetooth keyboard working!)

With all this in mind, I'm sticking with AsteroidOS for the near future, and I'm
hoping to be able to deliver some progress for the ecosystem myself. Ah, the
joys of open source!

<div class="thanks">
    Thanks to Käthe for reviewing a draft of this post.
</div>
