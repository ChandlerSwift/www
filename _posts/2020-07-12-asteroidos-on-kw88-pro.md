---
layout: post
title: Installing AsteroidOS on the Kingwear KW88 Pro
include_syntax_styles: true
---

I recently bought a Kingwear KW88 Pro,
and I'm not much a fan of the OS that came with it. In the interest of doing
something different, I decided to install
[AsteroidOS](https://asteroidos.org/). While this is a reasonably
straightforward process, there are a few issues that I ran into that stumped me
for a while, that I thought were worth writing down.

[![AsteroidOS running on the KW88 Pro](/images/installing-asteroidos/asteroidos-sm.jpg)](/images/installing-asteroidos/asteroidos.jpg)

### SP Flash Tool
Devices based around the MTK6580 chipset don't seem to have support for
fastboot, so they use a MediaTek software product called SP Flash Tool. If
you've used Odin for flashing Samsung devices, you may find a similar feel here.
It's open source, but doesn't really _feel_ like an open source tool---source
code for different versions is scattered across different repositories, without
a direct link from the website, and it seems that they're used more as a way of
hosting releases than of offering public development access. It _does_ have a
Linux build, but it expects a fair number of libraries to be in very specific
places, which was the cause of most of my pain, and with the source being
difficult to access and compile, I wasn't able to rebase it on newer versions
of the libraries I needed.

In the end, on Debian Buster, I had success downloading the latest version
(v5.1916) from the [SP Flash Tool website](https://spflashtool.com/download/),
and a copy of the required
[`libpng1.2` library from Sourceforge](https://sourceforge.net/projects/libpng/files/libpng12/1.2.59/libpng-1.2.59.tar.gz/download).
`libpng1.2` is older than what's available in the Debian archives, which is why
I ended up installing it manually. The real struggle was what to do with it---I
didn't particularly want an out-of-date version of `libpng` permanently
installed on my system. An `strace` later, and it seems that among other places,
`flash_tool` checks the directory it lives in for dependencies, so copying
`libpng12.so.0` to the same directory as `flash_tool` got me up and running.
(_Why_ it needs a PNG library, I can't say!) The AsteroidOS site says to run it
as root, but I didn't find this necessary given that my user was a member of the
`dialout` group. Other Linux distros may handle this differently, however.

Toward the end of this process, I realized that there's an [AUR package for SP
Flash Tool](https://aur.archlinux.org/packages/spflashtool-bin/), which likely
would have alleviated most or all of this hassle. Ah well, lessons learned!

### Flashing AsteroidOS
AsteroidOS provides flashing instructions at
[https://asteroidos.org/install/harmony/](https://asteroidos.org/install/harmony/).
However, they don't quite work out of the box[^heres-what-happened-instead]. The
instructions do note[^caveat-in-instructions]:

 > However, please note that only the Kingwear KW88 has been rigorously tested.
 > Other watches have been reported to have various bugs, for instance the
 > Zeblaze Thor has non working touchscreen. The Lemfo LES1 and Zeblaze Thor 3G
 > have a screen rotated by 45° or **the KW88 Pro requires a different scatter
 > file**.

I wasn't able to find such a scatter file, so I wound up creating my own, which
ended up being quite an easy process. As far as I can tell, it's only the
partition alignment that was causing problems, so I updated the partition sizes
and positions to be the same as the ones in the scatter file from the stock ROM:
```diff
177c177
<   file_name: logo-harmony.bin
---
>   file_name: logo.bin
302c302
<   partition_size: 0x3b800000
---
>   partition_size: 0x60000000
315,316c315,316
<   linear_start_addr: 0x46000000
<   physical_start_addr: 0x46000000
---
>   linear_start_addr: 0x6a800000
>   physical_start_addr: 0x6a800000
330,331c330,331
<   linear_start_addr: 0x56000000
<   physical_start_addr: 0x56000000
---
>   linear_start_addr: 0x7a800000
>   physical_start_addr: 0x7a800000
369d368
<
```

I did also have problems flashing after flashing the stock image v1.5. The
[Full Android Watch forum's thread on the KW88 Pro](https://discourse.fullandroidwatch.org/t/asteroidos-on-kw88-pro/38194/7)
has a post with the following:

 > I just try it, i have a bootloop…
 >
 > Edit:
 >
 > Works if i flash 1.3 original firmware (KW88Pro)

The same appeared to be true to me; after downgrading from v1.5 to v1.3, the
boot loop I was experiencing went away.

[^caveat-in-instructions]: The note about the KW88 Pro was introduced May 30,
    2020 in [17bdcc1](https://github.com/AsteroidOS/asteroidos.org/commit/17bdcc17a8f577368460411cc1c53f92280d185d),
    but I couldn't find an issue or anything that prompted this, and couldn't
    track down any such scatter file.

[^heres-what-happened-instead]: I attempted flashing the scatter file provided,
    which initially failed to run the "Download All", saying I also needed to
    also run a "Format All + Download" (All logs are from the stdout/stderr of
    flash_tool. Similar popup windows also appeared, but contain a subset of the
    text available in the console):
    ```
    USB port detected: /dev/ttyACM1
    BROM connected
    Downloading & Connecting to DA...
    connect DA end stage: 2, enable DRAM in 1st DA: 0
    COM port is open. Trying to sync with the target...
    DA Connected
    Disconnect!
    App Exception! (PMT changed for the ROM; it must be downloaded.
    Please select "Format All + Download" scene and try again)((fw_throw_error,../../../flashtool/Flow/ErrString.cpp,27))
    ```
    I selected "Format All + Download" instead. The process seemed to complete;
    all 3 partitions were formatted and downloaded, but at the end of the
    flashing, it gave a new error:
    ```
    USB port detected: /dev/ttyACM1
    BROM connected
    Downloading & Connecting to DA...
    connect DA end stage: 2, enable DRAM in 1st DA: 0
    COM port is open. Trying to sync with the target...
    DA Connected
    Format Succeeded.
    Format Succeeded.
    Format Succeeded.
    executing DADownloadAll...
    Download failed.
    Disconnect!
    BROM Exception! ( ERROR : S_SECURITY_SECURE_USB_DL_DA_RETURN_INVALID_TYPE (6104) , MSP ERROE CODE : 0x00. 


    [HINT]:
    )((exec,../../../flashtool/Cmd/DADownloadAll.cpp,84))
    ```
    and wouldn't boot. I had to "Format All + Download" back to stock, as
    described above, to get back to a working state.
    ![The same error, but now it's a picture!](/images/installing-asteroidos/popup.png)


### Flashing back to stock
I had a heck of a time tracking down stock firmware to flash this device back
to its factory state. I eventually found a copy on
[Full Android Watch](https://discourse.fullandroidwatch.org/t/kw88-pro-android-7/36810).
Before blindly flashing, it's worth noting that the person posting the links
provided the following caveat:

 > DO NOT FLASH THIS UNLESS YOU EXISTING FIRMWARE IS NHH TYPE!!
 >
 > Here is the latest version for NHH screens.

I didn't get a reading of the initial firmware version that came with my watch,
so I'm not sure what type my watch was, but it seemed to work with both of the
images posted on the linked forum.

### Flashing, more generally
I'm not sure if I have a flaky cable, a flaky device, or what, but the flashing
process sometimes intermittently failed for me. Simply trying again always
succeeded eventually, but sometimes it took a few tries.
