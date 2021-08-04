---
layout: post
title: Enabling Hotspot on a Rooted Sprint Galaxy S6
---

While the transition from my S4 to S6 has gone generally smoothly, I do miss
the lack of support for the Xposed framework; specifically, the ability to
create a wireless hotspot. However, there is a simple fix, with very little
technical knowledge required (taken with gratitude from
[a post buried on xda-developers](http://forum.xda-developers.com/note-4-sprint/general/native-hotspot-stock-rooted-t2941853)):

### Prerequisites


 * A rooted phone. Samsung's Galaxy S6 and Note 3/4 are known working, but it
   should work on most phones with recent versions of Android.
 * An app called
   [SQLite Editor](https://play.google.com/store/apps/details?id=com.speedsoftware.sqleditor).
   It’s available on the Play Store for $2.99 (at the time of writing), and I
   gladly paid it. If you insist on not paying, you can probably find it free
   online, but be careful what you install!

### Abbreviated Steps

 * Open SQLite Editor.
 * Select Files from the top menu.
 * Find `/data/data/com.android.providers.telephony/databases/telephony.db`
 * Select carriers.
 * Find `APN2LTE internet` and `APN2 EHRPD internet`, which should be the last
   two lines.
 * Change the type field from its default `default,mms` to `default,mms,dun` on
   both lines.
 * Reboot.
 * Enable your device’s native hotspot!

### Comments
Wow. Coming from the S4 (Latest CyanogenMod nightly), the S6’s built-in hotspot
is absolutely incredible. I came from having controls for AP name and Password,
to an array of controls that nearly puts my router to shame. Beyond the usual,
the new native hotspot (Android 5.0):

 * Lists connected devices
 * Allows for MAC Address filtering (Whitelist)
 * Allows configuration of the channel (frequency _and_ band)
 * Allows control of IP addressing: Subnet, etc.
 * Allows fairly fine-tuned control over DHCP settings: IP range, etc.

Also, if the phone cannot connect to the internet, it (as far as I can tell) 
assumes that tethering is disabled for your account, which causes a potentially
misleading notice to appear.

### Full walkthrough
Select the files tab:
![step 1](/images/enabling-s6-hotspot/step-1.png)

Select `data`:
![step 2](/images/enabling-s6-hotspot/step-2.png)

Select `data` again:
![step 3](/images/enabling-s6-hotspot/step-3.png)

Select `com.android.providers.telephony`:
![step 4](/images/enabling-s6-hotspot/step-4.png)

Select `databases`:
![step 5](/images/enabling-s6-hotspot/step-5.png)

Select `telephony.db`:
![step 6](/images/enabling-s6-hotspot/step-6.png)

Select the table `carriers`:
![step 7](/images/enabling-s6-hotspot/step-7.png)

Find the lines starting with `APN2`:
![step 8](/images/enabling-s6-hotspot/step-8.png)

Change `default,mms` to `default,mms,dun` as shown:
![step 9](/images/enabling-s6-hotspot/step-9.png)
