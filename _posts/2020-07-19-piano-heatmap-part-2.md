---
layout: post
title: Piano Heatmap Analysis (Part 2)
---

A [long time ago]({% post_url 2015-09-10-piano-heatmap-part-1 %}), I hacked
together a not-quite-working attempt at tracking played keys on a piano. Today,
I took another shot at what that attempt might look like with a few more years'
experience in play.

Here's what I made:
[chandlerswift.github.io/piano-heatmap/](https://chandlerswift.github.io/piano-heatmap/)

![demo of the keyboard playing the licc](/images/piano-heatmap/demo.gif)

Because
[WebMIDI isn't supported](https://developer.mozilla.org/en-US/docs/Web/API/MIDIInput#Browser_compatibility)
[by all browsers](https://caniuse.com/#feat=midi) (with 
[no plans for Firefox support](https://bugzilla.mozilla.org/show_bug.cgi?id=836897)),
you'll need to try this out in a Chromium-based browser. Plug in a keyboard,
and start pressing keys! It displays a nice heatmap of what keys you've pressed,
updated in realtime.

This is a pretty major update from the way I'd done things previously---as a
Windows-first user back in the day, finding tools that were interoperable with
others was a larger problem then. Now, I'd be able to compose a few tools
(probably `aseqdump` piped to some combination of `grep`, `uniq`, and
`sort`[^hacks-who-me-no-id-never] would get me most of the way there!) and have
it just work, but having an easy-to-use cross-platform display option sounded
nice, and WebMIDI promised just that[^no-firefox]!

[^hacks-who-me-no-id-never]: [github.com/umdacm/robot/issues/13](https://github.com/umdacm/robot/issues/13)

[^no-firefox]: Well, mostly! I _did_ have to download Chromium to get it
    working, since as mentioned above, Firefox doesn't currently support
    WebMIDI. Perhaps this will change, but the bug has been open for almost
    eight years now, and I don't want it badly enough to do it myself, so here
    it sits!

SVG seemed to be an easy way to make a simple keyboard display. (In hindsight,
I would have likely been able to do a very similar thing with an HTML canvas,
but &#xAF;\\\_(&#x30C4;)_/&#xAF;!) I didn't find any SVG keyboard illustrations
that I liked, and wound up drawing my own. I started in Inkscape, but Inkscape
adds a lot of [unnecessary, invisible content](https://xkcd.com/2109/) when I'm
just trying to display rectangles. I didn't want anything complex, and the SVG
spec is quite simple, so I just built the SVG myself, with
[a python script](https://github.com/ChandlerSwift/piano-heatmap/blob/master/generate-svg.py)
for tackling the repetitive bits. 

Later on while testing, I _did_ answer a question I've had open since Part 1:
What's the distribution of notes like in "F&uuml;r Elise"? Well, here's a shot
at it[^mistakes-were-made], playing from
[IMSLP's Breitkopf edition](https://imslp.org/wiki/File:PMLP14377-Beethoven_Werke_Breitkopf_Serie_25_No_298_WoO_59_Fuer_Elise.pdf).
This represents once through the entire piece, following repeats, etc., as
marked, strictly as written without embellishment. Ten internet points to anyone
who wants to download a MIDI file from IMSLP and feed it through here (or record
it more carefully than I did!):

[^mistakes-were-made]: Since my computer and stage piano are in separate rooms,
    I dragged a Roland PCR-500 onto my desk as a much more portable tool for
    testing. However, I didn't bother wiring it up for sound, so I couldn't
    actually hear myself play! I have a pretty good sense of what I'm playing,
    even without sound, but I certainly make fewer mistakes when I have auditory
    feedback as well!

![a heatmap of the notes in f&uuml;r elise](/images/piano-heatmap/fur-elise-analyzed.png)

This certainly isn't a finished product; there's no "cumulative score" or
anything; and I think having "leaderboards" would certainly be a fun way to
motivate practice competitively! However, it's exactly what I set out to do
today---an easy way of displaying the data I'd accumulated previously. Now, off
to play some music!
