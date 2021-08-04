---
title: (meta-)*tic-tac-toe
layout: post
excerpt: Tic-tac-toe in tic-tac-toe in tic-tac-toe&hellip;how deep can we go?
---

After a particularly interesting talk at UMD's math club, to fill some left-over
time, the speaker of the day introduced to us a game that was new to me:
[Meta Tic-Tac-Toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe)[^name]. After
a few games on the chalkboard, I was really interested, and spent a few weeks
asking anyone who would listen to play a game or three. I can't say I was ever
_good_ at it, but it was certainly fun!

[^name]: It was introduced as Super Tic-Tac-Toe, a name I tend to like better,
    but Meta* Tic-Tac-Toe seems to capture the recursive nature of what we're
    trying to do here more effectively.

If you haven't seen the rules,
[here's an overview](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/).
The gist is that you're playing on a tic-tac-toe grid full of tic-tac-toe grids,
and you must win three in a row. There's a twist to make it interesting, though:
The location of the previous play determines which grid the opponent plays on.
For example, an X in the top left corner of a grid means the opponent will next
have to play in the top left grid, and that move determines where you'll play
next.

```
     │ │  ┃  │ │  ┃  │ │      ?│?│? ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃  │ │ 
    ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─
     │ │  ┃  │ │  ┃  │ │      ?│?│? ┃  │ │  ┃  │ │       │ │o ┃  │ │  ┃  │ │ 
    ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─
     │ │  ┃  │ │  ┃  │ │      ?│?│? ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃  │ │ 
    ━━━━━━╋━━━━━━━╋━━━━━━━    ━━━━━━╋━━━━━━━╋━━━━━━━    ━━━━━━╋━━━━━━━╋━━━━━━━
     │ │  ┃ x│ │  ┃  │ │       │ │  ┃ x│ │  ┃  │ │       │ │  ┃ x│ │  ┃ ?│?│?
    ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─
     │ │  ┃  │ │  ┃  │ │   ->  │ │  ┃  │ │  ┃  │ │   ->  │ │  ┃  │ │  ┃ ?│?│?
    ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─
     │ │  ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃ ?│?│?
    ━━━━━━╋━━━━━━━╋━━━━━━━    ━━━━━━╋━━━━━━━╋━━━━━━━    ━━━━━━╋━━━━━━━╋━━━━━━━
     │ │  ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃  │ │ 
    ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─
     │ │  ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃  │ │ 
    ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─     ─┼─┼─ ┃ ─┼─┼─ ┃ ─┼─┼─
     │ │  ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃  │ │       │ │  ┃  │ │  ┃  │ │ 
```

If you haven't played, it's worth noting that moves near the beginning often
feel pretty random, and for me that's usually the case. I haven't worked out
much strategy for moves at the beginning, where they don't have much (obvious)
impact on later game state. Moves toward the end tend to have much more
immediate impact, and are usually where the bulk of my gameplay time is spent.

To make it easier to get other people (say, those not in the same room as me) to
play, I wrote [a server](https://github.com/ChandlerSwift/super-tic-tac-toe)
that supports playing games online. It was a nice weekend hack, though for a
variety of reasons not exactly production ready!

<style> code { font-size: 16px; } </style>
But here's the thing about nesting tic-tac-toe boards: Why only once? What if
we went deeper? Well, here's what we came up with for meta-meta-tic-tac-toe[^1]
[^no-rules]. It's played pretty much the same as meta-tic-tac-toe, with a few
rules clarifications. Like 2-deep tic-tac-toe, previous moves determine where
you're allowed to play. The conclusion we came to for 3-deep is that your
top-level board is that of the second-level board from last time, and the
second-level board is determined by which square was chosen last turn. More
generally, for `m`-nested boards[^nesting], your `n`th turn is played at
top-level board `n-m`, second level board `n-m-1`, ..., and the smallest board
at `n-1`. For example, here are the first few moves of a possible game:

![An animated start of a game](/images/meta-tic-tac-toe/gameplay.gif)

[^1]: or super-duper-tic-tac-toe, if you're so inclined.

[^nesting]: This does not counting the top level board; 0-nested is normal
    tic-tac-toe; 1-nested is 9 boards inside one larger board, etc.

[^no-rules]: I haven't been able to find any rules for how exactly the game is
    played, nor analysis on whether or not it's fair. But if there's any mention
    on the 'net that I missed, I'd be grateful to hear about it!

I find this confusing to reason about logically, but intuitively it makes
fairly decent sense; each turn you're progressively less affected by older
moves. For me, the lightbulb moment was when I realized that each move the area
a move is constrained to by an old move expands one board level. With that in
mind, I visualize an expanding board when I'm playing. Suppose I'm playing in
the yellow highlighted area below. Expanding the second-level board to cover the
top-level board gives an idea of where the next move will direct the players.
In this case, a move in the orange square will send one's opponent to the bottom
left sub-sub-grid of the middle right sub-grid.

![A visualization of meta-tic-tac-toe moves](/images/meta-tic-tac-toe/anim-1.svg)

This scales, too: The move after the next can be visualized by zooming out once
more. In this example, the next move will be in the bottom-left sub-sub-grid of
the center sub-grid, and the following move will be in the bottom-left sub-grid,
with a sub-sub-grid dependent on the location of the next move.

![A second visualization](/images/meta-tic-tac-toe/anim-2.svg)

Here are some more examples[^generated-with]:
<div style="display: flex; flex-wrap: wrap; justify-content: center;">
    <img alt="another visualiztion" width="360" src="/images/meta-tic-tac-toe/anim-3.svg">
    <img alt="another visualiztion" width="360" src="/images/meta-tic-tac-toe/anim-4.svg">
</div>

[^generated-with]: These examples were all generated using a short Python script
    [available here](https://github.com/ChandlerSwift/www/blob/master/images/meta-tic-tac-toe/generate.py).
    The script should support arbitrary nesting with maybe minor tweaks, but the
    SVG files get large pretty quickly!

    I had initially tried using Inkscape to generate these, but I had to do some
    manual editing of the SVG files, and Inkscape doesn't do a very nice job of
    outputting human-readable SVG. Between a surprisingly readable SVG spec and
    the wonder of modern technology that is
    [MDN's reference on the subject](https://developer.mozilla.org/en-US/docs/Web/SVG),
    it wound up being a pretty quick project. And arbitrary recursion is fun!

    Much of the logic was borrowed from an client I started trying to develop,
    which hopefully should support arbitrary nesting. When that's done, it'll
    probably show up [on GitHub](https://github.com/chandlerswift/sttt).

    To generate the images I've been using, you can simply
    ```
    ./generate.py -l 1 1,0 2,1 0,2 > anim-1.svg
    ./generate.py 1,0 2,1 0,2 > anim-2.svg
    ./generate.py 1,1 1,1 0,1 > anim-3.svg
    ./generate.py 2,0 0,2 2,0 > anim-4.svg
    ./generate.py -n 0,1 1,2 2,1 1,0 > too-meta-static.svg
    ./generate.py 0,1 1,2 2,1 1,0 > too-meta.svg
    ```

And, because why not, here's a four-deep example. I don't know how long exactly
this would take to play, but assuming you have to fill about half the spaces,
two players placing collectively one token per second would take almost an hour
to play. And I generally take >10 seconds a move! This can slow down a browser
a bit, so click the image, which is a link to the animated version.

[![meta-meta-meta-visualization](/images/meta-tic-tac-toe/too-meta-static.svg)](/images/meta-tic-tac-toe/too-meta.svg)

The other note, as compared to meta tic-tac-toe, is that when you're directed to
play on a bottom-level grid, you recursively escalate boards until you reach a
playable board. So if your opponent made a move sending you to a board that's
full, you can play anywhere on a second level board; if that's full, you can
play anywhere on a next-level board. These rules seem (mostly?) unavoidable, but
I haven't played enough games to work out if there are odd implications of this.

If anybody else has been playing by these (or different!) rulesets,
[let me know](mailto:chandler@chandlerswift.com)! I'd enjoy hearing about your
games, and whether or not you've liked the ruleset!

<div class="thanks">
    Thanks to Jeff and Isaac for reviewing a draft of this post.
</div>
