---
layout: post
title: Keeping Tabs on my Tabs &ndash; a quick Python hack
IncludeSyntaxStyles: true
excerpt: I'm a bit of a tab hoarder. Firefox, thankfully, is pretty good about
    not using excessive resources for infrequently-accessed tabs, but when my
    <a href="https://addons.mozilla.org/en-US/firefox/addon/tab-counter-webext/">Tab Counter extension</a>
    told me I'd topped 300 tabs, I figured it was time to start a more serious
    diet plan. And what's a diet without a scale? Here's a script that I use to
    keep track of how many tabs I have open at a time, so I can measure my
    progress in the fight against my hoarding instincts.
---

I'm a bit of a tab hoarder. Firefox, thankfully, is pretty good about not using
excessive resources for infrequently-accessed tabs, but when my
[Tab Counter extension](https://addons.mozilla.org/en-US/firefox/addon/tab-counter-webext/)
told me I'd topped 300 tabs, I figured it was time to start a more serious diet
plan. And what's a diet without a scale? Here's a script that I use to keep
track of how many tabs I have open at a time, so I can measure my progress in
the fight against my hoarding instincts.[^instincts]

[^instincts]: Generally, my usage consists of opening a bunch of tabs for a
    project, and closing them when I finish the project. This wouldn't be that
    big of a deal, considering that a good project is generally in the 20-30
    active tab range (generally consisting of documentation I'll want to refer
    back to, obscure forum threads where [DenverCoder9](https://xkcd.com/979/)
    mentioned my issue, API references, and of course some Stack Overflow tabs).
    However, this becomes a lot more of a problem when I'm swapping back and
    forth between several large projects, where I have a window for each.
    Currently, that list is:

     * DTANM - adding automated testing
     * Debugging screensharing on Wayland using Pipewire
     * Writing bare-metal Risc-V assembly
     * Fixing up an old super-tic-tac-toe server for better multiplayer
     * Finishing the Gallery app for AsteroidOS
     * Interfacing with MIDI instruments in Rust

    as well as a handful of smaller projects. One hope here is that this will
    be a nice kick in the pants to finish up some of those projects that have
    been sitting on the back burner for months.

Firefox[^currently] saves a `sessionstore` file that contains information about
your windows and tabs. Unfortunately, that seems to be only saved when the
browser is closed. However, Firefox also saves[^frequently] a
`$FIREFOX_PROFILE/sessionstore-backups/recovery.jsonlz4` with current data. This
is the file I used. `file` tells us that `.jsonlz4` is "Mozilla lz4
compressed data" -- apparently they're using a vaguely custom compression scheme
to store this data. I didn't have any luck stripping the header and
decompressing it with the standalone `lz4` tool, but Python proved workable.
Once I have the data, parsing it is fairly straightforward. I wound up running
the script once a day on a cronjob, frequently enough to give me that little
extra prod to close my tabs, and one day in...I've closed almost 30!

[^currently]: I'm not looking forward to the day when this changes and it breaks
    everything that relies on this partially-undocumented feature.

[^frequently]: It seems to save this file at least once a minute. I didn't
    really care if it was once a minute or once an hour, since my script runs
    daily; I just didn't want it to be "whenever you close your browser"!

```python
#!/usr/bin/env python
import lz4.block as lz4
import json
from datetime import date, timedelta
import urllib.parse
import shutil

RECOVERY_FILE="/home/chandler/.mozilla/firefox/cu3gxbtx.default-release/sessionstore-backups/recovery.jsonlz4"

today=date.today().isoformat()
# Take a snapshot of today's file
shutil.copy(RECOVERY_FILE, f"recovery-{today}.jsonlz4")

with open(f"recovery-{today}.jsonlz4", 'rb') as f:
    assert f.read(8) == b'mozLz40\0'
    today_data=json.loads(lz4.decompress(f.read()))

yesterday=(date.today() - timedelta(days=1)).isoformat()
with open(f"recovery-{yesterday}.jsonlz4", 'rb') as f:
    assert f.read(8) == b'mozLz40\0'
    yesterday_data=json.loads(lz4.decompress(f.read()))

def count_total_tabs(data):
    return sum([len(window['tabs']) for window in data['windows']])

# This is a unique tab identifier. However, it's not consistent, it seems to
# change when a tab is unloaded and reloaded (suspended?)
IDENTIFIER="docshellUUID"

def find_matching_tab(needle, haystack, remove_from_haystack=False):
    # If they have the same docshellUUID, they're definitely the same
    for tab in haystack:
        if tab['entries'][-1][IDENTIFIER] == needle['entries'][-1][IDENTIFIER]:
            if remove_from_haystack:
                haystack.remove(tab)
            return tab
    # If they have the same URL they're probably the same
    for tab in haystack:
        if tab['entries'][-1]['url'] == needle['entries'][-1]['url']:
            if remove_from_haystack:
                haystack.remove(tab)
            return tab
    # TODO: if they share history, they may be the same


def find_matching_window(needle, haystack, remove_from_haystack=False):
    leading_contender = None
    leading_contender_matches = 0
    leading_contender_percent = 0
    for potential_match in haystack:
        matches = 0
        for tab in needle['tabs']:
            if find_matching_tab(tab, potential_match['tabs']) is not None:
                matches += 1

        match_percent = matches / len(needle['tabs'])
        if (matches > leading_contender_matches or match_percent > leading_contender_percent) and match_percent > .5:
            leading_contender = potential_match
            leading_contender_matches = matches
            leading_contender_percent = match_percent

    if remove_from_haystack:
        haystack.remove(leading_contender)
    return leading_contender

def format_tab(tab, leading_spaces=0):
    entry = tab['entries'][-1]
    title = entry['title']
    if len(title) > 50:
        title = title[:50] + "…"
    url = urllib.parse.urlsplit(entry['url'])
    return f"{' ' * leading_spaces}{title} ({url.netloc})"


# TODO: persist these data
# TODO: graph these data
print(f"Yesterday: {len(yesterday_data['windows'])} windows, {count_total_tabs(yesterday_data)} tabs.")
print(f"Today:     {len(today_data['windows'])} windows, {count_total_tabs(today_data)} tabs.")

net_closed_tabs = count_total_tabs(yesterday_data) - count_total_tabs(today_data)
if net_closed_tabs > 0:
    print(f"Congrats! You closed {net_closed_tabs} tabs!")
elif net_closed_tabs == 0:
    print(f"Good work. You didn't open any more tabs today.")
else:
    print(f"You opened {-net_closed_tabs} tabs. Dishonor on you! Dishonor on your cow!")

# TODO: tab entries have a lastAccessed field. Do some counting on that? (ms since epoch)

yesterday_windows = yesterday_data['windows'][:]
for i, window in enumerate(today_data['windows']):
    yesterday_window = find_matching_window(window, yesterday_windows, remove_from_haystack=True)
    if yesterday_window:
        print(f"Window {i} ({len(window['tabs'])} tabs)")
    else:
        print(f"Window {i} (NEW, {len(window['tabs'])} tabs)")

    tabs = window['tabs'][:]
    if yesterday_window:
        yesterday_tabs = yesterday_window['tabs'][:]
    else:
        yesterday_tabs = []

    opened_tabs = []
    changed_tabs = []

    for tab in tabs:
        yesterday_tab = find_matching_tab(tab, yesterday_tabs, remove_from_haystack=True)
        if yesterday_tab is None:
            opened_tabs.append(tab)
        elif yesterday_tab['entries'][-1]['url'] != tab['entries'][-1]['url']:
            changed_tabs.append(tab)

    if opened_tabs:
        print(f"  Opened ({len(opened_tabs)}): ")
        for tab in opened_tabs:
            print(format_tab(tab, 4))

    if yesterday_tabs:
        print(f"  Closed ({len(yesterday_tabs)}): ")
        for tab in yesterday_tabs:
            print(format_tab(tab, 4))

    if changed_tabs:
        print(f"  Changed ({len(changed_tabs)}): ")
        for tab in changed_tabs:
            print(format_tab(tab, 4))
    
    if not (opened_tabs or yesterday_tabs or changed_tabs):
        print("  (unchanged)")

for window in yesterday_windows:
    print(f"CLOSED: Window {i} ({len(window['tabs'])} tabs)")
    print(f"  Closed ({len(window['tabs'])}): ")
    for tab in window['tabs']:
        print(format_tab(tab, 4))
```

Potential enhancements that'll probably never come since this was just a quick
evening project to scratch an itch I had:
 * Clean up the code, Chandler!
 * Rather than snapshotting the (reasonably large) file each time, save the
   relevant bits to a database
 * Make the tab matching more robust. Currently if I'm visiting example.com
   and click a link to example.org, the script thinks I closed example.com and
   opened example.org. However, since I do have access to each tab's history, I
   could reasonably easily modify the script to process this correctly. I
   actually got something mostly working here, but stripped it out since it
   made the output logic a lot more complex.
 * Add a trendline for the n-day trend (alternatively, a streak--"You've closed
   as many tabs as you've opened for N days in a row!")
