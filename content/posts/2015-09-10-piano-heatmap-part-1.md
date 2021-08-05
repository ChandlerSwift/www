---
layout: post
title: Piano Heatmap Analysis (Part 1)
---

I have always been curious about what the most-used key on my piano is. Songs
like [Billy Joel’s "Prelude"](/images/piano-heatmap/prelude.png)
(C4) or [Beethoven’s "Für Elise"](/images/piano-heatmap/fur-elise.png)
(A2) must throw off averages significantly, especially when practiced
repeatedly, right? Also, I thought it would be cool to figure out how many keys
total have been played: they should add up quickly! There do exist
[programs](https://whatpulse.org/) that do this for computer keyboards (and
[here are my stats](https://whatpulse.org/chandlerswift), if somewhat out of
date), but as far as I could tell there wasn’t a good option for a piano
keyboard.

<!--more-->

This should, in theory, be relatively simple. Nearly all electronic pianos (and
[such things](/images/piano-heatmap/piano-shaped-objects.jpg)) have a MIDI
output connection, which means all that has to be done is to plug this into a
computer and record the keystrokes as they roll in. So how hard can it be? I
figured I’d try making on my own.

To start, I based it off a wonderful piece of freeware called
[MIDI-OX](http://www.midiox.com/). So far, I haven’t come up with anything
MIDI-related that it can’t do. Well, it can’t produce a heatmap, but still,
it’s pretty great! What it _can_ do is save a log of all the MIDI keystrokes as
they come in, which can be analyzed later to compare numbers of keystrokes.
It’s pretty simple:

 * Plug in your MIDI device.
 * Start MIDI-OX.
 * If you press a key on your keyboard, you should see entries on the screen.
 * Go to File > Log, and check "Enable Logging".
 * Check "Append to Log" if you want old entries saved rather than overwritten
   to give a cumulative log.

That will give you your output log. If you’re feeling particularly Regex-y,
you can search the file yourself, otherwise
[experiments.chandlerswift.com/piano-heatmap/](https://experiments.chandlerswift.com/piano-heatmap/)
has my (strongly beta) tester; just upload the log file and see your results,
pretty graph coming soon! As a general rule, about 6000 keys per MB of log file
is not unreasonable, depending on how extensively you use the pedal.

And for anyone who’s wondering, my first few days’ worth of logged keys in
semi-readable form are available [here](/images/piano-heatmap/heatmap.txt),
with D4 my most played key.
