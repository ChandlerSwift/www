---
layout: post
title: "A phone a month for a year: Intro; Moto G7/Stock Android"
excerpt_separator: <!--more-->
---

Right off the bat, I'll concede: I'm not buying 12 new pieces of phone
hardware for this. However, "Trying a new phone or a new OS on a phone I already
have every month for a year" seemed a bit wordy!

I &lt;3 open source, so I enjoy trying new software that increases my freedom.
I also have some philosophical issues with how Google treats its users,
particularly in ways it seems to abuse its dominant market share to force its
apps, ads, and limitations on users. This has led me to back away from
Google's vision of Android, and to try to find a compromise between privacy
and utility that best meets my needs.

<!--more-->

### Current hardware: Motorola G7 Power
Wow. Easily the nicest phone I've ever owned. I wasn't initially convinced, when
going from Samsung's at the time (generation-old) flagship S7 to a mid-range
phone from a non-Samsung manufacturer, that I'd love it. Not so! If they were
sold at the same price point, I think I'd struggle to choose between Samsung's
_current_ flagship and the G7 Power---it's just that good!

Major hardware features I've appreciated:
 * Battery life. Oh my god, the battery life. I charge somewhere between once
   and twice a week. I can't overstate how liberating it is to go from having
   to plug in a phone at 5pm because it was already dead for the day, to
   never plugging it in other than my daily commute where it's plugged in for
   Android Auto anyway. The battery life is the primary reason I'd recommend
   this phone to anyone who asks.
 * USB C is a bigger change than I had imagined: Not only do I never have to
   worry about plugging it in backwards (!!) but I also can carry one charger
   for all (well, some -- headphones and watch haven't caught up yet) of my
   devices.
 * The camera probably can't keep up with that of the S20 or the iPhone 11,
   but nonetheless it's a reasonable improvement over the camera in the
   Galaxy S7 (which was best-in-class at the time of its release).
 * It still has a headphone jack! Bluetooth headphones are lovely, but still
   mean one more device to keep charged, and you can't beat the convenience
   and sound of wired headphones.

A few drawbacks:
 * No Wireless Charging. A minor convenience, but one I had gotten used to.
 * LCD Screen rather than OLED: Mostly noticeable in dark environments, but
   I miss the contrast of Samsung's AMOLED displays---particularly for
   always-on-display-type functionality, where it was especially handy.
 * 3GB RAM/32GB Storage is a bit on the low end for modern phones, although
   I haven't run out of storage yet, and the 3GB of RAM feels at least as snappy
   as the 4GB I had on Samsung's Galaxy S7.
 * Lack of NFC (and, therefore, Google/Samsung Pay) -- Again, a convenience, but
   a welcome one. Currently I do wear a Samsung Galaxy Watch Active, which
   supports Samsung Pay, so I'm not totally out to dry here; I just need to have
   the companion app installed on my phone.


### July 2020: Stock Android 9
Up until now, I've just discussed the hardware, but what I'm really looking to
compare here is the _software_. To give me some context, I briefly installed a
few custom roms in the first weeks I had the phone, a process made easy by
Motorola's straightforward bootloader unlock service, so I'm not forming
opinions totally in a vacuum. I spent several weeks with Lineage+OpenGApps, and
several more weeks with a Google-free LineageOS install, plus previous
experience with Samsung's TouchWiz+Android 8 combo on a Galaxy S7 and LineaegeOS
16 on a Galaxy S4.

Overall, I'm impressed. Coming from TouchWiz, I really like the nearly-stock
Android that the phone ships with. The few additions that Motorola add are
subtle and helpful; the one that I'm most pleased being the "double chop" to
enable the flashlight, which makes getting a light on a situation a nearly
instant and no-visual-feedback-required task. It also has a remarkably low false
positive rate; I think I can count on one hand the number of times it's falsely
triggered.

Android Auto: On the S7 and previous phones, Android Auto was always a bit of a
clunky, laggy experience, prone to frequent random crashes. Not so here: it's a
buttery smooth, stable, seamless experience. Having recently purchased my first
vehicle with Android Auto support...wow. Is this what driving a Tesla is like?

Because it's Android with all the Google services, everything Just
Works&trade;---at least, anything I'd expect to work on any other Android.
The Play store, for all its philosophical issues, does make installing any
app I can imagine a breeze, and I can sideload apps too! Being non-rooted
means I don't run into issues with SafetyNet, which definitely saves some
additional hassle.

While it's hands-down the best Android experience I've had, it _is_ still
Android, which means there are a few typical downsides:

 * Walled garden of Google's Play store: As mentioned, I like Free and Open
   Source software, so I'd rather get my software from [F-Droid](f-droid.org).
   However, Google's Play Framework gives its app store an unfair advantage over
   other app stores, as it's the only store that doesn't require separate
   user dialogs to update/install applications[^f-droid-root].
 * Unremovable bloatware: It does come with some Google apps I don't
   want/need, some from T-Mobile as well. Thankfully, very little from
   Motorola.
 * and the big one: Constant, insidious, unremovable, hard-to-detect tracking
   by Google, Facebook (which has several unremovable apps on the `/system`
   partition), and possibly others?

[^f-droid-root]: F-droid _does_ have a
    [privileged extension](https://f-droid.org/en/packages/org.fdroid.fdroid.privileged.ota/)
    that allows it to function as you'd expect for an app store. This requires a
    custom recovery for installation, which I don't have with the stock ROM.


### Future plans

I am the proud owner of a [PinePhone](https://www.pine64.org/pinephone/), which
just arrived today! The phone is
[well reviewed](https://drewdevault.com/2019/12/18/PinePhone-review.html) by
quite a few people who share similar opinions to me about what the experience
of having a phone should be, so I'm excited to give it a spin myself.

I also have a Samsung Galaxy S4 from ages ago, which thanks to LineageOS runs
~~as well as~~ better than it did new. Also, with [MicroG](https://microg.org/),
I can be free from our Google-y overlords if I wish, while still retaining most
(though not all) of the functionality I'd like to have.

Also, this leaves me a lot more freedom to tinker without having to worry about
breaking anything---if I always make sure at least _one_ of the phones is
working, I can just swap SIM cards and always have something ready to go.

Over the next year, I'd like to try [postmarketOS](https://postmarketos.org/)
on both the S4 and the PinePhone, spend some more time with
[LineageOS+MicroG](https://lineage.microg.org/) as well. KDE Mobile? Mobian?
Much will depend on the state of software, and I'm very ready to see how it all
pans out.

Anyway, for August I'm going to try to use the UBPorts Ubuntu Touch that the
PinePhone ships with. I expect I'll find a few things missing;
currently, the largest of which seems to be MMS support. However, I'm awed by
the breakneck pace of development, and hope to be able to dive in and contribute
some patches myself!
