---
title: Setting up an ODROID-HC4 as a NAS
layout: post
IncludeSyntaxStyles: yes
---

I bought a new NAS, a [Hardkernel
ODROID-HC4](https://www.hardkernel.com/shop/odroid-hc4-oled/)! It's a real
upgrade. Before: 6C/12T Xeon processor; After: 4C/4T ARM processor. Before: 12GB
ECC RAM, After: 4GB RAM. Before: 6 HDD slots/SATA ports; After: 2. But most
importantly:

<div style="display: flex; flex-wrap: wrap; justify-content: center;">
    <span>Before:
    <img alt="power consumption before: 185W" width=300px src="/images/odroidhc4/power-before.jpg">
    </span>
    <span>After:
    <img alt="power consumption after: 111W" width=300px src="/images/odroidhc4/power-after.jpg">
    </span>
</div>

I keep the Kill-A-Watt measuring the whole homelab, so those numbers are for the
while rack. However, without any NAS at all the total sits just over 100W.
That is, I cut my power consumption by something like forty percent by replacing
one of my four machines---and not even the fastest, by a good margin!

With electricity prices just below [the national average of
$0.13/kWh](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a),
I generally figure 1W=$1/year. So if I cut my power consumption by a bit more
than 70W, this should pay for itself in just over a year.

Note that this is steady-state power; I suspect numbers would go up under heavy
access. However, my NAS spends 90+% of its time idle, so I'm most concerned
about its performance there. I _did_ see nearly 40W on startup, with both disks
spinning up plus higher CPU usage, so that seems like a good upper bound. Even
if it was at this state all the time, I'd still be using less than half of my
previous power consumption.

### Purchase process
There are several North American resellers of Hardkernel products, but their
markup is big enough that I opted to buy directly from
Hardkernel[^pricing-breakdown]. I did have some issues the first time through
the purchase process (the largest of which was that when I was filling out my
info in the purchase form, many of the labels weren't in English...until some
reloads later, when they suddenly were!), but ended up making it through. The
shipping was surprisingly fast for crossing an ocean; from clicking "ORDER" to
opening the box took just under seven days.

[^pricing-breakdown]: I paid $79 for the device, $9.40 for the power supply, and
    $25.13 for shipping, totaling $113.53. AmeriDroid, who was the
    on-the-same-continent-with-a-website-entirely-in-a-language-I-can-read
    option, would have charged $79.95 for the base (no OLED) model, $12.95 for
    the power supply, and $15.29 for shipping, for a total of $108.19. I did
    want the display/RTC, and the prices were close, so I chose to buy straight
    from Hardkernel.

### Hardware impressions
Wow. Super slick. This thing is pretty great! The case is sturdy, and seems to
support the drives well. The "toaster" form factor is kind of cute, and
definitely serves its job well. I suspect it may not protect the drives as well
as fully enclosed models, but on the upside it _does_ do a nice job keeping good
airflow for cooling.

Speaking of cooling, there's a built in fan that I never once saw spin. I did a
bit of compiling, and the temperature indicator budged from 50°C where it
usually sat to nearly 60°C, but it never did actually break 60°. Perhaps if I
stressed the CPU and GPU (not sure why, with a headless device) _and_ put a good
load on the disks so the power supply and PCIe controller are working, I might
be able to get the fans to kick in, but under normal use it's cool as a
cucumber.

The CPU is reasonably speedy, and 4GB of memory isn't anything to scoff at. I
did some development of the [OLED display driver software](#oled-display) on the
device itself, and though I eventually moved to cross compiling, this was more
for toolchain reasons than for speed. The hardware is certainly more than
sufficient for serving files over the network, as long as I'm not doing
particularly heavy-duty encryption or compression.

Single-core performance for encryption was the one issue I did run into;
`scp`ing files within my network did bottleneck on my single-core speeds,
limiting me to about 60MB/s instead of the full 100-110MB/s that's typical with
a gigabit network. Of course, Comcast's anemic upload speeds ensure I'll never
have to worry too much about that!

### OLED Display
I opted to pay the extra $10 for the integrated OLED display. In hindsight,
totally worth it! (It also adds a battery backed realtime clock, so that adds
extra value too, but the display is easily worth it on its own.) While I was
running some initial backups (in case I had problems switching over to the new
NAS) I took the time to try to figure out how I wanted to use the display.

[The wiki page for the ODROID-HC4's OLED display](https://wiki.odroid.com/odroid-hc4/application_note/oled)
links to some sample software, written in Python, that can be used for running
the display. However, it's fairly dependency heavy, and requires maintaining
a Python installation. This seems like a fairly good candidate for a
zero-dependency statically-compiled drop-in binary, so I set about writing a
small app in Go to do what I wanted.

![the OLED display with system stats showing](/images/odroidhc4/display.jpg)

The [result is on GitHub](https://github.com/ChandlerSwift/odroidhc4-display);
I'm pretty happy with it!

### Setting up software
I have in the past used FreeNAS (now TrueNAS CORE), but I was hoping to migrate
away in favor of something I could manage more directly. Even if I had wanted to
stay with FreeNAS, though, my hand would have been relatively forced since this
board doesn't have good support for FreeBSD. Linux support for ZFS is supposedly
quite good at this point, and since [Jeff](https://blackolivepineapple.pizza)
set up his NAS in about 15 minutes on Void Linux, I figured I could make it
work.

Hardkernel offers official images, but they seem to be stuck on Linux 4.9 (an
LTS release from 2016) with no plans to move to more recent images. Also, while
they do provide the kernel source code, I wasn't able to find packaging info or
build scripts for the images they produce. I prefer more transparency than that
in the build process, so I went searching for something else.

Ideally, I'd have tried for a Debian install, but Debian's ARM support seems
patchy. My next attempt was Arch Linux ARM, but they don't support the HC4.
After some searching, it turns out Armbian seems to be the best supported distro
for the HC4, so that's what I chose.

After running through Armbian's setup process, here's the config I had to change
to get the NAS set up the way I wanted:

```sh
sudo hostname nas

# Set up SSH
mkdir .ssh
curl https://github.com/chandlerswift.keys | head -n1 > .ssh/authorized_keys
sudo vim /etc/ssh/sshd_config # set PasswordAuthentication=no, PermitRootLogin=no
sudo service sshd restart # Apply new config

# Update packages
sudo apt update
sudo apt upgrade

# Set up ZFS
sudo armbian-config # Software > Headers_Install
sudo apt install zfs-dkms zfsutils-linux
sudo reboot # Could possibly `modprobe` instead?
```

### Importing data
Now we're ready for some disks! I had two 8TB disks set up in Freenas as a
mirrored pool. Some historical baggage remained -- the pool was still called
Duluth from two moves ago[^long-time]. Plug the disks in, and let's re-import
the pool as `nas`:
```sh
# Still some remnants of prior living locations here!
sudo zpool import Duluth nas
```

[^long-time]: 
    ```
root@nas:~# zfs get creation nas
NAME  PROPERTY  VALUE                  SOURCE
nas   creation  Fri Aug  9  8:59 2019  -
    ```

### Future steps
This isn't terribly useful as a NAS yet. I can mount filesystems from Linux with
SSHFS quite easily and with decent performance (assuming I remember to turn
compression off, as single-core compression limits my throughput); but for MacOS
or Windows clients I'm out of luck. With this in mind, I intend to get NFS or
SMB (or both!) shares set up. This will also let me easily mount shares to VMs
when I want to offload data from the VM hosts, and keep them backed up.

I also intend to set up an automated backup solution. I've had fairly good luck
with pointing [Duplicity](http://duplicity.nongnu.org/) at B2. I've also heard
good things about [Borg Backup](https://www.borgbackup.org/), but I don't
believe that it directly supports targeting B2, and I don't have a remote server
to stash backups on.

Finally, I'm still not thrilled with Armbian; it's done reasonably well, but I
do prefer to trust the most important piece of server hardware in my house to a
big-name distribution like Debian. I'm considering trying to get support for
the ODROID-HC4 merged into Debian and/or Arch Linux ARM so I have a distribution
I'm more directly familiar with to use. Also, after getting settled in with
Armbian, I did see that Alpine is supposed to have decent `aarch64` support, so
that may be worth exploring as well.
