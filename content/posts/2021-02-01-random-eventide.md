---
layout: post
title: A random accompaniment on EVENTIDE
IncludeSyntaxStyles: yes
---

How good can we make a random accompaniment sound? I was playing with
[EVENTIDE](https://hymnary.org/tune/eventide_monk),
William Henry Monk's tune written for
[Abide with Me](https://en.wikipedia.org/wiki/Abide_with_Me), and was pondering
this. I was trying to play randomly on the piano from octaves and notes in the
scale, but suspected my "randomess" of playing wasn't particularly good. But
what _does_ have good randomness? Python! (If you don't want to read the code,
just [check out the results at the bottom]({% post_url 2021-02-01-random-eventide %}#results).)

```python
#!/usr/bin/python

# pip install pymusicxml
# https://pypi.org/project/pymusicxml/
# https://git.sr.ht/~marcevanstein/pymusicxml
from pymusicxml import *
from random import choice

score = Score(title="EVENTIDE", composer="Chandler Swift")
accompaniment = Part("Piano")

### GENERATE ACCOMPANIMENT:

# First, we do some boilerplate. We generate the note names and octaves to be
# used later in the program. This section generates the 88 keys on a piano,
# with a result like ["a0", "bb0", "b0", "c1", "db1", ... "bb7", "b7", "c8"]
note_names = ["c", "db", "d", "eb", "e", "f", "gb", "g", "ab", "a", "bb", "b"]
notes_with_octaves = ["a0", "bb0", "b0"]
for octave in range(1,8):
    for note in note_names:
        notes_with_octaves.append(note + str(octave))
notes_with_octaves.append("c8")


# to save some writing later, scales are major, minor, or dominant sevenths.
# I could have just written out "major" or "minor" everywhere, but simply being
# able to write `M` saves a fair number of quotes typed!
#
# Abide with me does have some slightly more complex chords than these three,
# but we can get nearly there with these. The biggest thing that I miss having
# is probably the nice Csus2/E that we have in the second bar and elsewhere.
M="major"
m="minor"
dom7="dominant seventh"

# Now let's write out the notes. A C major scale is C D E F G A B; offsets from
# the starting C of 0, 2, 4, 5, 7, 9, and 11 notes. The others are similar.
#
# After some playing around, I think I like the melodic minor best, but I'm
# still not sure. If we wanted, we could simplify any of these; perhaps omitting
# a 7 altogether from the major scale would be nice; for example, in the second
# chord in the first measure (assuming key of C, for simplicity), we really
# don't want an F# (the major seventh of the V chord, G). We could switch all
# of our V chords to V7 chords, and then at least we have F naturals instead of
# F sharps, but I was happy enough with the result here to let it be.
scales={
    M: [0,2,4,5,7,9], # M2, M3, P4, P5, M6
    m: [0,2,3,5,7,10], # M2, m3, P4, P5, m7
    dom7: [0,2,4,5,7,9,10]
}

# Here are the changes for the tune. Each tuple has the chord root (c, d, f, g, 
# and a, here), the chord type (major, minor, or dominant seventh), and the
# (whole) number of beats for which that chord is played. Hey, it's the world's
# lousiest lead sheet!
changes=[
    # simplified, and transposed to C so I don't have to deal with accidentals
    # see also e.g. https://hymnary.org/page/fetch/LUYH2013/504/low
    ("c", M, 2),
    ("g", dom7, 2),
    ("a", m, 4),
    # ^ 2, Csus2/E 2
    ("f", M, 2),
    ("g", dom7, 2),
    ("c", M, 4),
    ("c", M, 4),
    ("f", M, 2),
    ("c", M, 2),
    ("d", m, 2),
    ("d", dom7, 2),
    ("g", M, 2),
    ("g", dom7, 2),
    ("c", M, 2),
    ("g", dom7, 2),
    ("a", m, 4),
    # ^ 2, Eb/G 2
    ("f", M, 2),
    ("a", dom7, 2),
    ("d", m, 4),
    ("g", dom7, 4),
    ("c", M, 1),
    ("g", M, 1),
    ("a", m, 1),
    ("f", M, 1),
    ("g", M, 2),
    ("g", dom7, 2),
    ("c", M, 4),
    # TODO: intro/outro
]

# We randomly generate an array of notes to be added to the score. So that we
# don't have to keep track of the measures, and since the notes are all the same
# duration, we just generate them all at once, and then slot 4*NOTES_PER_BEAT of
# them into each measure at the end.
notes = []

BEATS_PER_MINUTE=80
NOTES_PER_BEAT=4
for chord in changes:
    chord_root, chord_type, beats = chord

    # Play the root of the chord
    tonic = chord_root + "3" # start in the third octave
    notes.append(Note(tonic, 1/NOTES_PER_BEAT, directions=StartPedal()))
    notes_left = beats * NOTES_PER_BEAT - 1

    # If the chord is held for longer than a beat, add a fifth in the bass. We
    # do this check specifically for the second measure of the last phrase,
    # which has four chords each held for one beat. If we added both the tonic
    # and fifth to each of those, we wouldn't have room for any random notes.
    if beats > 1:
        # add a major fifth above the tonic
        fifth = notes_with_octaves[notes_with_octaves.index(tonic) + 7]
        notes.append(Note(fifth, 1/NOTES_PER_BEAT))
        notes_left -= 1

    # fill the rest with random notes from the top end of the piano.
    while notes_left:
        interval = choice(scales[chord_type])
        octave = choice([4,5,6,7,8]) # Notes will be in the range of C4 to C8
        note = note_names[(note_names.index(chord_root) + interval) % len(note_names)]
        note_with_octave = note + str(octave)
        if note_with_octave in notes_with_octaves:
            #print(f"from {chord_root} {chord_type}, picked interval {interval}"
            #       "octave {octave} so note {note_with_octave}")
            directions=StopPedal() if notes_left == 1 else () # unpedal at the end of the chord
            notes.append(Note(note_with_octave, 1/NOTES_PER_BEAT, directions=directions))
            notes_left -= 1

# Now take those notes and break them up into measures
measures = []
first_measure = True
while len(notes) > 0:
    if first_measure:
        measure = Measure(
            time_signature=(4,4),
            directions_with_displacements=[(MetronomeMark(1.0, BEATS_PER_MINUTE), 0)]
        )
        first_measure = False
    else:
        measure = Measure()
    measure.extend(notes[:NOTES_PER_BEAT*4])
    notes = notes[NOTES_PER_BEAT*4:]
    measures.append(measure)

# and tack those measures onto the score.
accompaniment.extend(measures)


### ADD VOICE PART, FOR REFERENCE

# This bit adds the melody line to EVENTIDE. Mostly busy work, I debated not
# even including it.

voice = Part("Voice")

# I took a long time to convince myself that it wasn't worth it to reimplement
# lilypond to make this section work. We're like 80% of the way there, but the
# pareto principle suggests that it's still not worth it to get that last 20%.
voice_notes="""
e4 2 e4 1 d4 1 c4 2 g4 2 a4 1 g4 1 g4 1 f4 1 e4 4
e4 2 f4 1 g4 1 a4 2 g4 2 f4 1 d4 1 e4 1 f#4 1 g4 4
e4 2 e4 1 d4 1 c4 2 g4 2 g4 1 f4 1 f4 1 e4 1 d4 4
d4 2 e4 1 f4 1 e4 1 d4 1 c4 1 f4 1 e4 2 d4 2 c4 4
"""
voice_notes = voice_notes.split()
# https://stackoverflow.com/a/15480540/3814663
voice_notes = list(zip(voice_notes[::2], voice_notes[1::2]))
# [('g4', '2'), ('g4', '1'), ('f4', '1'), ('eb4', '2'), ...]

current_measure = Measure(time_signature=(4,4))
beats_through_current_measure = 0
measures = []
for note, duration in voice_notes: # this only works because no notes are held through bar lines
    duration = int(duration)
    current_measure.append(Note(note, duration))
    beats_through_current_measure += duration
    if beats_through_current_measure == 4: # should never be greater than four, see above.
        # new measure
        measures.append(current_measure)
        current_measure = Measure()
        beats_through_current_measure = 0
voice.extend(measures)

score.append(PartGroup([voice, accompaniment]))
score.export_to_file("Eventide.xml")
```
The code above is built off the
[pymusicxml](https://git.sr.ht/~marcevanstein/pymusicxml) python library, and
is therefore licensed under the [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html).

If you want to run it yourself, here's my Makefile:
<details>
<summary><code>Makefile</code></summary>
{% highlight make %}
Eventide.xml:
	python eventide.py

Eventide.pdf: Eventide.xml
	musescore Eventide.xml -o Eventide.pdf

Eventide.mp3: Eventide.xml
	musescore Eventide.xml -o Eventide.mp3

Eventide.mscz: Eventide.xml
	musescore Eventide.xml -o Eventide.mscz

.PHONY: clean
clean:
	rm -f Eventide.xml Eventide.mp3 Eventide.pdf Eventide.mscz

all: Eventide.pdf Eventide.mp3 Eventide.mscz
{% endhighlight %}
</details>

### Results
Here's one sample of the output. (This isn't hand-picked from lots of results;
it's the result of the first complete run of the program.) You can view it
[on Musescore's community site](https://musescore.com/user/81342/scores/6588039/s/FdPG3I)
(embedded below), or download the
[MusicXML file](/images/random-eventide/Eventide.xml),
[Musescore file](/images/random-eventide/Eventide.mscz),
[PDF](/images/random-eventide/Eventide.pdf),
or [MP3](/images/random-eventide/Eventide.mp3).

<iframe width="100%" height="394" src="https://musescore.com/user/81342/scores/6588039/embed" frameborder="0" allowfullscreen allow="autoplay; fullscreen"></iframe>

Bonus: While looking up information about EVENTIDE, I found that the Thelonious
Monk Septet has a recording of Abide with Me!
<iframe src="https://open.spotify.com/embed/track/2QradSkPvUearyo5Z4tVRk" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>

Edited 2021-02-09 to add -- Bonus bonus: What's almost as random as
`random.choice()`? Chickens! (Thanks Jeff!)
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/WFxDOV6IwHk" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
