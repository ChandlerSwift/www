---
title: "PinePhone software from the ground up, part 2"
layout: post
tags: pinephone
IncludeSyntaxStyles: true
---

<style>code { font-size: 1.3em; line-height: 1.4em; }</style>
A few weeks ago, I
[compiled and installed a Linux kernel]({% post_url 2020-11-10-pinephone-from-the-ground-up %})
and a bit of other software to run on the PinePhone. Today, let's look at some
next steps.

<!--more-->

First, let's talk about the init process. When the kernel finishes its
initialization process, it launches a single userspace program. Typically, the
kernel will attempt to run `/init`
([if launched from a ramdisk](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/init/main.c?h=v5.9#n159)),
[followed by](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/init/main.c?h=v5.9#n1455)
`/sbin/init`, `/etc/init`, `/bin/init`, and, as a final fallback, `/bin/sh`.
If you're using a recent mainstream Linux distribution, your init process is
likely `systemd`. Ubuntu tried creating a system called
[Upstart](http://upstart.ubuntu.com/), which didn't really catch on; before
that, they used some variant of
[SysVinit](https://en.wikipedia.org/wiki/Init#SysV-style)[^before-my-time].

[^before-my-time]: I didn't start using Linux enough to be aware of things like
    init systems until Ubuntu was well into the Upstart&rarr;systemd migration,
    if you want to know anything about an init system older than systemd, ask
    somebody who lived through a different init system!

The init process is responsible for setting up a computer and spawning all the
subsequent processes that are run[^pstree]. Commonly, this might mean mounting
disks, setting up your path, setting up your network, and starting any services
that you run. When you're ready to turn off or restart your computer, you can
send your init process a signal, and it will (hopefully) stop other running
processes gracefully, and then tell the kernel to shut down or reboot, as the
case may be[^but-not-exit].

[^pstree]: While doing some research for this post, I found out about `pstree`,
    which does pretty much what it says on the tin: prints a pretty listing of
    processes that you have running. It's part of the `psmisc` package, which
    seems to be required by the base system on Arch, at least. This is a listing
    of a pretty bare-bones system before a desktop environment is started up. It
    would be a fair bit lighter without Docker.
    ```
    chandler@xenon ~ % pstree
    systemd─┬─agetty
            ├─containerd───11*[{containerd}]
            ├─dbus-daemon
            ├─dhcpcd─┬─dhcpcd───dhcpcd
            │        └─2*[dhcpcd]
            ├─dockerd───9*[{dockerd}]
            ├─login───zsh───pstree
            ├─polkitd───7*[{polkitd}]
            ├─ssh-agent
            ├─sshd
            ├─systemd─┬─(sd-pam)
            │         └─dbus-daemon
            ├─systemd-journal
            ├─systemd-logind
            ├─systemd-timesyn───{systemd-timesyn}
            └─systemd-udevd
    chandler@xenon ~ %
    ```

[^but-not-exit]: One thing that threw me off initially was that the init process
    shouldn't ever exit, and the kernel will complain if it does. Instead, the
    process ensures everything is ready for shutdown, and then sends a
    `reboot` or `shutdown` system call to the kernel.

Last time, we installed Busybox and ran a shell script that just looped. A shell
script (and, therefore, a shell) is pretty overkill for printing some strings.
Instead, below is a C reimplementation of what we did using Busybox last time.
I'm pretty much just resuming where I left off---we have a functioning
bootloader and kernel, hopefully, so I just need to adjust the initramfs.

```sh
cd ~/mobile/pinephone
mkdir my_init
cat > my_init/init.c <<EOF
#include <stdio.h>
#include <unistd.h>

int main() {
	unsigned int counter = 0;
	while (1) {
		printf("Hello world %i\n", counter++);
		sleep(1);
	}
}
EOF
# Because the compiled init is the only thing in the initramfs, we of course
# can't dynamically link to libraries like (in this case) glibc, which is what
# gcc tries to do by default. Luckily, we can just add -static and gcc will give
# us a nice statically linked binary.
aarch64-linux-gnu-gcc my_init/init.c -o initramfs/init -static

# rebuild initramfs
cd initramfs
find . | cpio -H newc -o > ../bootloader/initramfs.cpio
cd ..

# deploy to SD card
sudo p-boot/dist/p-boot-conf-native bootloader /dev/sda1
```

It still seems like the disk usage is a bit high, though:

```sh
du -hs initramfs/init
# 584K	initramfs/init
```

There's no way a program that's just incrementing a counter and printing 13
bytes of text needs that much space! How does it compare without the statically
linked glibc parts embedded in the binary?
```sh
aarch64-linux-gnu-gcc my_init/init.c -o init-dynamic

du -hs init-dynamic
# 12K	init-dynamic
```

Yeah, that seems better. How can we cut out some of that bloat? Well, glibc has
[drawn complaints](http://ecos.sourceware.org/ml/libc-alpha/2002-01/msg00079.html)
for being [pretty heavyweight](https://www.etalabs.net/compare_libcs.html).
How does [musl](https://musl.libc.org/) stack up?

```sh
# I don't really want to figure out how to get my system's toolchain to link to
# musl, so I'll just do it in a prebuilt container.
docker run --volume `pwd`/my_init:/src \
    --user 1000 \
    muslcc/i686:aarch64-linux-musl \
    sh -c "gcc /src/init.c -o /src/init-musl -static"

du -h my_init/init-musl
# 136K	my_init/init-musl
```

That's a bit better. And with musl's
[easier to understand](https://drewdevault.com/2020/09/25/A-story-of-two-libcs.html)
libraries besides? I'll call it a victory. In theory, these two approaches
should be interchangeable, so you can compile with whichever libc you prefer.

Of course, at this point, we haven't managed to create a system that does
anything particularly useful; we've just removed some dependencies to make our
initramfs a bit smaller. Instead, to demonstrate a bit of I/O, here's a
(relatively) brief C program that draws a sine wave on the screen[^which-dev], responding to touch input.

[^which-dev]: Here's the script to check which `/dev/input` device your
	touchscreen is on:

	```sh
	#!/bin/sh

	Create all the symlinks to /bin/busybox
	/bin/busybox --install -s

	mount -n -t devtmpfs -o mode=0755,size=4M devtmpfs /dev
	echo dev:
	ls /dev
	echo dev input:
	ls /dev/input
	# we see event0, event1, event2, event3, so we check which one is correct:
	for i in 0 1 2 3; do
		echo i: $i
		timeout 5 cat /dev/input/event$i
	done
	```

```c
#include <stdio.h>
#include <sys/mount.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <math.h>
#include <unistd.h>
#include <errno.h>
#include <linux/input.h>
#include <string.h>

#define SCREEN_WIDTH 720
#define SCREEN_HEIGHT 1440

// For more information on writing to framebuffers, check out the slides at
// https://archive.fosdem.org/2020/schedule/event/fbdev/attachments/slides/3595/export/events/attachments/fbdev/slides/3595/fosdem_2020_nicolas_caramelli_linux_framebuffer.pdf

void reset(unsigned char* fbmem) {
	memset(fbmem, 0, SCREEN_WIDTH * SCREEN_HEIGHT * 4);
	// The naïve approach, here, is an order of magnitude slower than above
	//for (int p = 0; p < SCREEN_WIDTH * SCREEN_HEIGHT * 4; p++) {
	//	fbmem[p] = 0;
	//}
}

void draw_sine(unsigned char* fbmem, int x_offset, int h) {
	for (int x = 0; x < SCREEN_WIDTH; x++) {
		int y = SCREEN_HEIGHT/2 + (h/2)*sin((x - x_offset)/100.0);

		// Ensure we don't write out of bounds
		y = fmin(fmax(y, 0), SCREEN_HEIGHT - 1);

		fbmem[(SCREEN_WIDTH * y + x) * 4] = 255;
		fbmem[(SCREEN_WIDTH * y + x) * 4 + 1] = 255;
		fbmem[(SCREEN_WIDTH * y + x) * 4 + 2] = 255;
	}
}

int main() {
	// Since Linux 2.6.32, devtmpfs (https://lwn.net/Articles/330985/) has
	// provided an easy way to automatically mount special device files.
	// (Earlier versions of this program were much longer, and relied on the
	// `mknod` system call to create these as they were used. This turned out
	// to be a much less wieldy approach.) The `mount` system call mounts a
	// `devtmpfs` on `/dev`, so that we can use it to read touch inputs from a
	// file in `/dev/input`, and write output to the framebuffer `/dev/fb0`.
	mount("devtmpfs", "/dev", "devtmpfs", 0, "");

	// Open the framebuffer
	int fb = open("/dev/fb0", O_RDWR);
	if (fb < 0) {
		printf("Error opening /dev/fb0: %i\n", errno);
		return 1;
	}
	// To give us convenient random-write access to the framebuffer, we map the
	// file into memory. Technically, we could likely use fseek() and fwrite(),
	// but being able to easily index and write makes this much more pleasant.
	unsigned char* fbmem = mmap(NULL, SCREEN_WIDTH * SCREEN_HEIGHT * 4,
					PROT_WRITE, MAP_SHARED, fb, 0);

	// Open the touch input device
	//
	// In my case, the touchscreen was at `/dev/input/event3`, where `event0`,
	// `event1`, and `event2` belong to other input devices---power and volume
	// buttons among them. This ordering may not be always the same, and may
	// vary between PinePhone hardware revisions. I checked using a simple init
	// script based on the BusyBox install from last time, included in the
	// footnotes.
	int touchscreen = open("/dev/input/event3", O_RDONLY);
	if (touchscreen < 0) {
		printf("Error opening /dev/input/event3: %i\n", errno);
		return 1;
	}

	// Print and update a sine wave on the framebuffer
	int h = 100; // height of the sine wave, in px
	int x = 0; // horizontal offset

	struct input_event ev;
	int pressed_slot = -1; // no slot selected
	int reporting_slot = 0;
	int previous_x_pos = -1; // no previous position
	int previous_y_pos = -1; // no previous position
	while (1) {
		if (read(touchscreen, &ev, sizeof(struct input_event)) < 0) {
			printf("Error reading touchscreen input\n");
			return 1;
		}

		// Handle touchscreen input
		//
		// Because handling touch input isn't the focus of this post, I'm not
		// going to go into great detail here. If you want, check out docs at
		// https://www.kernel.org/doc/html/latest/input/multi-touch-protocol.html
		if (ev.type != EV_ABS) { // Only listen for absolute position events
			continue;
		}
		switch(ev.code) {
		case ABS_MT_SLOT:
			reporting_slot = ev.value;
			break;
		case ABS_MT_TRACKING_ID:
			if (ev.value > 0 && pressed_slot < 0) {
				pressed_slot = reporting_slot;
			} else if (ev.value < 0 && reporting_slot == pressed_slot) {
				pressed_slot = -1;
				previous_x_pos = -1;
				previous_y_pos = -1;
			}
			break;
		case ABS_MT_POSITION_X: // move left-to-right
			if (reporting_slot == pressed_slot) {
				if (previous_x_pos >= 0) {
					x += ev.value - previous_x_pos;
				}
				previous_x_pos = ev.value;
			}
			break;
		case ABS_MT_POSITION_Y: // adjust vertical scale
			if (reporting_slot == pressed_slot) {
				if (previous_y_pos >= 0) {
					h += ev.value - previous_y_pos;
				}
				previous_y_pos = ev.value;
			}
			break;
		}
		reset(fbmem);
		draw_sine(fbmem, x, h);
	}
}
```

Compile and write to the SD card, and here's what we have:

![demo video of application running](/images/pinephone-from-scratch-demo.gif)

At this point, we have our program running; no other userspace is needed! That's
pretty neat. But for now, we're still running entirely from a ramdisk. We can't
persist any changes, and the initramfs model will get unwieldy quickly as more
assets are added to the image. Next time, we'll take a quick look at what's
needed to mount a root filesystem and persist changes to disk.
