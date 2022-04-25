---
title: Ages of Minnesota Wild Players
layout: post
IncludeSyntaxStyles: yes
---

Tonight the Minnesota Wild won their game against the Nashville Predators, in a
nailbiting finish---we (specifically Dmitry Kulikov, age 31) scored our final
goal to end 5-4 with 1.3 seconds left of overtime.

It's always amazing to me as I get older that a large component of professional
sports players are younger than I am. (Though hockey players are somewhat older
than I'd imagined: Both goalies are in their mid to late thirties, and the
median player is still a few years older than I am.)

<!--more-->

The NHL has pretty good information available about their games, so I poked
around a bit. ([Here's the (extensive!) data for tonight's
game](https://statsapi.web.nhl.com/api/v1/game/2021021267/feed/live).)

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

```python
import requests, datetime

def age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

roster = requests.get("https://statsapi.web.nhl.com/api/v1/teams/30/roster").json()['roster']

# Retrieve full data on each player
players = []
for player in roster:
    players.append(requests.get(f"https://statsapi.web.nhl.com{player['person']['link']}").json()['people'][0])
players.sort(key=lambda p: p['birthDate'], reverse=True)

# Display table by age
print("| Name | Position | DOB | Age |\n|-|-|-|-|") 
for p in players:
    born = datetime.date.fromisoformat(p['birthDate'])
    print(f"| [{p['fullName']}](https://www.nhl.com/player/{p['id']}) | {p['primaryPosition']['name']} | {p['birthDate']} | {age(born)} |")

# Find average player age
average_dob = datetime.date.fromtimestamp(sum([datetime.datetime.combine(datetime.date.fromisoformat(p['birthDate']), datetime.time()).timestamp() for p in players])/len(players))
print(f"Average age: {age(average_dob)}")

# Count players by age
min_age = age(datetime.date.fromisoformat(players[0]['birthDate']))
max_age = age(datetime.date.fromisoformat(players[-1]['birthDate']))
players_by_age = {}
for a in range(min_age, max_age+1):
    players_by_age[a] = []
for p in players:
    players_by_age[age(datetime.date.fromisoformat(p['birthDate']))].append(p)
for age, players in players_by_age.items():
    print(f"{len(players)} players {age} years old")
```

<!--
```python
print("""<div class="chart">""")
for age, players in players_by_age.items():
    print(f"""<div class="part percent-{100*len(players)//3}"><div class="label">{age}</div><div class="bar"><div class="label">{', '.join([f"<a href='https://www.nhl.com/player/{p['id']}'>{p['lastName']}</a>" for p in players])}</div></div></div>""")
print("""</div>""")
```
-->

<style>
.chart {
  position: relative;
  border-radius: 5px;
  font-size: 16px;
}
.chart * {
  box-sizing: border-box;
}
.chart:after {
  content: "";
  position: absolute;
  left: 10%;
  top: 0;
  width: 4px;
  background: #888;
  height: 100%;
  border-radius: 2px;
}
.chart .part {
  display: flex;
  height: 3em;
}
.chart .part > .label {
  flex: 1;
  flex-basis: 10%;
  text-align: right;
  padding-right: 1em;
  margin: 0.5em 0;
  height: 2em;
  line-height: 2em;
  font-weight: 600;
}
.chart .part .bar {
  flex: 3;
  flex-basis: 90%;
  position: relative;
  margin: 0.5em 0;
}
.chart .part .bar:after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  border-radius: 0 2px 2px 0;
  background: #444;
}
.chart .part .bar .label {
  position: absolute;
  top: 50%;
  left: 0.5em;
  transform: translateX(0%) translateY(-50%);
  z-index: 1;
  color: #FFF;
  font-weight: 600;
}
.chart .part .bar a {
  color: #FFF;
  text-decoration: none;
}
.chart .part .bar a:hover {
  text-decoration: underline;
}
.chart .part.percent-33 .bar:after {
  width: 33%;
}
.chart .part.percent-66 .bar:after {
  width: 66%;
}
.chart .part.percent-100 .bar:after {
  width: 100%;
}
</style>

2021-2022 Minnesota Wild players by age:

<div class="chart">
    <div class="part percent-33"><div class="label">21</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8481557'>Boldy</a></div></div></div>
    <div class="part percent-33"><div class="label">22</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8480980'>Dewar</a></div></div></div>
    <div class="part percent-0"><div class="label">23</div><div class="bar"><div class="label"></div></div></div>
    <div class="part percent-100"><div class="label">24</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8479370'>Jost</a>, <a href='https://www.nhl.com/player/8479520'>Duhaime</a>, <a href='https://www.nhl.com/player/8478864'>Kaprizov</a></div></div></div>
    <div class="part percent-100"><div class="label">25</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8478413'>Greenway</a>, <a href='https://www.nhl.com/player/8478493'>Eriksson Ek</a>, <a href='https://www.nhl.com/player/8477942'>Fiala</a></div></div></div>
    <div class="part percent-33"><div class="label">26</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8478136'>Middleton</a></div></div></div>
    <div class="part percent-66"><div class="label">27</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8477451'>Hartman</a>, <a href='https://www.nhl.com/player/8476856'>Dumba</a></div></div></div>
    <div class="part percent-66"><div class="label">28</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8476463'>Brodin</a>, <a href='https://www.nhl.com/player/8477919'>Gaudreau</a></div></div></div>
    <div class="part percent-66"><div class="label">29</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8476390'>Cramarossa</a>, <a href='https://www.nhl.com/player/8475760'>Bjugstad</a></div></div></div>
    <div class="part percent-66"><div class="label">30</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8475750'>Merrill</a>, <a href='https://www.nhl.com/player/8475220'>Foligno</a></div></div></div>
    <div class="part percent-66"><div class="label">31</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8475235'>Deslauriers</a>, <a href='https://www.nhl.com/player/8475179'>Kulikov</a></div></div></div>
    <div class="part percent-33"><div class="label">32</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8474716'>Spurgeon</a></div></div></div>
    <div class="part percent-0"><div class="label">33</div><div class="bar"><div class="label"></div></div></div>
    <div class="part percent-100"><div class="label">34</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8475692'>Zuccarello</a>, <a href='https://www.nhl.com/player/8474818'>Benn</a>, <a href='https://www.nhl.com/player/8475660'>Talbot</a></div></div></div>
    <div class="part percent-0"><div class="label">35</div><div class="bar"><div class="label"></div></div></div>
    <div class="part percent-33"><div class="label">36</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8471274'>Goligoski</a></div></div></div>
    <div class="part percent-33"><div class="label">37</div><div class="bar"><div class="label"><a href='https://www.nhl.com/player/8470594'>Fleury</a></div></div></div>
</div>

The average player is 29 years and one month old; the median player is 28.

| Name | Position | DOB | Age[^as-of-today] |
|-|-|-|-|
| [Matt Boldy](https://www.nhl.com/player/8481557) | Left Wing | 2001-04-05 | 21 |
| [Connor Dewar](https://www.nhl.com/player/8480980) | Center | 1999-06-26 | 22 |
| [Tyson Jost](https://www.nhl.com/player/8479370) | Center | 1998-03-14 | 24 |
| [Brandon Duhaime](https://www.nhl.com/player/8479520) | Right Wing | 1997-05-22 | 24 |
| [Kirill Kaprizov](https://www.nhl.com/player/8478864) | Left Wing | 1997-04-26 | 24 |
| [Jordan Greenway](https://www.nhl.com/player/8478413) | Left Wing | 1997-02-16 | 25 |
| [Joel Eriksson Ek](https://www.nhl.com/player/8478493) | Center | 1997-01-29 | 25 |
| [Kevin Fiala](https://www.nhl.com/player/8477942) | Left Wing | 1996-07-22 | 25 |
| [Jacob Middleton](https://www.nhl.com/player/8478136) | Defenseman | 1996-01-02 | 26 |
| [Ryan Hartman](https://www.nhl.com/player/8477451) | Right Wing | 1994-09-20 | 27 |
| [Matt Dumba](https://www.nhl.com/player/8476856) | Defenseman | 1994-07-25 | 27 |
| [Jonas Brodin](https://www.nhl.com/player/8476463) | Defenseman | 1993-07-12 | 28 |
| [Frederick Gaudreau](https://www.nhl.com/player/8477919) | Center | 1993-05-01 | 28 |
| [Joseph Cramarossa](https://www.nhl.com/player/8476390) | Center | 1992-10-26 | 29 |
| [Nick Bjugstad](https://www.nhl.com/player/8475760) | Center | 1992-07-17 | 29 |
| [Jon Merrill](https://www.nhl.com/player/8475750) | Defenseman | 1992-02-03 | 30 |
| [Marcus Foligno](https://www.nhl.com/player/8475220) | Left Wing | 1991-08-10 | 30 |
| [Nicolas Deslauriers](https://www.nhl.com/player/8475235) | Left Wing | 1991-02-22 | 31 |
| [Dmitry Kulikov](https://www.nhl.com/player/8475179) | Defenseman | 1990-10-29 | 31 |
| [Jared Spurgeon](https://www.nhl.com/player/8474716) | Defenseman | 1989-11-29 | 32 |
| [Mats Zuccarello](https://www.nhl.com/player/8475692) | Right Wing | 1987-09-01 | 34 |
| [Jordie Benn](https://www.nhl.com/player/8474818) | Defenseman | 1987-07-26 | 34 |
| [Cam Talbot](https://www.nhl.com/player/8475660) | Goalie | 1987-07-05 | 34 |
| [Alex Goligoski](https://www.nhl.com/player/8471274) | Defenseman | 1985-07-30 | 36 |
| [Marc-Andre Fleury](https://www.nhl.com/player/8470594) | Goalie | 1984-11-28 | 37 |

[^as-of-today]: As of today, April 24, 2022.
