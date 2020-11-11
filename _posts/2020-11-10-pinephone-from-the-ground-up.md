---
title: "Phone a Month 4?: Setting up PinePhone software from the ground up"
layout: post
tags: pinephone
include_syntax_styles: true
---

I never actually ran anything new on my phone this month. Instead, I've been
tinkering with the PinePhone. Instead of the usual update post, here's some info
on how to install and boot the most basic possible Linux installation for the
PinePhone.

In my defense, I _did_ make quite a few attempts to get something (anything!)
working on the PinePhone, but after trying up-to-date versions of Ubuntu Touch,
PostmarketOS, and Mobian, I found major dealbreakers in each. I can't remember
which had which problem(s), but I struggled with terrible call quality, missed
incoming calls and SMS messages, lack of functioning camera apps, and probably
other issues as well.

In any case, I'm currently running the marvelous
[p-boot](https://xnux.eu/p-boot/) bootloader with Megi's latest
[PinePhone kernel](https://megous.com/git/linux/tree/?h=pp-5.10) (optionally
[prebuilt here](https://xff.cz/kernels/)) and a manually configured initramfs.
I don't expect this to ever be a fully-functional system, but I wanted to build
this system to make sure that I understood all the parts I'd have to be
troubleshooting later on in the process, and it's proven quite useful for that.

The end result of this process is, more or less, the smallest system that can
be said to be running Linux[^though-with-busybox]. It boots to a shell, and
thanks to Busybox, I do have a fairly complete environment. I can write (with
`cat` and `sed` as my editors) and execute shell scripts, and...that's about it!

[^though-with-busybox]: That's not strictly true; I could have written my own
    init process as well and taken busybox out of the process entirely. But then
    I lose some usefulness of the system, and it's a slippery slope---why
    shouldn't I just write my own kernel?

The notes below are given with the caveat that I'm running Arch Linux (and so
x86_64 architecture), and that I have the `base-devel` package installed. It
assumes I'm installing to an SD card located at `/dev/sda`, and building for the
PinePhone 1.2 (where 1.0 was the dev kit, 1.1 was Braveheart, and 1.2 was the
UBports, PostmarketOS, and Manjaro CE's). Adjust as needed; your mileage may
vary.

<style>code { font-size: 1.3em; line-height: 1.4em; }</style>

```sh
mkdir -p ~/mobile/pinephone
cd ~/mobile/pinephone

mkdir -p bootloader/files # This is where the setup for p-boot will go

# Step 1: set up p-boot bootloader
# I don't compile this myself; I use the pre-compiled portions provided.
# Documentation and more info at https://megous.com/git/p-boot/tree/README
git clone https://megous.com/git/p-boot
# the p-boot-conf that comes pre-compiled is compiled for ARM, but we're running
# x86_64. We'll compile our own. If we were using this directly on the PinePhone
# we would be able to skip this step.
gcc -o p-boot/dist/p-boot-conf-native p-boot/src/conf.c

# Step 2: partition the SD card. 
# BE CAREFUL here; you will lose all data on /dev/sda, which could be your hard
# drive! If you're not sure, running `sudo fdisk -l` will tell you the size and
# model of your disks.
#
# Press <m> for help. My configuration looks like this:
## Disk /dev/sda: 28.89 GiB, 31016878080 bytes, 60579840 sectors
## Disk model: Card-Reader
## Units: sectors of 1 * 512 = 512 bytes
## Sector size (logical/physical): 512 bytes / 512 bytes
## I/O size (minimum/optimal): 512 bytes / 512 bytes
## Disklabel type: dos
## Disk identifier: 0x3a6e5394
## 
## Device     Boot  Start      End  Sectors  Size Id Type
## /dev/sda1  *     65536   589823   524288  256M 83 Linux
## /dev/sda2       589824 60579839 59990016 28.6G 83 Linux
#
# I did start the first partition quite a ways into the disk. This may not have
# been necessary, but I didn't want to run into issues with the p-boot binary
# itself (which gets written 8K into the disk) and the first partition, so I
# decided to offset it by 64K sectors (32MiB) into the disk.
sudo fdisk /dev/sda

# Step 3: Write the p-boot binary to the SD card
sudo dd if=p-boot/dist/p-boot.bin of=/dev/sda bs=1024 seek=8

# Step 4: Compile the Linux kernel
# More info at https://github.com/megous/linux/blob/orange-pi-5.10/README.md
# We need a cross-compiler. On Debian derivatives, this would probably be the
# build-essential package.
sudo pacman -Sy aarch64-linux-gnu-gcc
# I'm using megi's kernel from https://megous.com/git/linux/, but for bandwidth
# reasons cloning from the GitHub mirror. (This is a 4GBish repo!)
git clone https://github.com/megous/linux
cd linux
# I was initially confused that the PinePhone branch (currently pp-5.10) wasn't
# the correct branch to build. Instead, there are defconfigs for the PinePhone
# in the orange-pi-* branches.
git checkout orange-pi-5.10
# We'll be using the default configs here:
ARCH=arm64 make pinephone_defconfig
# Time to build! I have an 16-thread processor; scale this for your machine. You
# may have to answer a few questions that the default config did not cover; I'm
# not sure exactly why they don't get populated in the previous step.
ARCH=arm64 \
    CROSS_COMPILE=aarch64-linux-gnu- \
    make -j16 Image dtbs
mv arch/arm64/boot/dts/allwinner/sun50i-a64-pinephone-1.2.dtb ../bootloader/
mv arch/arm64/boot/Image ../bootloader/
cd ..

# Step 5: Build the initramfs
# Initramfs uses a cpio archive to store the filesystem, so we need the `cpio`
# tool. https://en.wikipedia.org/wiki/Initial_ramdisk#Implementation
sudo pacman -Sy cpio
# https://www.jootamam.net/howto-initramfs-image.htm gives a decent walkthrough
# of this process, as well as some background behind why this works.
# First, we create the filesystem:
mkdir -p initramfs/{bin,sbin,etc,proc,sys,usr/bin,usr/sbin}
# Install busybox for a reasonable range of utilities:
curl -O https://www.busybox.net/downloads/binaries/1.31.0-defconfig-multiarch-musl/busybox-armv8l
mv busybox-armv8l initramfs/bin/busybox
chmod +x initramfs/bin/busybox
ln -s busybox initramfs/bin/sh
# We create something for the kernel to run as the init process:
cat > initramfs/init <<EOF
#!/bin/sh

# Create all the symlinks to /bin/busybox
/bin/busybox --install -s

i=1
# Loop forever, displaying an incrementing value
while true; do
	echo Hello world \$i
	i=\$((i+1))
	sleep 1
done
EOF
# The init process should never exit; in theory we should be calling shutdown()
# somewhere in here, but we don't have a shutdown program written yet! However,
# since we're in the initramfs, we don't really have much to worry about with
# an improper shutdown here.
chmod +x initramfs/init
# And create our image!
cd initramfs
find . | cpio -H newc -o > ../bootloader/initramfs.cpio
cd ..

# Step 6: Install all this to the SD card
cat > bootloader/boot.conf <<EOF
no=1
name=Chandler's custom Linux
dtb=sun50i-a64-pinephone-1.2.dtb
atf=fw.bin
linux=Image
initramfs=initramfs.cpio
EOF
cp p-boot/dist/fw.bin bootloader # ATF (Arm Trusted Firmware)
sudo p-boot/dist/p-boot-conf-native bootloader /dev/sda1

# Boot and run!
```


### Next steps
With this done, we should be able to insert your SD card, and boot to the init
script that we added to the initramfs. Unfortunately, we're missing quite a
few things necessary for a functional system. Specifically¸ we don't have
[`util-linux`](https://git.kernel.org/pub/scm/utils/util-linux/util-linux.git/)
([Wikipedia](https://en.wikipedia.org/wiki/Util-linux)), which would normally
provide us with tools like `mount` that are fairly essential for a functioning
system (particularly so since we need to mount things like `/dev` to talk to
hardware!). We don't do anything yet with the second partition on the kernel;
while we could use that instead of an initramfs, that would add some time to the
boot process while providing little benefit at this stage.


### Further reading
A few months ago I picked up a copy of Greg Kroah-Hartman's
[Linux Kernel in a Nutshell](http://www.kroah.com/lkn/), which, in addition to
being a surprisingly entertaining read, has lots of still-relevant information
about the kernel-building process at a high level. It's available for free from
his site, though I did pick up a physical copy of the book.

Everything on [https://xnux.eu/](https://xnux.eu) is worth reading. In addition
to the thorough summaries of the state of PinePhone hardware and software, there
are lots of interesting insights into the development process. 

[https://www.linux.it/~rubini/docs/init/init.html](https://www.linux.it/~rubini/docs/init/init.html)
has an old (but still informative) writeup of what the init process does, and
compares a few different approaches to `init`ing.
