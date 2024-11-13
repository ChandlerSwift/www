---
title: Notes on installing LineageOS on OnePlus 9 ("lemonade")
layout: post
IncludeSyntaxStyles: true
---

I just got a hand-me-down OnePlus 9, and installed LineageOS on it. There were
a few things that were non-obvious about the installation (which is a first;
normally the LineageOS docs are pretty comprehensive!), so I've documented those
here.

<!--more-->

I'm following the
[installation guide](https://wiki.lineageos.org/devices/lemonade/install/)
from the LineageOS Wiki, with a `LE2115` device.

{{< toc >}}

## `adb`/`fastboot` on NixOS

> **[Basic requirements](https://wiki.lineageos.org/devices/lemonade/install/#basic-requirements)**
>
> 2. Make sure your computer has adb and fastboot.

```shell
nix-shell -p android-tools
```

## Correct Firmware Version

> Warning: Before following these instructions please ensure that the device is
> currently using Android 13 firmware. If the vendor provided multiple updates
> for that version, e.g. security updates, make sure you are on the latest! If
> your current installation is newer or older than Android 13, please upgrade or
> downgrade to the required version before proceeding (guides can be found on
> the internet!).

(also the better part of
"[Checking the correct firmware](https://wiki.lineageos.org/devices/lemonade/install/#checking-the-correct-firmware)")

I was on OxygenOS 14, which was too new, and needed to downgrade to 13. I had
one more teeny little insignificant requirement for this bit: Don't run random
untrusted binaries off the internet! Thankfully, xda-developers had the hookup
as usual:

https://xdaforums.com/t/oneplus-9-rom-ota-oxygen-os-repo-of-oxygen-os-builds.4254579/ (5040MiB)

From the "Downgrade zips (will wipe your data)" section, I downloaded this file:

https://oxygenos.oneplus.net/8990_sign_LE2115_11_F_OTA_2310_all_uaFihW_10100001.zip (14MiB)

From the body of the first post:

> For OxygenOS 14, the
> [OTA-OnePlus-localUpdate-Oplus_key.apk](https://oxygenos.oneplus.net/OTA-OnePlus-localUpdate-Oplus_key.apk)
> APK […] must be used. It will become available as "Software Update" in the app
> drawer.

Push the image, set up the updater…

```shell
adb push 8990_sign_LE2115_11_F_OTA_2310_all_uaFihW_10100001.zip /sdcard/
adb install OTA-OnePlus-localUpdate-Oplus_key.apk
```

…et voila! There it is.

<img src="install-lineageos-on-lemonade/screenshot.png" alt='screenshot of "Software Update" app installing new update' style="max-height: 600px;">

Extracting the image takes about 15 minutes. Installing takes about 2 minutes.

Beware: The phone gets wiped during this install!

## Root

I'm using [`magisk`](https://github.com/topjohnwu/Magisk). Directions there are
pretty good. `boot.img` is the thing we used for installing LineageOS earlier.

```shell
adb push boot.img /sdcard/
```

and follow the directions! https://topjohnwu.github.io/Magisk/install.html
