---
layout: post
title: Data mining my Spotify history
include_syntax_styles: yes
---

I have a few songs I listen to very frequently. Enough that I wonder, "Does the
amount I stream this song have a noticeable effect on the song's popularity?"
It turns out, yes, there are at least a handful of songs for which that is the
case.

First, the main findings:

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

Song | Listens/Total | Percentage of total
-----|-----------------------|------------------
[Nun komm, der Heiden Heiland, BWV 659](https://open.spotify.com/track/3iVaSPY04q6lm6yk1JZfw8) | 67/<1000[^spotify-thousand-song-minimum] | 6.700%
[Come To Mama](https://open.spotify.com/track/4X4f9s89oqRzA6cbG3Qqpm) | 73/1118 | 6.530%
[10 Pièces - Organ: Scherzo](https://open.spotify.com/track/2QJDUqE12goajiRvX2ZGA9) | 68/1156 | 5.882%
[Dandaya](https://open.spotify.com/track/2OD2twxgZDvzzZk0LBFcG0) | 83/1753 | 4.735%
[How Long Does It Take?](https://open.spotify.com/track/5nJdSukxjQT2GMRroy2T4t) | 44/<1000[^spotify-thousand-song-minimum] | 4.400%
[The Eye of the Hurricane](https://open.spotify.com/track/6HNfSCcXvcfzm8P0atsoYB) | 42/<1000[^spotify-thousand-song-minimum] | 4.200%

Neat! I have four (and possibly more[^spotify-thousand-song-minimum]
[^not-all-listening-on-lastfm]) songs for which I account for at least 4% of the
Spotify listens. Interestingly, none of these are among my [top played
tracks](https://www.last.fm/user/chandlerswift/library/tracks), some of which
have hundreds of plays.

That said, there are two ways to get a high listen percentage: have my personal
total be very high, or have the global total be very low. Given this, it's not
particularly surprising that a large number of the songs for which I have a high
listen percentage have a very low total number of listens.

[^not-all-listening-on-lastfm]: I only signed up for
    [last.fm](https://last.fm/user/chandlerswift) in 2017, so this won't account
    for any listening I did before then. Also, for a while, I'm not convinced
    the integration was very good, so I think a fair number of my listens got
    skipped for the first year.

[^spotify-thousand-song-minimum]: Spotify appears to not show listen counts for
    songs with fewer than 1000 plays. It's not impossible that some of the more
    obscure things I listen to (artists I know in person, or obscure organ
    recordings, likely) have only tens to hundreds of plays. However, unless I
    can find out otherwise, I'm considering them conservatively, as if each
    track without a count had exactly one thousand listens.

### Methodology

*The full source code I wrote and used is
[available on Github](https://github.com/chandlerswift/spotify-listen-percentage).*

I have my listening history mostly [recorded on
last.fm](https://last.fm/user/chandlerswift), and Spotify provides total listen
counts for songs, at least through their web client. Here's an abbreviated
runthrough of the code I used to find the data, ignoring most of the error
handling and boilerplate.

```python
#!/usr/bin/env python3

import pylast
import spotify.sync as spotify
```

Python has nice packages to do the heavy lifting here:
[pylast](https://github.com/pylast/pylast) for last.fm and
[spotify.py](https://github.com/mental32/spotify.py) for Spotify.

```python
lastfm_top_tracks = lastfm_client.get_user("chandlerswift").get_top_tracks(stream=True, limit=None)
```

First, we get a generator that returns (lazily -- no need to pull all 11000ish
of my listens in one go!) the tracks I've played the most frequently, in
descending order. (If you want to try this, note that `limit=None` does require
[pylast/pylast#367](https://github.com/pylast/pylast/pull/367) to be merged.)

```python
track_data=[]
for i, lastfm_track in enumerate(lastfm_top_tracks):
    spotify_track = spotify_client.search(
        f"{lastfm_track.item.artist.name} {lastfm_track.item.title}", types=["track"], limit=1
    ).tracks[0]
```

Then, for each track we've retrieved from last.fm, we find its corresponding
track on Spotify. This can be issue-prone; tracks don't necessarily have
identical names between services, and often the same artist will have the same
track across many albums. Apparently last.fm considers these to be the same,
while Spotify counts them differently. Despite these problems, this generally
seemed to work well.

```python
    res = requests.get(f"http://localhost:8080/albumPlayCount?albumid={spotify_track.album.id}").json()
```

Here's some magic! It turns out [Spotify doesn't provide a
way](https://github.com/spotify/web-api/issues/70) to retrieve play count
information from their API, so we have to use a third party tool. (I could
likely have figured out what calls this tool makes, exactly, and integrated it,
but that seemed more complex than integrating an extra tool into a one-off
workflow.) I downloaded a .jar file from
[sp-playcount-librespot](https://github.com/evilarceus/sp-playcount-librespot)'s
[latest release](https://github.com/evilarceus/sp-playcount-librespot/releases/tag/v1.4),
ran it, and directed my API requests there.

```python
    found_track = None
    for spotify_disc in res['data']['discs']:
        for spotify_track_info in spotify_disc['tracks']:
            if spotify_track_info['name'].lower() == lastfm_track.item.title.lower():
                found_track = spotify_track_info
```

We end up having to extract the Spotify track from that album, since it doesn't
seem to be possible to get data for an individual track from
`sp-playcount-librespot`. This naïve comparison did have some issues, but for
the most part it worked fairly well.

```python
    if found_track:
        found_track['my_playcount'] = lastfm_track.weight
        track_data.append(found_track)
        print(f"{i}. {found_track['name']}: {found_track['my_playcount']}/{found_track['playcount']} ({100*found_track['my_playcount']/found_track['playcount']:.3f}%)")
    else:
        find_manually.append(lastfm_track)
        print(f"No track {lastfm_track.item.title} found on album {spotify_track.album.name} (will find later)")
```

To each track, we tack on its "weight" (play count) from last.fm, and save it
for later. We do a note of songs that we couldn't find on the album---I'll clean
those up later. In the end, I wound up effectively running through this whole
process again on the initially failed tracks, with a manual track comparison
instead of an automatic one.

### Data/Analysis

At this point, we're done gathering the data; let's see what we have from it.
I ran the script with `ipython -i main.py`, so when I was done, it just dropped
me into an `ipython` shell to manipulate the data as I wanted. I sorted it by
percentages, and printed them out in the format used to generate the table at
the beginning of the article:

```python
track_data.sort(key=lambda track: track['my_playcount']/max(track['playcount'], 1000), reverse=True)
for i, track in enumerate(track_data[:50]):
    print(f"[{track['name']}](https://open.spotify.com/track/{track['uri'].split(':')[2]}) | {track['my_playcount']}/{track['playcount'] if track['playcount'] > 0 else '<1000'} | {track['my_playcount']/max(track['playcount'], 1000)*100:.3f}%")
```
```
[Nun komm, der Heiden Heiland, BWV 659](https://open.spotify.com/track/3iVaSPY04q6lm6yk1JZfw8) | 67/<1000 | 6.700%
[Come To Mama](https://open.spotify.com/track/4X4f9s89oqRzA6cbG3Qqpm) | 73/1118 | 6.530%
[10 Pièces - Organ: Scherzo](https://open.spotify.com/track/2QJDUqE12goajiRvX2ZGA9) | 68/1156 | 5.882%
[Dandaya](https://open.spotify.com/track/2OD2twxgZDvzzZk0LBFcG0) | 83/1753 | 4.735%
[How Long Does It Take?](https://open.spotify.com/track/5nJdSukxjQT2GMRroy2T4t) | 44/<1000 | 4.400%
[The Eye of the Hurricane](https://open.spotify.com/track/6HNfSCcXvcfzm8P0atsoYB) | 42/<1000 | 4.200%
[It's A Shame, It's A Mystery](https://open.spotify.com/track/3b92Si6WeUY3AtgIdIauIC) | 63/1757 | 3.586%
[Behind My Back](https://open.spotify.com/track/2HajmdZaKcSGjVVwkbDD7n) | 36/1095 | 3.288%
[Lucky Southern (Live)](https://open.spotify.com/track/35bMR4tsBzexE4sbfQ7iHW) | 27/<1000 | 2.700%
[Pussy Cat Moan](https://open.spotify.com/track/1trxN9IV3zuKKm8DwLq6MS) | 80/3103 | 2.578%
[You're Nobody 'Til Somebody Loves You](https://open.spotify.com/track/579seIobCvjKFMA5iWVzIZ) | 24/<1000 | 2.400%
[Imagine](https://open.spotify.com/track/4llK1G7gFgs9Of6TeblOU6) | 29/1351 | 2.147%
[Come Along and Join Me](https://open.spotify.com/track/3AlEiVaGtg9juGSdHhe20T) | 20/<1000 | 2.000%
[Sweet Inspirations](https://open.spotify.com/track/3ev9yqA7eEQlj5YX6Dkxj4) | 23/1175 | 1.957%
[Soul Shine](https://open.spotify.com/track/3ps0pyaq8qIS6S01cWhZ0l) | 57/2954 | 1.930%
[How High the Moon](https://open.spotify.com/track/5Lwk2DGagiaJ91HzKPcxjQ) | 18/<1000 | 1.800%
[I'm Happy With Me](https://open.spotify.com/track/3ZJ21R1Hj5CgqpWdEVpCpq) | 18/<1000 | 1.800%
[I Want To Be Happy](https://open.spotify.com/track/5c6OtW2SbbQQAAmIX9tZhk) | 18/<1000 | 1.800%
[I Don't Want To Hurt You Baby](https://open.spotify.com/track/31EyidBsi5nOeIKDXnUpaF) | 52/3042 | 1.709%
[You Gotta Move](https://open.spotify.com/track/1FRly0ajiFsnhDfI55hqu9) | 54/3374 | 1.600%
[To Dream The Impossible Dream](https://open.spotify.com/track/5U0NztxEG065s4p2eKJl6K) | 15/<1000 | 1.500%
[Mannenberg - Pts. 1 & II (Feat. Sons of Table Mountain)](https://open.spotify.com/track/7afjyhiW4mtBJnoLuXYO9I) | 37/2471 | 1.497%
[Jump Blues Jam Track in D_160 bpm](https://open.spotify.com/track/6VmbBxl8RIZQebBbM1NT7C) | 38/2670 | 1.423%
[You'll Never Walk Alone](https://open.spotify.com/track/05CePy9cYchqsf8HVmzrt7) | 18/1267 | 1.421%
[All Things Are Possible](https://open.spotify.com/track/2zpnKFy41KROv5AEAAtoAX) | 14/<1000 | 1.400%
[Gospel Beat](https://open.spotify.com/track/3xjdt4l1W7L8iVc1PkjMI8) | 14/<1000 | 1.400%
[Business is Tough (in Db)](https://open.spotify.com/track/0Cx1kdVuhZzD0zxrhpVwoc) | 183/13218 | 1.384%
[Schefel](https://open.spotify.com/track/72Wn6cgsupR0shGI70bCZ3) | 14/1047 | 1.337%
[If I Only Had a Brain](https://open.spotify.com/track/2ABlZfY0YhluHszFZzwzat) | 37/2792 | 1.325%
[Milestones](https://open.spotify.com/track/6qRngToVR7MQKjO4zh1ZV0) | 13/<1000 | 1.300%
[Let It Be](https://open.spotify.com/track/4LecnEWdIg6ZgQBUZjVBFJ) | 17/1338 | 1.271%
[Centerpiece](https://open.spotify.com/track/19baWZcpp71fvy6zJlzCZi) | 20/1590 | 1.258%
[Hero](https://open.spotify.com/track/4RRMcdtPxLJyUFGCRbGi3l) | 11/<1000 | 1.100%
[Why Did You Leave My Child?](https://open.spotify.com/track/7nHXsKpgWz7zSwG2cb8toD) | 11/<1000 | 1.100%
[A Chance To Breathe](https://open.spotify.com/track/6rEzSUOZiRr9AOiDXy2kRM) | 45/4325 | 1.040%
[Live In The Spirit](https://open.spotify.com/track/4f7rI4Su9pYkmFO94kq43d) | 10/<1000 | 1.000%
[Jesus, Oh What a Wonderful Child (In the Style of Mariah Carey) [Karaoke Version]](https://open.spotify.com/track/5RT29wO0uGJzUYm7tTmFrX) | 23/2407 | 0.956%
[Songs of Praise Toccata for Organ](https://open.spotify.com/track/4gx4oXLSZJ0qpCzZmzprIf) | 26/2829 | 0.919%
[Bye Bye Blackbird](https://open.spotify.com/track/7xCnMzJzNuPlU0ynd6u4An) | 9/<1000 | 0.900%
[Leave the Door Open](https://open.spotify.com/track/2FG2bGSmK2al4ZbMzxUw8m) | 28/3226 | 0.868%
[I Wish](https://open.spotify.com/track/5YtgljxatdsJNbVkus464N) | 17/2041 | 0.833%
[The Walking Wounded](https://open.spotify.com/track/43uFShzMWIOnJzqq9MoYLH) | 26/3175 | 0.819%
[Suite brève: IV. Dialogue sur les mixtures](https://open.spotify.com/track/0Y4cwqqIcvzcKSQsNhjkqf) | 8/<1000 | 0.800%
[It Had To Be You](https://open.spotify.com/track/6cSIcX545GS9kjxUrF9eW2) | 8/<1000 | 0.800%
[Atlanta Blue](https://open.spotify.com/track/3VZCyBekMReptNB5cwPLmp) | 8/<1000 | 0.800%
[I'm A Woman](https://open.spotify.com/track/2knT9LjDV2M8wgp2zAhHeM) | 34/4500 | 0.756%
[Honey It's Your Fault](https://open.spotify.com/track/3vfyT1JduiIdezBcG30ypL) | 28/3862 | 0.725%
[Bathtub Blues](https://open.spotify.com/track/2X0W1IZBy92uAYb91j510D) | 7/<1000 | 0.700%
[Cookin' At The Colonels](https://open.spotify.com/track/13wUXxTzGk939tcE80Al2w) | 7/<1000 | 0.700%
[Let's Have a Natural Ball](https://open.spotify.com/track/5om3jWnIwPyXtHygKVsUsI) | 7/<1000 | 0.700%
```

A few more questions: Of the songs I've listened to at least 5 times, how many
have <1000 listens?
```python
[f"{i}. {t['name']} by {', '.join([a['name'] for a in t['artists']])}" for i, t in enumerate(list(filter(lambda track: track['playcount'] == 0, track_data)))]
```
```
['0. Nun komm, der Heiden Heiland, BWV 659 by Johann Sebastian Bach, Matti Hannula',
 '1. How Long Does It Take? by Sista Monica Parker',
 '2. The Eye of the Hurricane by D Squared',
 '3. Lucky Southern (Live) by Thirteen Degrees',
 "4. You're Nobody 'Til Somebody Loves You by Swingin' Fireballs",
 '5. Come Along and Join Me by The Chancellors Quartet',
 '6. How High the Moon by Les DeMerle, Bonnie Eisele',
 "7. I'm Happy With Me by Sista Monica Parker",
 '8. I Want To Be Happy by The Carl Fontana - Arno Marsh Quintet',
 '9. To Dream The Impossible Dream by Sista Monica Parker',
 '10. All Things Are Possible by Sista Monica Parker',
 '11. Gospel Beat by Sista Monica Parker',
 '12. Milestones by The Carl Fontana - Arno Marsh Quintet',
 '13. Hero by Sista Monica Parker',
 '14. Why Did You Leave My Child? by Sista Monica Parker',
 '15. Live In The Spirit by Sista Monica Parker',
 '16. Bye Bye Blackbird by The Carl Fontana - Arno Marsh Quintet',
 '17. Suite brève: IV. Dialogue sur les mixtures by Jean Langlais, John Balka',
 '18. It Had To Be You by The Carl Fontana - Arno Marsh Quintet',
 '19. Atlanta Blue by Bill Walker, The Bill Walker Orchestra',
 '20. Bathtub Blues by Joe Scruggs',
 "21. Cookin' At The Colonels by Steve Einerson",
 "22. Let's Have a Natural Ball by The Blue In Blues",
 '23. Now the Green Blade Rises (arr. P. Manz for pipe organ) by J. M. C. Crum, Paul Manz',
 '24. Too Many Drivers at the Wheel by AJ Crawdaddy',
 '25. Singet frisch und wohlgemut op. 12,4 - II. by Hugo Distler, MonteverdiChor Muenchen, Konrad von Abel',
 '26. Peas Porridge Hot by Joe Scruggs',
 '27. Organ Symphony No. 1 in D Major, Op. 14: VI. Final by Louis Vierne, Fabien Chavrot',
 '28. Old Devil Moon by Michael Gott',
 "29. It's a Beautiful Day in the Neighborhood by Rich Szabo, Curtis McKonly, Mark Vinci, Bill Kirschner",
 '30. Dr. Mlk & Obama Impossible Dream Tribute by Sista Monica Parker',
 '31. Old Devil Moon by Michael Gott']
```

Only 32 of the 1989 tracks we're inspecting; sounds like my tastes aren't _too_
obscure!

Spotify gives me the length of each song. What songs have I listened for the
longest total time?

```python
import datetime

track_data.sort(key=lambda track: track['my_playcount'] * track['duration'], reverse=True)
for i, track in enumerate(track_data[:10]):
    print(f"{i}. {track['name']}: {track['my_playcount']} listens at {datetime.timedelta(seconds=round(track['duration']/1000))}: {datetime.timedelta(seconds=round(track['my_playcount'] * track['duration'] / 1000))}")
```
```
0. You Look Good To Me: 690 listens at 0:04:52: 2 days, 7:58:46
1. Lucky Southern: 649 listens at 0:03:46: 1 day, 16:45:00
2. Change the World: 569 listens at 0:03:55 seco: 1 day, 13:07:19
3. Strasbourg / St. Denis: 473 listens at 0:04:39: 1 day, 12:36:30
4. Rock of Ages: 306 listens at 0:05:28: 1 day, 3:52:58
5. At Long Last Love - Live: 282 listens at 0:04:56: 23:12:39
6. Sultans of Swing: 229 listens at 0:05:50: 22:17:22
7. Mo' Better Blues (feat. Terence Blanchard): 281 listens at 0:03:39: 17:05:31
8. Here We Go Again: 231 listens at 0:03:58: 15:16:18
9. Love Me or Leave Me - 2013 Remastered Version: 270 listens at 0:03:21: 15:06:15
```
It looks like this list is still roughly in order of listen count, as one might
expect. Most songs tend to be around the same length, so it makes sense that it
wouldn't be wildly different from the most-listened-to song list.

I did limit the script run to songs with at least 5 plays; however, a song with
only 4 plays would need to be almost 4 hours long to make this list, so I think
it's safe to ignore those.

### Potential improvements
A solution to many of the issues I've been having would be to use Spotify's data
on my listening history rather than last.fm's.

 * Because I'd be correlating Spotify's data with Spotify's data, I wouldn't
   have to worry about track title mismatches (the most notable being "¿Quién
   Será?" vs "Quien Sera?"; the most common being "[track title]" vs "[track
   title] - Remastered 20xx"). In this case, I could simply match the internal
   Spotify IDs (if that's something their data dumps do actually provide).
 * Spotify should have my complete, precise listening history, compared to
   last.fm which only has the last few years' worth.
 * Since I'm using Spotify's search, rather than selecting a track by ID,
   occasionally I receive an obscure track on a weird album that isn't what I'm
   looking for.

I _did_ want to base this analysis on Spotify's data, but I wasn't particularly
patient, and Spotify seems to try to barely scrape under GPDR's 30-day deadline
for delivering data exports.

And finally, this isn't an improvement, but worth mentioning: While reading
through Spotify's API docs, I found that they [expose an Audio Analysis for a
Track](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-audio-analysis)
(if the link doesn't take you there, reload or search the page for "Get Audio
Analysis for a Track" -- anchors don't always seem to work on the first page
load), which includes information like time and key signature! This is probably
enough data that I'd be able to write the music player feature of which I've
long been dreaming: Create playlists with no key changes between songs!


<details markdown="1">
<summary>Oh man, let me tell you all about it!</summary>
Any song has a starting key signature and an ending key signature. For many
songs, these are the same. Those are the easy ones. Start with a song in the key
of D, say, and play more songs in the key of D. Here's an example from the last
time I seriously thought about this:

<iframe src="https://open.spotify.com/embed/playlist/3NvR4Y9nq4QATw0lLzN9JR" height="380" style="width:min(100%, max(400px, 75%)); display: block; margin: auto;" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>

The hard part comes in when songs have one or more modulations (changes in
key signature, essentially) in the middle. As a relatively quick example, you
could run through the following songs:

Track | Artist | Album | Start Key | End Key
------|--------|-------|-----------|--------
[This Will Be (An Everlasting Love)](https://open.spotify.com/track/0PDCewmZCp0P5s00bptcdd?si=ee7e8847eca5489b) | Natalie Cole | Inseparable | B&#9837; | D&#9837;
[I Just Called To Say I Love You - Live/1995](https://open.spotify.com/track/2g9gfrERaKzRCIV1UQX12w?si=78ed86ebdb2c4b02) | Stevie Wonder | The Complete Stevie Wonder | D&#9837; | E&#9837;
[You're Nobody 'Til Somebody Loves You](https://open.spotify.com/track/579seIobCvjKFMA5iWVzIZ?si=a230f5e7521041a3) | Swingin' Fireballs | Live in Bremen | E&#9837; | G
[Beyond the Sea (La Mer)](https://open.spotify.com/track/6XMn6IKd4WPfBclWsxWe2q?si=430137f139f24946) | George Benson | 20/20 | G | A&#9837;
[My Buick, My Love and I - Bonus Track](https://open.spotify.com/track/1GYCBJuUZGeLtEYuerS2fG?si=9894c61f414e4fff) | Seth MacFarlane, Elizabeth Gillies | In Full Swing | A&#9837; | F
[The Liberty Bell March](https://open.spotify.com/track/0ipIyLG8vbqqxr0ZOL8oUe?si=329a294187764723) | John Philip Sousa | Last Night of the Proms | F | B&#9837;

Each one begins in the key the other left off in, creating what is (for me) a
relatively seamless listening experience! I had abandoned this project years ago
when I figured I'd have to manually classify every song I wanted to listen to,
but if Spotify will do do it for me...problem succesfully avoided!

My ideal listening client, then, would be an improvement on the standard
"shuffle" functionality. Instead of picking songs completely at random, it would
pick song `n+1` from the set of songs that begin in the same key that the
song `n` ended in.

<!-- Other contenders: 
High School Never Ends Bowling for Soup - A->B
It's a Small World Nikki Y (disney jazz) - F-> G
Man in the Mirror - G->Ab (kinda, ends with a strong IV, not a good candidate)
From this Moment on G -> B

A shorter example would be Beyond the Sea -> My Buick My Love and I -> It's a
small world, but it's all swing -- how dull is that!

This will Be (An everlasting love) Bb -> Db
I just Called to say I love you Db -> Eb
Nobody til somebody loves you Eb->G
Beyond the Sea George Benson G->Ab
My Buick my Love and I - Ab -> F
The Liberty Bell March F->Bb

For once in my life F -> F#
The Washington Post March G->C
-->

<iframe src="https://open.spotify.com/embed/playlist/2jfVngq0cEwcfK5MIL2n85" height="380" style="width:min(100%, max(400px, 75%)); display: block; margin: auto;" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>

</details>
