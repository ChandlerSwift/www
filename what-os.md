---
title: What OS/Distro am I currently using?
layout: page
---

# What OS/Distro am I currently using?

For the better part of the last decade (!) I've been using some flavor of Linux
as either my primary or active secondary operating system. I've switched between
quite a few different distributions, for a varying set of reasons which no
longer fit in a throwaway line in my "about me" page. I think the list of
operating systems I use, as well as the rationales behind them, provides an
interesting insight into what I've prioritized in an operating system over time.

Note that these are distros that have worked for me, and may or may not be a
good fit for anybody else. That said, I'm happy to help anyone who wants to make
one of these work for them; [drop me a line](mailto:chandler@chandlerswift.com)!

Current as of Fall 2020.

### 2012: Linux Mint

I don't actually remember a date on this one, but I _do_ remember that my
first release of Linux Mint was 13. I installed it on a Dell Latitude D810
that no longer quite kept up with Windows (XP was obsolete, though not _quite_
out of support yet; Windows 7 wouldn't comfortably run with the maxed-out 2GB
of RAM the laptop supported). After a bit of research (read:
"google.com/search?q=what+linux+is+best"), Mint seemed like a good starting
point. In retrospect, it was an easy introduction to Linux: it gave me a taste
of what Free Software had to offer, without making me do too much scary
command line hacker business. Also, the MATE desktop environment was welcoming
and performant on the hardware at the time. Given my limited experience, and
the fact that the laptop was likely eight to ten years old at this point, that
made for a strong combination suited to my inexperience and hardware.

During this time, I did play around with a few other distributions (which
mostly consisted of Ubuntu, with varying desktop environments). LXDE was okay,
but I didn't like it as much as MATE. Puppy Linux was fun---and sooo
fast!---but it didn't come with a software suite I liked as much.

### Spring or Summer 2015: Ubuntu Server

Around this time I started thinking about servers. There were quite a few
projects related to this, my favorite of which was a streaming radio server,
which entirely deserves its own blog post. 

### Fall 2015: Ubuntu

Off to college, and with that, a new laptop! An Acer Aspire 15,
i5-5200u/8GB/1TB hybrid drive. Finally, I could run Unity! Which I did, for a
while, probably about six months. I ran into issues using it for coursework,
so I was back to Windows for most of my freshman year.

### Spring 2016: Windows

Spring 2016 was back to Windows. Windows 10 was new, exciting, and fixed a lot
of my complaints about Windows 7 and 8. I was a big fan of
[MobaXTerm](https://mobaxterm.mobatek.net/), which gave me really nice
SSH/SFTP/etc integration into Windows; enough to scratch my
"file-manager-that-just-works-with-remote-systems" itch. Also, it worked well
with non-CS coursework.

### Fall 2017: Ubuntu GNOME

Windows is frustrating. Why can't I just [ssh into things from the command
prompt|have a nice command prompt|have a file manager I like|not have to deal
with Windows Defender|...]? GNOME seems to be the way of the future, and
Ubuntu announced that they'd be going that direction, so I decided to be an
early adopter. With 18.04, mainline Ubuntu came with GNOME so I was back with
standard Ubuntu. This one actually stuck for quite a while, though I dual
booted pretty regularly with Windows for games, projects, classes, and
sometimes work.

### Spring 2019: New Laptop, New OS: Debian

Spring 2019 I bought a new laptop! It was a tablet convertible, and the
Windows 10 that it came with was great in the support it had for the hardware.
For that reason, despite the pitiful amount of disk space I was working with,
I did leave Windows as an option. Additionally, I did an extended stretch of
development on a .NET project, so I needed Visual Studio, and by extension,
Windows, for that.

Ubuntu, by this point, had started to embrace snaps as their method of
application distribution, and the combined bundling of Amazon search and other
unwanted applications was starting to get on my nerves. I _did_ like the `apt`
package manager, so why not cut out the middleman! Debian seemed like the
logical conclusion. I've been pretty pleased with Debian since: Debian Stable
is a rock-solid base for servers and desktops alike, and when I need newer
packages, Debian Testing has me covered!

Also, this was my first time using Wayland, and it _just works_ with my laptop's
touchscreen in a way that X just didn't. Sway is a fantastic i3 replacement, and
the few things I don't have Wayland support out of the box are made easy with
`xwayland`. Hopefully this will be a struggle of the past soon, but I'm thrilled
with how easy Wayland is making a display server switch.

### Spring 2020: Arch Linux
Okay, so it's been almost a year, and my system doesn't seem to know whether
it's on Debian Unstable or Testing, and I certainly don't! What a mess. All I
wanted was the latest version of Python! Some of the guys I work with like Arch.
I don't _really_ want to be the "btw I use arch" guy, but what the heck? I
figured I'd give it a shot.

Initial installation was a bit less do-it-in-my-sleep-easy than, say, Ubuntu or
Debian, but after running through it once or twice, I felt like I really
_understood_ the install process. There's no magic, just some disk partitioning,
copying of packages, set up an `/etc/fstab`, load `grub`, and voilà! An install
that I understand, because I built it.

The install was my first exposure to that ideology of "everything makes sense
because you made it that way", but it seems like everything works that way with
Arch, and I like it. Plus, reasonably stable but up-to-date software, packaged
as upstream intended. `pacman` is easy to use and oh so very fast; the official
repos are well-stocked (not to mention the AUR!); and `yay` is fantastic! And
_nobody_ beats the Arch Wiki!

### Honorable Mention
 * OpenSUSE: For a job I was working on at the time (probably late 2016), I
   wound up using OpenSUSE because one of our largest clients used it, so they
   wanted somebody testing on their platform. It was fine, no complaints.
 * Void Linux: A few of my good friends in the UMD ACM Club swore by Void. I
   like the philosophy, but I had a lot of issues during the install process
   and afterwards that I wasn't really prepared to deal with at the time, and I
   didn't want to spend all my time debugging driver issues.
