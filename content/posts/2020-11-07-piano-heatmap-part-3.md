---
layout: post
title: Piano Heatmap Analysis (Part 3)
---

A third post in a series
([part 1]({{< ref 2015-09-10-piano-heatmap-part-1 >}}),
[part 2]({{< ref 2020-07-19-piano-heatmap-part-2 >}})) on exploring what keys
of a piano I use the most. 

<!--more-->

I'm a sucker for data. Doesn't really matter about what---lately, election
polling has been interesting to watch---but I really like seeing numbers about
things I do. Music is one interesting thing, and I like that I can see
[my stats on last.fm](https://www.last.fm/user/chandlerswift), or the annual
email from Spotify with my year in review. Whether it's using
[time-tracking software](https://xkcd.com/1690/) or using a fitness app to track
duration/pace/heart rate/etc when running or using GPS data and OBD sensors to
figure out what part of my commute burns the most gas[^not-yet], I really enjoy
being able to see changes even in fairly useless data. With that in mind, here's
an update on my attempt to keep track of the keys I play.

[^not-yet]: Unfortunately, this one was starting to bubble up to the top of my
    project list just as full COVID-19 stay-at-home measures started, so it
    hasn't borne any fruit yet. Someday!

We [left off]({{< ref 2020-07-19-piano-heatmap-part-2 >}}) with a page that
would keep track of keys played, but every time the page was reloaded (which
wasn't infrequent, given that Edge[^edge] crashed more than occasionally when
MIDI devices were added and removed) the data would be reset, so it was
difficult to keep a running total.

[^edge]: Since the laptop I'm using occasionally also needs to run
    [Hauptwerk](https://www.hauptwerk.com/), I'm kind of stuck running Windows.
    Now that Edge is Chromium-based, I don't have a strong need to install
    Firefox as a default browser, if all I'm doing is occasional browsing.

To mitigate this, I added support for saving data per-session. If Edge decides
to stop accepting MIDI data, I can simply save the session and restart the
browser. This uses [Dexie](https://dexie.org/) as an easy wrapper for IndexedDB,
and stores that data in the browser's storage[^local-only]. I added some options
to save the current play session, and a few extra page links:

![same page as last time, but now with buttons!](/images/piano-heatmap/new-buttons.png)

I can then see my per-day/per-session stats:

![summaries of my last few sessions](/images/piano-heatmap/session-summary.png)

This probably isn't the endgame for this project, but it's a nice move in the
direction of collecting more data. Like I said, I like data! And it's much
easier to do any kind of analysis later if I've already been collecting the data
than it would be if I wasn't already keeping track! Here's the aggregated total
of the first few days' collected data:

![key totals over the last few days](/images/piano-heatmap/all-time-stats.png)

[^local-only]: This does mean that you can't (easily?) sync your sessions across
    devices, nor share your data with anyone else. That said, it wouldn't be
    too difficult to automatically upload and share this data publicly, à la
    [WhatPulse](https://whatpulse.org/). I just haven't done that.

As usual, the [source](https://github.com/chandlerswift/piano-heatmap) and the
[application](https://chandlerswift.github.io/piano-heatmap/) are available to
view or modify!
