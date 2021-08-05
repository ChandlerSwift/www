---
title: Notes on Building AsteroidOS
layout: post
tags: asteroidos
IncludeSyntaxStyles: true
---

Building AsteroidOS isn't terribly difficult, and reasonably well documented,
but there are a handful of gotchas I ran into during the process.

<!--more-->

### Build with one thread at a time

The OpenEmbedded build system, which AsteroidOS is based on, seems to have
problems running concurrent builds. I tried to do some debugging to isolate the
problem, but gave up after a few tries; it's hard to stay interested with a
several hour long build-run-debug cycle. It also didn't seem to be the same
problem every time; perhaps there's some kind of race condition somewhere.

The solution is pretty simple:

```sh
export BB_NUMBER_THREADS=1
```

Experimentally, after a successful initial run, I haven't had problems doing
subsequent parallel builds. YMMV!

### Building on Arch etc. with Docker
Arch Linux ships with newer versions of packages than AsteroidOS allows by
default, so I'm running the build inside of Docker. Here's what I use:

```sh
#!/bin/sh
docker build -t asteroidos-toolchain .

docker rm -f asteroidos-toolchain
docker run --name asteroidos-toolchain -it \
	-u `id -u`:`id -g` \
	-v "$HOME/.gitconfig:/$HOME/.gitconfig" \
	-v "$(pwd):/asteroid" \
	asteroidos-toolchain \
	bash -c "source ./prepare-build.sh update && \
		source ./prepare-build.sh harmony && \
		BB_NUMBER_THREADS=1 nice bitbake asteroid-image || bash"
```

This provides a handful of niceties I've come to appreciate. Line by line:

```sh
docker build -t asteroidos-toolchain .
# This ensures the image is up to date. Thanks to Docker's caching, though,
# it won't take more than a second or so if the image is already built.

docker rm -f asteroidos-toolchain
# This cleans up after the last image. I could just add --rm to the `docker run`
# command, but this lets it stay around afterwards if I want to do any post hoc
# troubleshooting

docker run --name asteroidos-toolchain -it \
	-u `id -u`:`id -g` \
	# Use the same user and group inside the container as outside. If I didn't
	# do this, I'd have permissions issues on files created in the volume mounts

	-v "$HOME/.gitconfig:/$HOME/.gitconfig" \
	# It seems that the prepare-build.sh script occasionally attempts to make
	# commits, so I need my user.name and user.email config values.

	-v "$(pwd):/asteroid" \
	# I want the files present after the container exits, so I do all my work
	# in a volume mount here. This also means I can keep caches between runs.
	asteroidos-toolchain \ # The container we built earlier

	bash -c "source ./prepare-build.sh update && \
		source ./prepare-build.sh harmony && \
		BB_NUMBER_THREADS=1 nice bitbake asteroid-image || bash"
		# The prepare-build script invocations are pretty standard. I have a
		# KW88 Pro, so I use the `harmony` image. The BB_NUMBER_THREADS=1 is
		# documented above, to work around that concurrency bug. `nice`, by
		# default, sets a niceness (roughly the reverse of priority; processes
		# that are more "nice" will run with lower priority, with the scheduler
		# giving up their timeslices if there's contention for CPU time) of 10,
		# so this will soak up all my available processing power in the
		# background without much of an impact on my foreground work. The
		# `|| bash` at the end simply drops me into a bash shell if the previous
		# command fails so that I can troubleshoot in the container if I want.
```

One more note: Since I'm running `./prepare-build.sh update` in the container, I
need to be able to `git pull` all of the repos. I'm not passing in my ssh
private keys, so I can't pull over `ssh`. That's okay, since I'm not pushing
upstream anyway; I'll just switch to `https`:
```sh
git remote set-url origin https://github.com/AsteroidOS/asteroid.git
```

### Running a build server
I try to automatically build up-to-date packages for supported watches. This
lets me keep my own watch updated, and verify that the changes I make don't
break on other builds as well.

Those builds are available at
[home.chandlerswift.com/asteroid/](https://home.chandlerswift.com/asteroid/) and
run periodically -- [let me know](mailto:chandler@chandlerswift.com) if you use
these, or if you want to use them and you need help getting `opkg` set up to use
them!

I built this on my local machine originally, and didn't want to start from
square one on the build VM, so I copied over my build files. One particular
gotcha here is that apparently the OpenEmbedded build system makes extensive
use of hard links to save space. I tried `rsync`ing my `asteroid` directory to
the VM, and the 60GB directory filled up the 250GB of disk space the VM had
available! That's not right. However, `rsync` will honor hardlinks if you ask it
politely:

```sh
rsync --archive \
      --verbose \
      --info=progress2 \
      --keep-dirlinks \
      --hard-links \
      --delete \
      ./ asteroidos-build:asteroid/
```

That did the trick for me.

On the build side, I have a short script that builds everything. (Note: this
might take days!)
```sh
#!/bin/bash

cd ~/asteroid/

WATCHES="anthias bass dory harmony inharmony lenok mooneye smelt sparrow sprat sturgeon sawfish swift tetra wren"
ADDITIONAL_PACKAGES="vim gdb alsa-utils "
#ADDITIONAL_PACKAGES+="quake "

for watch in $WATCHES; do
	. prepare-build.sh $watch
	BB_NUMBER_THREADS=1 bitbake asteroid-image $ADDITIONAL_PACKAGES
	cd ~/asteroid
done
```

I can add any extra packages that I want built, and they'll just show up in the
repos for each watch. Pretty slick!
