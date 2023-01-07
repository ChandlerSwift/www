---
title: New Year, New Router!
layout: post
---

Over Christmas break, I replaced my old router (a standard x86_64 PC running
pfSense[^which-im-happy-to-get-away-from]) with a new
[FriendlyElec NanoPi R2S](https://wiki.friendlyelec.com/wiki/index.php/NanoPi_R2S),
which has (for the first few days, anyway) been a fantastic bit of hardware. On
the software side, I'm running OpenWRT, which is a stability upgrade from
pfSense, and a major functionality bump from any other router OS I've tried.
I'm now a few days in, and it's been a really nice experience.

[^which-im-happy-to-get-away-from]: I'm
    [pretty happy to be done with pfSense](https://github.com/doktornotor/pfsense-still-closedsource).
    Their software is definitely usable, but their business shenanigans plus the
    fact that their software isn't really Open Source have left a pretty bad
    taste in my mouth, and I'm happy to be moving on. Plus, a major yikes at the
    [whole pfSense/Wireguard fiasco](https://arstechnica.com/gadgets/2021/03/buffer-overruns-license-violations-and-bad-code-freebsd-13s-close-call/)!

<!--more-->

It's worth clarifying that this isn't the combination router/access point device
that many people mean when they say "router". An off-the-shelf wireless
router/AP performs a whole bunch of functions, and this device performs many,
but not of all, of those:

- [x] Packet routing/NAT
- [x] Firewall
- [x] DHCP server
- [x] DNS server/forwarder
- [x] VPN server (WIP, untested)
- [ ] Wireless access point (I use a [Unifi AC Lite](https://store.ui.com/products/unifi-ac-lite), which may soon also be running OpenWRT)
- [ ] Ethernet switch (I'm running a Netgear GS724T switch I pulled out of a
      dumpster; nothing fancy, but it gets the job done)
- [ ] Modem, sometimes (I use a [Motorola MB7220](https://www.motorola.com/us/mb7220/p))

{{< toc >}}

## Hardware

### Acquisition: Ordered from AliExpress

Shipping from the official FriendlyElec site was fairly expensive. The board,
case, and USB cable totaled $41.99, and shipping was at least an additional $17.
Plus, I'm too impatient to wait two months!

![$17 for "China Post - Extraordinary times: takes up to 2 month", $37 for "DHL Express - Within 10-17 days", $93 for "SF-Express - Within 5-14 days"](new-year-new-router/shipping-prices.png)

Instead, I found a reseller on AliExpress who included free shipping in their $3
markup ($45.81 total, free shipping, plus tax, at the time of purchase.)

https://www.aliexpress.us/item/3256802737557752.html

I placed my order December 1st, and the package arrived December 21st.

### Performance: Adequate for 200mbps
I'm currently on a 200mbps down/10mbps up internet plan. I don't have any
trouble getting that on this hardware. However, gigabit or multi-gigabit might
have trouble, based on a quick benchmark: When downloading at
[full throttle](https://www.speedtest.net/result/14130516086), just over 20% of
my CPU time is used (mostly spent in softirqs). I'd expect this to scale with
network traffic, so I'd plan to top out around a gigabit one way, or 500mbps
full-duplex. If I ever wind up with gigabit fiber, I may want to look at
upgrading; however, this is plenty of headroom for my current connection.

### Thermals: Pretty good with the heatsink

The R2S has a quad-core processor, so I spun up four processes of
`cat /dev/urandom > /dev/null` (a pretty effective single-core CPU stresser) and
watched temperatures. They peaked around 65°C.

<!--
TODO: I tried making an APNG out of all four cores, but the size ended up being
a bit unreasonable. I'd expect it to be around the sum of the layers, but it
ended up being about 20x that size.

$ convert -delay 100 -loop 0 -dispose previous core* apng:core-all-usage.png
$ ls -lh
-rw-r--r-- 1 chandler chandler 9.5K Dec 28 19:28 core-0-usage.png
-rw-r--r-- 1 chandler chandler 9.9K Dec 28 19:29 core-1-usage.png
-rw-r--r-- 1 chandler chandler 9.7K Dec 28 19:29 core-2-usage.png
-rw-r--r-- 1 chandler chandler 9.6K Dec 28 19:29 core-3-usage.png
-rw------- 1 chandler chandler 801K Dec 28 19:49 core-all-usage.png

Note that this isn't just an inefficiency in ImageMagick's PNG compression:

$ convert core-0-usage.png core-0-usage-1.png
$ ls -lh
-rw-r--r-- 1 chandler chandler 4.5K Dec 28 19:51 core-0-usage-1.png
-rw-r--r-- 1 chandler chandler 9.5K Dec 28 19:28 core-0-usage.png

Note that Imagemagick produces a _smaller_ image than the default compression!

So, instead, I created an APNG with https://ezgif.com/apng-maker, which was
much more in line with the size I was expecting.

$ ls -lh all-cores.png
-rw-r--r-- 1 chandler chandler 8.4K Jan  6 13:44 content/posts/2023-01-04-new-year-new-router/all-cores.png
-->
![a two hour graph of CPU usage, hovering around 0% for 30 minutes, hovering around 100% for 60 minutes, and hovering around 0% for 30 more minutes](new-year-new-router/all-core-usage.png)

![a two hour graph of temperature, stabilizing around 65°C after half an hour after the CPU spike](new-year-new-router/temperature.png)

I haven't done any kind of burn-in test, but my suspicion is that this chip
should be able to run flat out indefinitely. I'd been considering opening this
up and applying thermal paste (which, I suspect, is somewhere between
unoptimally applied and nonexistent at the moment), but it looks like that won't
be necessary.

Note that I didn't do anything fancy for testing here, so take these
observations with a generously sized grain of salt. It's plausible that the
temperature sensor isn't properly calibrated; it's plausible that there's
throttling happening which I haven't noticed; it's plausible that this is a poor
stress test, and that running something else would generate quite a bit more
heat; it's plausible that my house being 10°F warmer in the summer would cause
some additional problems. All that said, I'm comfortable enough that I don't
feel the need to do more investigation unless I run into problems.

[Further discussion on the Armbian forums](https://forum.armbian.com/topic/14365-nanopi-r2s-overheating-and-throttling/)

### Power consumption: Typically 2-3 Watts
When idle, the router pulls as little as 2.0 to as much as 2.5 watts; it seems
to average 2.1 or 2.2, measured with a
[Kill-A-Watt P4400](http://www.p3international.com/products/P4400.html). When
running a speedtest (so about 200mbps down), I measured barely more power
(2.3–2.6W), and when running a quad-core stress test, the highest observed peak
was 4.2 watts.

### Other considered hardware
I'd also been looking at some other models in the NanoPi line, and ooh boy do
they ever make a lot of models. This feels like one of those choices that might
be accidentally turing-complete! Here's a comparison of all of NanoPi's boards
with at least two ethernet ports. Prices listed are all from FriendlyElec: I'd
never have finished this post if I also collected the best AliExpress prices for
each!

<style>
    table {
        border-collapse: collapse;
    }
    table thead {
        border-bottom: 2px solid #ddd;
        text-align: left;
    }
    table th {
        padding: 10px;
    }
    table td {
        padding: 10px;
        border-top: 1px solid #ddd;
    }

    @media only screen and (min-width: 800px) {
        table {
            margin: 30px;
            width: calc(100% - 60px);
            min-width: 400px;
        }
    }
</style>

Product | Processor | Memory | Storage | Ethernet ports | Price with case
--------|-----------|--------|---------|----------------|----------------
[NanoPi R2C Plus](https://www.friendlyelec.com/index.php?route=product/product&product_id=286) | Rockchip RK3328: 4x Cortex-A53 | 1GB DDR4 | 8GB eMMC | 1x native 1Gbps, 1x USB3 1Gbps | $39
[NanoPi R2S](https://www.friendlyelec.com/index.php?route=product/product&product_id=282) | Rockchip RK3328: 4x Cortex-A53 | 1GB DDR4 | — | 1x native 1Gbps, 1x USB3 1Gbps | $39
[NanoPi R4S](https://www.friendlyelec.com/index.php?route=product/product&product_id=284) | Rockchip RK3399: 4x Cortex-A72 + 4x Cortex-A53 | 4GB LPDDR4 | — | 1x native 1Gbps, 1x PCIe 1Gbps | $75
[NanoPi R4SE](https://www.friendlyelec.com/index.php?route=product/product&product_id=288) | Rockchip RK3399: 4x Cortex-A72 + 4x Cortex-A53 | 4GB LPDDR4 | 32GB eMMC | 1x native 1Gbps, 1x PCIe 1Gbps | $80
[NanoPi R5C](https://www.friendlyelec.com/index.php?route=product/product&product_id=290) | Rockchip RK3568B2: 4x Cortex-A55 | 1GB LPDDR4X | 8GB eMMC | 2x PCIe 2.5Gbps[^pcie-wifi-too] | $49
[NanoPi R5C](https://www.friendlyelec.com/index.php?route=product/product&product_id=290) | Rockchip RK3568B2: 4x Cortex-A55 | 4GB LPDDR4X | 32GB eMMC | 2x PCIe 2.5Gbps[^pcie-wifi-too] | $59
[NanoPi R5S](https://www.friendlyelec.com/index.php?route=product/product&product_id=287) | Rockchip RK3568B2: 4x Cortex-A55 | 2GB LPDDR4X | 8GB eMMC | 1x native 1Gbps, 2x PCIe 2.5Gbps | $75
[NanoPi R5S](https://www.friendlyelec.com/index.php?route=product/product&product_id=287) | Rockchip RK3568B2: 4x Cortex-A55 | 4GB LPDDR4X | 16GB eMMC | 1x native 1Gbps, 2x PCIe 2.5Gbps | $85
[NanoPi R6S](https://www.friendlyelec.com/index.php?route=product/product&product_id=289) | Rockchip RK3588S: 4x Cortex-A76 + 4x Cortex-A55 | 8GB LPDDR4X | 32GB eMMC | 1x native 1Gbps, 2x PCIe 2.5Gbps | $139

Many of these have other features like various speed USB ports, GPUs and HDMI
out, WiFi and Bluetooth adapters, and IR receivers. I didn't care about any of
those use cases, so those aren't mentioned here. I also didn't include the
specifics on CPU and memory clock speeds, or on eMMC performance, though those
may factor in to many use cases. My needs aren't too demanding, which is why I
ended up happy with the lowest-spec'ed device on the list!

[^pcie-wifi-too]: This board also includes an M.2 slot for a PCIe WiFi adapter
    on the bottom, which I can buy for an extra $18. I didn't include that in my
    comparison, because I use a discrete access point, which is designed to be
    an access point and nothing else.

All in all, the basic board I ordered was plenty for my use case: I don't have
fast enough internet (thanks, Comcast!) to saturate download bandwidth; I don't
have enough upload bandwidth to be CPU-limited when using a VPN from elsewhere;
I don't run vlans or anything that requires internal-only networking to pass
through the router; and I don't have >1Gbps networking set up anywhere in my
house.

And, worth a mention: FriendlyElec's documentation is really good. See for this
board, for example: http://wiki.friendlyelec.com/wiki/index.php/NanoPi_R2S

## Installing OpenWRT

OpenWRT's documentation (despite being labeled "Under Construction") for the R2S
is fantastic.

https://openwrt.org/toh/friendlyarm/nanopi_r2s

Installing OpenWRT is pretty straightforward: Write the downloaded disk image to
a microSD card, insert the card, and log into the router for first-time
configuration. I'd guess the part that took me the longest was finding a blank
microSD card!

## Configuring OpenWRT

This is my first experience with OpenWRT, and I wanted easy, so I stuck to
[LuCI](https://openwrt.org/docs/guide-user/luci/luci.essentials), the web-based
administration portal LuCI is just a convenient wrapper around
[UCI](https://openwrt.org/docs/guide-user/base-system/uci), the Unified
Configuration Interface, which amounts to editing text files in `/etc/config`.

Initial configuration amounted to setting up an administrator password, setting
up some basics like time and time zone, and adding my SSH keys.

### Basic routing: Plug and play

I just plugged in the router and the
[tubes](https://en.wikipedia.org/wiki/Series_of_tubes) started flowing. No
configuration needed.

### Static DHCP leases
In general, I try to use DHCP for everything I can; however, there are a few
things on my network for which I need to have static addresses set up. (I set
these up as static DHCP leases, so they can survive accidental networking
configuration changes; I've done that more than once!) Those exceptions are, at
the moment, the router, my desktop, and my HTTP server (since I can't port
forward to a dynamic IP address).

This was straightforward to setup: Network > DHCP and DNS > Static Leases.

### Port forwarding

Network > Firewall > Port Forwards

At the point that I was trying to configure these, I hadn't really gotten used
to the UI yet, and I didn't notice that below the menu and dropdown submenus at
the top, there's another tier of menus in a tabbed interface below, and port
forwarding is hidden behind one of these.

I try to keep as few ports open as possible, but do forward `:80`, `:443`,
`:25565` (occasionally), and a few ports for custom internal services that I
occasionally want friends to have access to without necessarily needing to be
VPN'ed into my network.

### DDNS

I use Cloudflare for my DNS.

I installed the `luci-app-ddns`, `ddns-scripts`, and `ddns-scripts-cloudflare`
packages, and then configured DDNS through the web interface (Services > Dynamic
DNS).

I tried to set the service up without reading through the documentation, which
proved to be a mistake. I ran into a few issues that I had to fall back to
reading the (excellent) documentation for:

* For a domain like `home.chandlerswift.com` in the `chandlerswift.com` zone, I
  need to put `home@chandlerswift.com` in the Domain field. (Docs: "To use subdomains (CNAME or A records), use the format below when filling your credentials: `domain {subdomain}@[zone]`")
* Credentials aren't my CloudFlare credentials, but they don't use OAuth or
  similar either. Instead, I have to create a new API token through the
  Cloudflare dashboard, and use username `Bearer` and password `{token}` to
  authenticate.
  (Docs: "[Create Custom Token](https://dash.cloudflare.com/profile/api-tokens)
  by following the
  [Creating API tokens guide](https://developers.cloudflare.com/api/tokens/create/).
  Make sure to add “Zone DNS Edit” Permission to your custom token. You can also
  “include Specific zone” under Zone Resources. ...
  `username Bearer`, `password [Your API token]`")

Docs: https://openwrt.org/docs/guide-user/services/ddns/client#cloudflarecom

### Monitoring/pretty graphs with [collectd](https://collectd.org/)

I'm monitoring an assortment of things with collectd, which I'd never used
before and am now enamored with. It's very plausible that I'm going to stand up
a proper collectd collector somewhere on my network, and send a variety of stats
there. I do like graphs!

![a screenshot of some collectd graphs](new-year-new-router/collectd.png)

I installed the `luci-app-statistics` package, plus `collectd-mod-thermal` for
the thermal sensor images above, and now I have memory, networking, and CPU
stats, plus potentially more in the future.

I haven't yet figured out what the default LuCI install uses for its statistics
(Status > Realtime Graphs), and if I can add stats to that instead of collectd.
It does seem, though, that those stats are only graphed when I'm viewing the
page, while I can get historic graphs at any time with collectd.

![a screenshot of some built-in graphs](new-year-new-router/luci-other.png)

I'm currently not persisting my collectd logs anywhere. I may send them off to
another server at some point: the NAS, possibly? But for now they're just going
into `/tmp`, and will be lost on reboot.

In addition to what I have set up, there are lots of other plugins for
monitoring other data points with collectd:

<details>
<summary>List of available collectd packages</summary>

```text
root@OpenWrt:~# opkg list | grep collectd-mod
collectd-mod-apache - 5.12.0-33 - apache status input plugin
collectd-mod-apcups - 5.12.0-33 - apcups status input plugin
collectd-mod-ascent - 5.12.0-33 - ascent status input plugin
collectd-mod-bind - 5.12.0-33 - BIND server/zone input plugin
collectd-mod-chrony - 5.12.0-33 - chrony status input plugin
collectd-mod-conntrack - 5.12.0-33 - connection tracking table size input plugin
collectd-mod-contextswitch - 5.12.0-33 - context switch input plugin
collectd-mod-cpu - 5.12.0-33 - CPU input plugin
collectd-mod-csv - 5.12.0-33 - CSV output plugin
collectd-mod-curl - 5.12.0-33 - cURL input plugin
collectd-mod-df - 5.12.0-33 - disk space input plugin
collectd-mod-dhcpleases - 5.12.0-33 - show dhcpleases plugin
collectd-mod-disk - 5.12.0-33 - disk usage/timing input plugin
collectd-mod-dns - 5.12.0-33 - DNS traffic input plugin
collectd-mod-email - 5.12.0-33 - email output plugin
collectd-mod-entropy - 5.12.0-33 - Entropy amount input plugin
collectd-mod-ethstat - 5.12.0-33 - Ethernet adapter statistics input plugin
collectd-mod-exec - 5.12.0-33 - process exec input plugin
collectd-mod-filecount - 5.12.0-33 - file count input plugin
collectd-mod-fscache - 5.12.0-33 - file-system based caching framework input plugin
collectd-mod-interface - 5.12.0-33 - network interfaces input plugin
collectd-mod-ipstatistics - 5.12.0-33 - ipstatistics input plugin
collectd-mod-iptables - 5.12.0-33 - iptables status input plugin
collectd-mod-irq - 5.12.0-33 - interrupt usage input plugin
collectd-mod-iwinfo - 5.12.0-33 - libiwinfo wireless statistics plugin
collectd-mod-load - 5.12.0-33 - system load input plugin
collectd-mod-logfile - 5.12.0-33 - log files output plugin
collectd-mod-lua - 5.12.0-33 - lua input/output plugin
collectd-mod-match-empty-counter - 5.12.0-33 - empty-counter match plugin
collectd-mod-match-hashed - 5.12.0-33 - hashed match plugin
collectd-mod-match-regex - 5.12.0-33 - regex match plugin
collectd-mod-match-timediff - 5.12.0-33 - timediff match plugin
collectd-mod-match-value - 5.12.0-33 - value match plugin
collectd-mod-memory - 5.12.0-33 - physical memory usage input plugin
collectd-mod-modbus - 5.12.0-33 - read variables through libmodbus plugin
collectd-mod-mqtt - 5.12.0-33 - transmit data with MQTT plugin
collectd-mod-mysql - 5.12.0-33 - MySQL status input plugin
collectd-mod-netlink - 5.12.0-33 - netlink input plugin
collectd-mod-network - 5.12.0-33 - network input/output plugin
collectd-mod-nginx - 5.12.0-33 - nginx status input plugin
collectd-mod-ntpd - 5.12.0-33 - NTP daemon status input plugin
collectd-mod-nut - 5.12.0-33 - UPS monitoring input plugin
collectd-mod-olsrd - 5.12.0-33 - OLSRd status input plugin
collectd-mod-openvpn - 5.12.0-33 - OpenVPN traffic/compression input plugin
collectd-mod-ping - 5.12.0-33 - ping status input plugin
collectd-mod-postgresql - 5.12.0-33 - PostgreSQL status input plugin
collectd-mod-powerdns - 5.12.0-33 - PowerDNS server status input plugin
collectd-mod-processes - 5.12.0-33 - process status input plugin
collectd-mod-protocols - 5.12.0-33 - network protocols input plugin
collectd-mod-routeros - 5.12.0-33 - MikroTik RouterOS input plugin
collectd-mod-rrdtool - 5.12.0-33 - RRDtool output plugin
collectd-mod-sensors - 5.12.0-33 - lm_sensors input plugin
collectd-mod-smart - 5.12.0-33 - smart input plugin
collectd-mod-snmp - 5.12.0-33 - SNMP input plugin
collectd-mod-snmp6 - 5.12.0-33 - snmp6 input plugin
collectd-mod-sqm - 5.12.0-33 - SQM/qdisc collection plugin
collectd-mod-swap - 5.12.0-33 - swap input plugin
collectd-mod-syslog - 5.12.0-33 - syslog output plugin
collectd-mod-table - 5.12.0-33 - table-like structured file input plugin
collectd-mod-tail - 5.12.0-33 - tail input plugin
collectd-mod-tail-csv - 5.12.0-33 - tail CSV input plugin
collectd-mod-tcpconns - 5.12.0-33 - TCP connection tracking input plugin
collectd-mod-teamspeak2 - 5.12.0-33 - TeamSpeak2 input plugin
collectd-mod-ted - 5.12.0-33 - The Energy Detective input plugin
collectd-mod-thermal - 5.12.0-33 - system temperatures input plugin
collectd-mod-threshold - 5.12.0-33 - Notifications and thresholds plugin
collectd-mod-ubi - 5.12.0-33 - Unsorted block images plugin
collectd-mod-unixsock - 5.12.0-33 - unix socket output plugin
collectd-mod-uptime - 5.12.0-33 - uptime status input plugin
collectd-mod-users - 5.12.0-33 - user logged in status input plugin
collectd-mod-vmem - 5.12.0-33 - virtual memory usage input plugin
collectd-mod-wireless - 5.12.0-33 - wireless status input plugin
collectd-mod-write-graphite - 5.12.0-33 - Carbon/Graphite output plugin
collectd-mod-write-http - 5.12.0-33 - HTTP POST output plugin
```

</details>

### Disk space
The image that OpenWRT provides contains a partition just over 100MB in size.
This, of course, wildly underutilizes the available space when extracted to a
16GB microSD card. The way it's set up makes sense, as they need to build their
images to the lowest common denominator of disk space, and most people don't
need that much space anyway. I don't _really_ care; I'm currently using `18.86
MiB / 102.33 MiB (18%)` of my disk space, and I don't anticipate installing many
more packages. But for use cases like logging, it might be nice to have more
disk space available.

It [sounds like](https://forum.openwrt.org/t/resizing-root-partiton/11019) the
best way to deal with this is to either manually extract each image onto the
disk, or to build my own images with a custom amount of space. Either of these
is a feasible workaround, but my current view is that I'm going to cross that
bridge when I run out of space. Plus, I like having the microSD card as a mostly
read-only filesystem, since they're not known for their reliability.

### Unimplemented/Unresolved issues
* OpenWRT uses a self-signed certificate for LuCI over HTTPS. Can I use a proper
  cert? At least I'd like to use something from my internal CA.
* VPN: I've explored both OpenVPN and Wireguard. These were painful and
  unimplemented-then-badly-implemented, respectively, on pfSense, and I haven't
  finished setting them up here yet.
  https://openwrt.org/docs/guide-user/services/vpn/wireguard/basics,
  https://openwrt.org/docs/guide-user/services/vpn/openvpn/start
* I'd like to do some kind of per-device bandwidth monitoring, which apparently
  OpenWRT has
  [good support for](https://openwrt.org/docs/guide-user/services/network_monitoring/start).
  I'm rarely even remotely close to it, but Comcast does impose a data cap that
  I'm reasonably keen to avoid.
* I use a small USB-enabled UPS (an 
  [Amazon Basics-branded white-label APC unit](https://www.amazon.com/AmazonBasics-Standby-UPS-600VA-Outlets/dp/B073Q48YGF))
  to keep my network gear running through brief power outages. I'd love to use
  the router to monitor power draw on the UPS and its expected runtime. OpenWRT
  appears to have support for this:
  https://openwrt.org/docs/guide-user/services/ups/apcupsd_su700,
  https://networkupstools.org/ (Though at the moment, the battery appears to be
  on death's door, as it dies an under-voltaged death on any significant load; I
  typically use <100w for all of my networking/server gear, and it's a 600VA UPS
  so it should be able to handle the load without any issues!)
* As long as I'm messing around with networking gear, now would be a great time
  to set up vlans for my IoT gear. My switch and access point both support this,
  so it might be nice to try.
  https://openwrt.org/docs/guide-user/network/vlan/start

### Reboot time: 30 seconds
One thing I wanted to measure was how long the router takes to come back up
after a reboot or power outage. My fairly unscientific test ("start pinging the
router, SSH in and reboot the router, measure how many seconds' worth of pings
are lost"), repeated 3 times, yielded 29, 29, and 30 seconds. This isn't
fantastic (something this basic should probably be able to start and get network
connected somewhat faster) but it's definitely usable, and an improvement over
what I had with pfSense.

### UI samples

![the LuCI home screen](new-year-new-router/home.png)

![SSH configuration](new-year-new-router/ssh.png)

![Dynamic DNS configuration](new-year-new-router/dynamic-dns.png)

![DHCP and DNS configuration](new-year-new-router/dhcp-and-dns.png)

![Package management](new-year-new-router/software.png)
