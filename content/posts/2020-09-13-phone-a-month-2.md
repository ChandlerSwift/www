---
layout: post
title: "A phone a month for a year: August: Several false starts"
---

I'm continuing my open-source phone exploration I started
[last month]({{< ref 2020-07-29-phone-a-month >}}). This month's updates are
both a bit late and a bit light, with quite a few false starts and dead ends.

<!--more-->

I got my PinePhone last month, but after a day or two of tinkering wasn't able
to place calls on it, so I stuck with Android on the G7 Power. I'm definitely
not writing this one off for long, as development is rapid and claims are that
there's good support for T-Mobile, so I may give this another shot this month.
(While I didn't get calls working, WiFi _did_ work, and I was very impressed
with both the UBPorts distribution that came with it, as well as the copy of
postmarketOS that I installed. I could easily see myself using either of these
full-time, if I can get the basic phone functionality up and running.)

In the mean time (as I had gotten myself a bit burnt out on the PinePhone), I
started tinkering with my old Samsung Galaxy S4. I bought it just as the S5 was
coming out, and it's served me will since then (2014-ish). It spent its purchase
through mid-2017 as my primary phone, and I'd guess at least a couple months a
year since, as I've installed a wide variety of third-party ROMs on it[^roms]. 

[^roms]: As far as I recall, I started with CyanogenMod, as the de facto
    newbie ROM. Following that, xda-developers was my friend, and I tried some
    variants of CyanogenMod (later LineageOS) as I wanted new features (maybe
    the Xposed framework was a driving factor?).
    [OctOS](https://github.com/Team-OctOS/) is the only other one I remember,
    and that only because it had a stunning default boot animation and some
    really impressive customization options.

An easy task to get it working now, one would think? Alas, not so fast! What I
didn't immediately realize is that the S4 was made in the dark ages of carrier
specific phones, before all carriers just sold the same phone that covered all
the bands. And that wasn't even immediately obvious: LineageOS doesn't handle
activation very gracefully, so my usual routine is (1) use TWRP to backup the
ROM, (2) flash back to stock, (3) run Sprint's crappy activation utility, and
(4) restore from my backup. I've gotten it down to a 30-40 minute process, but
then again I've had quite a bit of practice! But here's when I realize: It'll
activate on T-Mobile[^technically-yes], but the best I could do was HSPA+,
somewhere in the 3G range of speeds, and even that only intermittently. Clearly
I was missing a few crucial bands. 

[^technically-yes]: I had expected this to be a fairly straightforward SIM card
    swap...it was not. xdadevelopers has a good thread on [how to SIM Unlock the
    Sprint Galaxy S4](https://forum.xda-developers.com/galaxy-s4-sprint/general/info-sprint-galaxy-s4-sim-unlock-sph-t3144530),
    which seems to require a certain version of a rom, and was a bit finicky. 
    From my notes:
    > Needed to do a factory reset (and possibly the stock recovery
    > automatically set something right for me) after flashing the stock
    > tar.md5. Let the phone boot, _then_ installed TWRP and rebooted.

With some research, it turns out that Sprint's S4 has support for these
bands[^sprint-bands]:

> LTE: Band 25, 26, 41
>
> CDMA 1x/EVDO Rev.A: 800/1900MHz
>
> HSPA+/UMTS: 850/900/1900/2100MHz
>
> GSM: 850/900/1800/1900MHz

[^sprint-bands]: Sprint bands are listed at
    [https://web.archive.org/web/20160323082401/https://www.samsung.com/us/mobile/cell-phones/SPH-L720ZWASPR-specs/](https://web.archive.org/web/20160323082401/https://www.samsung.com/us/mobile/cell-phones/SPH-L720ZWASPR-specs/)[^internet-archive]

while the T-Mobile S4 has support for these[^t-mo-bands]:

> LTE: Bands 1/2/4/5/7/17
>
> HSPA+/UMTS: 850/AWS/1900/2100MHz
>
> GSM: 850/900/1800/1900MHz

[^t-mo-bands]: T-Mobile bands are listed at
    [https://web.archive.org/web/20140827092551/http://www.samsung.com/us/mobile/cell-phones/SGH-M919ZKATMB-specs](https://web.archive.org/web/20140827092551/http://www.samsung.com/us/mobile/cell-phones/SGH-M919ZKATMB-specs)[^internet-archive]

[^internet-archive]: The Internet Archive's Wayback Machine to the rescue again!
    I've started maintaining a list of everything I wouldn't've been able to
    find without it, and when every time I hit 20 things I'm planning to donate
    $20 to the Internet Archive. Hopefully this doesn't become too expensive!

[T-Mobile's page on the topic](https://www.t-mobile.com/support/coverage/t-mobile-network#frequencies)
says that LTE requires 2, 4, 5, and 66; and that their "Extended Range 4G LTE"
requires bands 12 and 71. That seems to check out with my experience. So...let's
check the used market! Swappa has T-Mobile S4's for $30-40, depending on
condition and accessories[^for-the-low-low-price-of]. I bought one. It's in
pretty good shape, with just a bit of burn-in on the screen (something I've 
not seen before), and a mediocre---but not terrible---battery life. 

[^for-the-low-low-price-of]: The phone I ended up buying was $35 shipped. Why
    people pay hundreds of dollars for new phones when perfectly functional
    phones like this are so readily available eludes me.

Unfortunately, the combination of missing Extended LTE bands in addition to lack
of WiFi calling means that signal in my house is pretty lousy. I made it two
days and two missed calls before I switched back, once again, to the G7 Power.
It seems that with some hacking, WiFi calling can be made to work, but it's not
enabled by default[^how-to-check].

Back on the Motorola phone, then, all is good(ish), until I made the mistake of
clicking the "Update me to Android 10" button. Turns out some of the earlier
messing around I'd done left one of the A/B partitions _hella_ broken. Or
something like that. I, of course, ran the update at 10pm the night before I was
supposed to be out bicycling the next morning, so I spent a few hours'
frantically trying quite a few different things before I got a
[custom build of LineageOS](https://forum.xda-developers.com/g7-power/development/unofficial-lineageos4microg-16-0-t4057273)
running, with which I finished off the month. 

Maaaan, technology is hard.

[![relevant-xkcd, "TV problems"](https://imgs.xkcd.com/comics/tv_problems.png "Certified skydiving instructors know way more about safely falling from planes than I do, and are way more likely to die that way.")](https://xkcd.com/1760/)

[^how-to-check]: To find this, dial `*#*#4636#*#*` from your dialer app, and
    click Phone Information. It'll give you a toggle for WiFi calling (and one
    for VoLTE, and one for Video Calling, and some others). If that's enabled
    you're fine, but if it's disabled, it's not supported by your device and/or
    its software.
    ([more hidden codes](https://www.xda-developers.com/codes-hidden-android/)
    on xda-developers)
