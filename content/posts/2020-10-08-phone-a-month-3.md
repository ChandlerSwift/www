---
layout: post
title: "A phone a month for a year: September: Custom LineageOS 16.0/MicroG"
---

Here's another post about the open-source phone exploration I started
[in July]({{< ref 2020-07-29-phone-a-month >}}). Last month, I ran an
[unofficial LineageOS/microG build](https://forum.xda-developers.com/g7-power/development/unofficial-lineageos4microg-16-0-t4057273)
(containing no Google apps) to pretty good results. 

<!--more-->

> The fun thing about being with you is that when I call and you don't answer,
> there are _so many_ reasons it could be.
>
> --Käthe, yesterday, after my PinePhone looked like it might not receive calls

Not too many interesting points this month, which, in my opinion, is a good
thing. Overall, it's an OS I'm quite happy with, and one that strikes a good
balance of reliability and privacy.

### Apps

LineageOS takes its apps pretty much straight from AOSP, with a few tweaks that
I generally appreciate. It's a nice default set of apps---browser, email,
camera, file manager, dialer; all functional enough that I don't feel compelled
to immediately add more. I did make the following shifts:
 * Play Store &rarr; F-Droid and Aurora Store (for apps like Spotify that I
   can't get from F-Droid)
 * Google's sync &rarr; [DAVx<sup>5</sup>](https://www.davx5.com/), with which I can sync
   my calendar and contacts.
 * Google Keep &rarr; [OpenTasks](https://opentasks.app/)
 * YouTube &rarr; [NewPipe](https://newpipe.schabi.org/)

I haven't found a Maps app I particularly like, but Google Maps works fine with
microG, so that's my one remaining Google app. I'd also like an Android Auto
app, but support for that is required and
[not currently implemented in microG](https://github.com/microg/android_packages_apps_GmsCore/issues/897),
so that'll have to wait for the time being.

Beyond the Lineage apps and Google replacements, I have a handful of apps that
cover the rest of what I want to use my device for:
 * AsteroidOS Sync ([F-Droid](https://f-droid.org/en/packages/org.asteroidos.sync/))
 * Bitwarden, via [a custom F-Droid repo](https://mobileapp.bitwarden.com/fdroid/)
 * Menards (Play Store, works without Google libraries)
 * Spotify (Play Store, works without Google libraries)
 * Pancheros (Play Store, sort of works without Google libraries)
 * RevolutionIRC ([F-Droid](https://f-droid.org/en/packages/io.mrarm.irc/))

### Miscellany

I was pleasantly surprised that the Moto Actions I had set up persisted after I
reset my phone, so I still have my chop-chop for a flashlight. Presumably the
Moto Actions app writes something to the gesture detection chip that survives
an internal storage wipe?

I've only run into one noticeable bug: Display colors are sometimes wonky after
turning the phone on. I've found that this can be fixed by changing the
LiveDisplay mode in Settings, or toggling sRGB in Developer Options...perhaps
this resets something in the graphics chip that isn't set properly on boot?
It seems like it doesn't really matter what setting I change nor what I change
it to; any combination works, as long as it's not the combination the phone was
booted with. Here's what I see, compared to what the phone thinks I should be
seeing:

<div style="display: flex; flex-wrap: wrap; justify-content: center;">
    <img alt="A photo of the Dialer app with incorrect colors" width="360" src="/images/phone/dialer-bad.jpg">
    <img alt="The same screen, with correct coloring" width="360" src="/images/phone/dialer-good.jpg">
</div>

<div style="display: flex; flex-wrap: wrap; justify-content: center;">
    <img alt="A photo of the home screen, with incorrect colors" width="360" src="/images/phone/home-bad.jpg">
    <img alt="The same screen, with correct coloring" width="360" src="/images/phone/home-good.jpg">
</div>

LineageOS quietly added
[official LOS 17.1 builds for `ocean`](https://download.lineageos.org/ocean)
early in the month, so perhaps that's in the future!
[MicroG has them too](https://download.lineage.microg.org/ocean/)!

### Next Month

```
[chandler@xenon ~]$ ssh chandlers-pinephone
Welcome to postmarketOS!

This distribution is based on Alpine Linux.
Read both our wikis to find a large amount of how-to guides and
general information about administrating and development.
See <https://wiki.postmarketos.org> and <https://wiki.alpinelinux.org>.

You may change this message by editing /etc/motd.

chandlers-pinephone:~$
```
