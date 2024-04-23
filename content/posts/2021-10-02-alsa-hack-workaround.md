---
title: Hacking together a workaround for Audio issues
layout: post
IncludeSyntaxStyles: yes
---

I've had a longstanding issue somewhere in my system's config where when I
adjust my system volume using the hardware wheel, the left and right channels
get out of sync. It's certainly something I can work around, but it's
frustrating to have to either have to turn the volume all the way down, which
resynchronizes the channels, or to open `alsamixer` or similar and manually
adjust the right and left channels to match.

<!-- more -->

Here's me spamming the volume wheel, and watching the issue in `alsamixer`:

<noscript>
If you don't use JavaScript, watch on asciinema here:
<a href="https://asciinema.org/a/DirP2shBb94KStKfjUvZpOsXy" target="_blank"><img src="https://asciinema.org/a/DirP2shBb94KStKfjUvZpOsXy.svg" /></a>
</noscript>
<script id="asciicast-DirP2shBb94KStKfjUvZpOsXy" src="https://asciinema.org/a/DirP2shBb94KStKfjUvZpOsXy.js" async></script>

It's an inconvenient reality that sometimes fixing the root cause[^root-cause]
of the issue just isn't nearly as easy as patching together a service that
addresses the symptom! (This was also a good excuse to gradually introduce
myself to ALSA's libraries; I'm not sure I would have figured out the root cause
of the issue if I hadn't been playing with this project.) This program
periodically checks the volume of the default output's left channel, and adjusts
the right channel's volume to match:

[^root-cause]: It seems that `amixer` runs into a race condition when run
    multiple times concurrently. This happens as a result of my `sway` config;
    `amixer` is called on each "press" of the `XF86AudioRaiseVolume` key, which
    may happen begin the previously called `amixer` instance terminates.

```c
// sudo pacman -Sy alsa-lib
#include <alsa/asoundlib.h>
#include <time.h>

// Based on the code at
// https://stackoverflow.com/questions/6787318/set-alsa-master-volume-from-c-code
int main()
{
	// Set up the mixer for card "default"
	snd_mixer_t *handle;
	snd_mixer_open(&handle, 0);
	snd_mixer_attach(handle, "default");
	snd_mixer_selem_register(handle, NULL, NULL);
	snd_mixer_load(handle);

	// Obtain the mixer element "Master" from the mixer
	snd_mixer_selem_id_t *sid;
	snd_mixer_selem_id_alloca(&sid);
	snd_mixer_selem_id_set_index(sid, 0);
	snd_mixer_selem_id_set_name(sid, "Master");
	snd_mixer_elem_t *elem = snd_mixer_find_selem(handle, sid);

	for (;;) {
		// If any events (say, volume changes) happened since the last
		// iteration, update our handle to reflect that. Without this, no volume
		// changes will be picked up:
		// https://www.raspberrypi.org/forums/viewtopic.php?t=175511
		snd_mixer_handle_events(handle);

		// Find the left channel's volume, and sync it with the right channel
		long left_ch_vol;
		snd_mixer_selem_get_playback_volume(elem, SND_MIXER_SCHN_FRONT_LEFT, &left_ch_vol);
		snd_mixer_selem_set_playback_volume(elem, SND_MIXER_SCHN_FRONT_RIGHT, left_ch_vol);

		// Don't monopolize the CPU; it's okay if the levels desync for 100ms
		nanosleep(&(struct timespec){0, 100 * 1000 * 1000}, NULL); // 100ms
	}

	// Clean up
	snd_mixer_close(handle);
	handle = NULL;
	snd_config_update_free_global();
}
```

For the time being, I'm running this as a `systemd` user service. (Since this
exists to deal with an issue in my `sway` config, it could also be run with an
`exec` line in my `sway` config.)

```text
chandler@xenon ~ % systemctl status --user volume-balancer.service
● volume-balancer.service - Keep L/R channel volumes in sync
     Loaded: loaded (/home/chandler/.config/systemd/user/volume-balancer.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2021-10-02 20:00:56 CDT; 42s ago
   Main PID: 218353 (volume-balancer)
      Tasks: 2 (limit: 19096)
     Memory: 1.1M
        CPU: 217ms
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/volume-balancer.service
             └─218353 /home/chandler/bin/volume-balancer

Oct 02 20:00:56 xenon systemd[2288]: Started Keep L/R channel volumes in sync.
chandler@xenon ~ % cat .config/systemd/user/volume-balancer.service
[Unit]
Description=Keep L/R channel volumes in sync

[Service]
ExecStart=/home/chandler/bin/volume-balancer
Type=simple
Restart=always

[Install]
WantedBy=default.target
chandler@xenon ~ %
```

**Update 2024-04-18:** [Hajo Noerenberg](https://github.com/hn) informs me that
this can be made substantially more efficient by waiting for a mixer event
rather than polling inputs:

```diff
- // Don't monopolize the CPU; it's okay if the levels desync for 100ms
- nanosleep(&(struct timespec){0, 100 * 1000 * 1000}, NULL); // 100ms
+ // Wait for a mixer to become ready (i.e. at least one event pending)
+ snd_mixer_wait(handle, 1000);
```

Hajo also provides a much cleaner solution for a similar problem:

> In the meantime I've released a slightly more complex daemon to watch for audio activity and volume changes:
>
> https://github.com/hn/linkplay-a31/blob/main/openwrt-linkplay-a31/linkplay-emu/src/linkplay-emu.c
>
> Might be helpful for some people perhaps.

Thanks, Hajo!
