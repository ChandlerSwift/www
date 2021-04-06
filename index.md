---
layout: page
title: Home
regenerate: true
---

<h1>Chandler Swift</h1>
<p id="nav-links">
  <strong><a href="https://chandlerswift.com/">Home</a></strong> |
  <a href="https://home.chandlerswift.com/">Burnsville, MN</a>
</p>
<hr class="separator">

## About
I'm a lifelong hacker (the
[good kind](http://catb.org/~esr/jargon/html/H/hacker.html)!). My parents
have a story they like to tell at my expense: At just a few years old, I was
interested enough in my Dad's laptop brought home from work one evening to
somehow manage to change the operating system language into German. Of course,
I vehemently deny everything. The interest in computers has stayed, though I
like to think I require a bit less supervision now, and I like to tinker with
hardware and software everything in between. Things I like include C and Go
and Linux and Assembly and MIDI and abusing hardware and...! Things I don't
like include: CSS. I run
[this software](https://github.com/chandlerswift/dotfiles) on
[this OS](/what-os.html) on
[this hardware](https://pcpartpicker.com/list/HMPTdm).
Ask me about my latest project!

As a musician I'm wrapping up a stint as the
[organist](https://youtu.be/31Ipq5v9T8E?t=3205)/[pianist](https://www.youtube.com/watch?v=xSH4ciadjDs)/[accompanist](https://www.youtube.com/watch?v=byk43j57SeM)
at [Pilgrim Congregational Church in Duluth, MN](http://pilgrimduluth.org/),
and another as an accompanist for the [Lake Superior Youth Chorus](https://www.lsyouthchorus.org/).
When I'm in Duluth, I often play for [Jazz at Blush](https://www.facebook.com/JazzatBlush)
on Monday nights (and if you play an instrument, please come join us!).
I especially enjoy playing in small
[ensembles](https://youtu.be/rxqeobkiNgg?t=482)
[and](https://www.youtube.com/watch?v=R9MqV2G2XAE)
[with](https://www.youtube.com/watch?v=s3Io31XU1k8&t=6s)
[other](https://www.youtube.com/watch?v=cgygq_R-RhY)
[people](https://www.youtube.com/watch?v=Gs4GqA0v690)
as much as I can.

In my free time, I try to remain active with
[my Boy Scout troop](https://troop352.us/) (of which I am an Eagle Scout),
especially on outdoor activities. I enjoy reading science fiction, though I
don't have as much time for it as I might like. I appreciate
[XKCD](https://xkcd.com/) comics, especially
[about](https://xkcd.com/1760/)
[technology](https://xkcd.com/722/).

<hr class="separator">

{% if site.posts.size > 0 %}
## Blog
<div class="media">
{% for post in site.posts limit:3 %}
{% include post-stub.html post=post %}
{% endfor %}
</div>

{% if site.posts.size > 3 %}
<div class="pull-right">
    <a href="/archive/" class="btn btn-primary">
        More
        <span class="icon">
          <svg height="1em" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 512"><path d="M0 384.662V127.338c0-17.818 21.543-26.741 34.142-14.142l128.662 128.662c7.81 7.81 7.81 20.474 0 28.284L34.142 398.804C21.543 411.404 0 402.48 0 384.662z"/></svg>
        </span>
    </a>
</div>
<div class="clearfix"></div>
{% endif %}

<hr class="separator">
{% endif %}

## [Projects](/projects.html)

<div class="media">
{% assign projects = site.projects | sort: 'date' | reverse %}
{% for project in projects %}
{% include project-stub.html project=project %}
{% endfor %}
</div>
