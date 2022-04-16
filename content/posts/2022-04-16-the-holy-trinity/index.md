---
layout: post
title: "The Holy (Midwestern) Trinity: Culvers, Kwik Trip, and Menards"
IncludeSyntaxStyles: true
---

If you live in the Upper Midwest, you know what I mean: There's no place like
Culvers. And Kwik Trip. And Menards. (All Wisconsin-based, for that lovely
hometown charm.) But the worst part of visiting all three is the period of time
between stepping out of one and arriving at another. Where is the best location
we can minimize this pain?

<!--more-->

<details>
    <summary>First, obligatory memes:</summary>
    <!-- TODO: this layout squishes images. Why? -->
    <div style="display: flex; flex-wrap: wrap; justify-content: center;">
        <img style="max-width:300px;" alt="The holy trinity: Culver's, Kwik Trip, and Menards" src="the-holy-trinity/trinity.png">
        <img style="max-width:300px;" alt="Spongebob meme: Culvers is the Krusty Krab; Dairy Queen is the Chum Bucket" src="the-holy-trinity/culvers-meme.jpg">
        <img style="max-width:300px;" alt="'Me explaining to my mom' meme: 'Me explaining why Kwik Trip isn't just an ordinary gas station'/'my friend from out of state'" src="the-holy-trinity/kwik-trip-meme.png">
        <video controls style="max-width: 300px;" loop>
            <source src="the-holy-trinity/menards-meme.mp4" type="video/mp4">
        </video>
        <!--
        also in consideration:
        https://imgflip.com/i/54altg
        https://ifunny.co/picture/came-to-new-york-for-the-lights-but-discovered-at-MfU7xdI99
        -->
    </div>
</details>

I grew up near Hutchinson, MN. Hutchinson gained a Menards in
2001[^menards-citation], a Culvers in 2005[^culvers-citation], and a Kwik Trip
in 2013[^kwik-trip-citation]. They're all within a few blocks of each other---a
good start for minimizing the total trip time of a Culver's--Kwik Trip--Menards
lap.

[^menards-citation]: Source: [Eric](https://ericvillnow.com/) says so. (The
    Menards API used to expose this information, but has since stopped.)
[^culvers-citation]: https://weblink.hutchinsonmn.gov/WebLink/DocView.aspx?id=16157&dbid=0&repo=Hutchinson&cr=1
    p.36-38
[^kwik-trip-citation]: https://mblsportal.sos.state.mn.us/Business/SearchDetails?filingGuid=3adf3dfd-6c16-e311-8e3a-001ec94ffe7f

<link rel="stylesheet" href="/css/leaflet.css" />
<script src="/js/leaflet.js"></script>

<script>
    let CustomIcon = L.Icon.extend({
        options: {
            iconSize:     [30, 40],
            iconAnchor:   [15, 40],
            popupAnchor:  [20, -5],
        }
    });
    let icons = {
        "Menards":   new CustomIcon({iconUrl: 'the-holy-trinity/menards-location-pin-solid.svg'}),
        "Culver's":  new CustomIcon({iconUrl: 'the-holy-trinity/culvers-location-pin-solid.svg'}),
        "Kwik Trip": new CustomIcon({iconUrl: 'the-holy-trinity/kwiktrip-location-pin-solid.svg'}),
    };

    function mapWith(el, filterFn=()=>true, setView=true, targetZoom=null) {
        let map = L.map(el);
        L.control.scale().addTo(map);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);
        document.addEventListener("data-loaded", function(){
            let markers = [];
            for (let store of stores.filter(filterFn)) {
                let marker = L.marker([store['lat'], store['long']], {icon: icons[store['chain']]}).addTo(map);
                marker.bindPopup(`${store['address']}<br>${store['city']}, ${store['state']} ${store['zip']}<br><a href="${store['website']}">${store['website']}</a>`);
                markers.push(marker);
            }
            if (setView) {
                map.fitBounds(L.featureGroup(markers).getBounds().pad(0.2));
            }
            if (targetZoom) {
                map.setZoom(targetZoom);
            }
        });
        return map;
    }

    let stores;
    fetch("the-holy-trinity/stores.json")
        .then(response => response.json())
        .then(data => stores = data)
        .then(() => document.dispatchEvent(new Event("data-loaded")));
</script>

<div id="hutchinson-map" style="height: 400px;"></div>

<script>
    let hutchinson = mapWith('hutchinson-map', store => store.state == "MN" && store.city == "Hutchinson");
</script>

But is there a location that has a closer clustering? Here we brute force every
Culver's/Kwik Trip/Menards combination, checking the sum of their distances and
finding the top ten results. (We use the sum of distances as a rough estimate of
the stores' total distance apart; one could also find the "center of mass"---the
point where the sum of distances to each of the other points is minimal---and
find the sum of distances to the other points, or any number of other scoring
methods.)

{{% code file="content/posts/2022-04-16-the-holy-trinity/find_closest_trio.py" language="python" %}}

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

| Rank | Culver's | Kwik Trip | Menards | Total distance |
|-|-|-|-|-|
| 1 | [1101 2nd St S, Waite Park, MN 56387](http://www.culvers.com/restaurants/waite-park) | [106 10Th Ave S, Waite Park, MN 56387](https://www.kwiktrip.com/locator/store?id=137) | [251 10Th Ave S, Waite Park, MN 56387](https://www.menards.com/store-details/store.html?store=3015) | 0.39 miles |
| 2 | [3604 University Dr, Muscatine, IA 52761](http://www.culvers.com/restaurants/muscatine) | [3605 University Dr, Muscatine, IA 52761](https://www.kwiktrip.com/locator/store?id=1064) | [3408 N Highway 61, Muscatine, IA 52761](https://www.menards.com/store-details/store.html?store=3135) | 0.43 miles |
| 3 | [525 Village Walk Ln, Johnson Creek, WI 53038](http://www.culvers.com/restaurants/johnson-creek) | [465 Village Walk Ln, Johnson Creek, WI 53038](https://www.kwiktrip.com/locator/store?id=487) | [440 Wright Rd, Johnson Creek, WI 53038](https://www.menards.com/store-details/store.html?store=3159) | 0.53 miles |
| 4 | [W6606 State Rd 23, Fond du Lac, WI 54937](http://www.culvers.com/restaurants/fond-du-lac-hwy-23) | [1123 W Johnson St, Fond Du Lac, WI 54937](https://www.kwiktrip.com/locator/store?id=652) | [1200 Rickmeyer Dr, Fond Du Lac, WI 54937](https://www.menards.com/store-details/store.html?store=3106) | 0.58 miles |
| 5 | [2270 Westowne Ave, Oshkosh, WI 54904](http://www.culvers.com/restaurants/oshkosh-westowne) | [1090 N Washburn St, Oshkosh, WI 54904](https://www.kwiktrip.com/locator/store?id=862) | [2351 Westowne Ave, Oshkosh, WI 54904](https://www.menards.com/store-details/store.html?store=3025) | 0.74 miles |
| 6 | [1510 Montreal St, Hutchinson, MN 55350](http://www.culvers.com/restaurants/hutchinson) | [10 Denver Ave Se, Hutchinson, MN 55350](https://www.kwiktrip.com/locator/store?id=316) | [1525 Montreal St Se, Hutchinson, MN 55350](https://www.menards.com/store-details/store.html?store=3155) | 0.74 miles |
| 7 | [1499 Lawrence Dr, De Pere, WI 54115](http://www.culvers.com/restaurants/de_pere) | [1620 Lawrence Dr, De Pere, WI 54115](https://www.kwiktrip.com/locator/store?id=1060) | [1313 Lawrence Dr, De Pere, WI 54115](https://www.menards.com/store-details/store.html?store=3281) | 0.86 miles |
| 8 | [1601 E 1st St, Grimes, IA 50111](http://www.culvers.com/restaurants/grimes-ia-1st-st) | [2351 E 1St St, Grimes, IA 50111](https://www.kwiktrip.com/locator/store?id=1055) | [300 Ne Destination Dr, Grimes, IA 50111](https://www.menards.com/store-details/store.html?store=3360) | 0.89 miles |
| 9 | [3048 5th Ave S, Fort Dodge, IA 50501](http://www.culvers.com/restaurants/fort-dodge) | [3121 5Th Ave S, Fort Dodge, IA 50501](https://www.kwiktrip.com/locator/store?id=509) | [3319 5Th Ave S, Fort Dodge, IA 50501](https://www.menards.com/store-details/store.html?store=3134) | 0.93 miles |
| 10 | [2520 Folsom St, Eau Claire, WI 54703](http://www.culvers.com/restaurants/eau-claire-folsom) | [2327 N Clairemont Ave, Eau Claire, WI 54703](https://www.kwiktrip.com/locator/store?id=390) | [3210 N Clairemont Ave, Eau Claire, WI 54703](https://www.menards.com/store-details/store.html?store=3011) | 1.18 miles |

Waite Park, MN comes out on top:

<div id="waitepark-map" style="height: 400px;"></div>

<script>
    let waitepark = mapWith('waitepark-map', store => store.state == "MN" && store.city == "Waite Park" && store.address != "458 Great Oak Dr", true, 15);
</script>

with Muscatine, IA a close second:

<div id="muscatine-map" style="height: 400px;"></div>

<script>
    let muscatine = mapWith('muscatine-map', store => store.state == "IA" && store.city == "Muscatine", true, 15);
</script>

And Hutchinson does make the list! The 0.74 miles for a Culvers-Menards-Kwik
Trip lap puts it in 6th place.

<br>
<hr>

While we have all this fun data, let's check out a few more things! I've noticed
that Menardses and Culver'ses seem to have a habit of being located right next
to each other though I have yet to see a Culver's in a Menards, the way you
might see a Subway in a Walmart, or something). This was true in Hutchinson,
Eden Prairie[^wrong-here], Burnsville/Savage, Richfield/Bloomington -- every
Menards I've ever been to, I believe, except Apple Valley.

[^wrong-here]: The Culver's here moved across the street a few years ago; it's
    now on the north side of 212. However, the Culver's restaurant, while
    updated to the correct address, still has the wrong coordinates:
    https://www.culvers.com/locator?key=220

<div id="culvers-menards-map" style="height: 400px;"></div>

<script>
    let culvers_menards = mapWith('culvers-menards-map', store => {
        return (store.chain == "Menards" || store.chain == "Culver's") && (
            (store.state == "MN" && store.city == "Hutchinson") ||
            (store.state == "MN" && store.city == "Eden Prairie") ||
            (store.state == "MN" && store.city == "Burnsville") ||
            (store.state == "MN" && store.city == "Savage") ||
            (store.state == "MN" && store.city == "Richfield") ||
            (store.state == "MN" && store.city == "Bloomington")
        );
    });
</script>

It's very possible that this is just confirmation bias, though -- it's not true
in Apple Valley, at least. When else _isn't_ this the case? That is, what cities
have the biggest distances between their Culver's and Menards?

{{% code file="content/posts/2022-04-16-the-holy-trinity/find_biggest_menards_culvers_gap.py" language="python" %}}


| Rank | Culver's | Menards | Distance |
|-|-|-|-|
| 1 | [4701 Kentucky Ave, Indianapolis 46221](http://www.culvers.com/restaurants/indianapolis-kentucky) | [7145 E 96Th St, Indianapolis 46250](https://www.menards.com/store-details/store.html?store=3171) |  19.41 miles |
| 2 | [7953 State Line Rd, Kansas City 64114](http://www.culvers.com/restaurants/kansas-city-mo) | [3701 Nw 90Th St, Kansas City 64154](https://www.menards.com/store-details/store.html?store=3342) |  18.84 miles |
| 3 | [7105 E 96th St, Indianapolis 46250](http://www.culvers.com/restaurants/indianapolis-96th) | [7140 S Emerson Ave, Indianapolis 46237](https://www.menards.com/store-details/store.html?store=3084) |  18.28 miles |
| 4 | [8232 Country Village Dr, Indianapolis 46214](http://www.culvers.com/restaurants/indianapolis-in-rockville-rd) | [7145 E 96Th St, Indianapolis 46250](https://www.menards.com/store-details/store.html?store=3171) |  17.85 miles |
| 5 | [5020 W 71st St, Indianapolis 46268](http://www.culvers.com/restaurants/indianapolis-71st) | [7140 S Emerson Ave, Indianapolis 46237](https://www.menards.com/store-details/store.html?store=3084) |  17.36 miles |
| 6 | [1444 Rentra Dr, Columbus 43228](http://www.culvers.com/restaurants/columbus-oh) | [6800 E Broad St, Columbus 43213](https://www.menards.com/store-details/store.html?store=3280) |  17.14 miles |
| 7 | [11050 S. Doty Avenue W, Chicago 60628](http://www.culvers.com/restaurants/chicago-il-doty-ave) | [2601 N Clybourn Ave, Chicago 60614](https://www.menards.com/store-details/store.html?store=3092) |  16.82 miles |
| 8 | [11050 S. Doty Avenue W, Chicago 60628](http://www.culvers.com/restaurants/chicago-il-doty-ave) | [4501 W North Ave, Chicago 60639](https://www.menards.com/store-details/store.html?store=3245) |  16.38 miles |
| 9 | [575 W Layton Ave, Milwaukee 53207](http://www.culvers.com/restaurants/milwaukee-layton) | [8110 W Brown Deer Rd, Milwaukee 53223](https://www.menards.com/store-details/store.html?store=3029) |  16.07 miles |
| 10 | [5115 Shear Avenue, Indianapolis 46203](http://www.culvers.com/restaurants/indianapolis-in-emerson-ave) | [7145 E 96Th St, Indianapolis 46250](https://www.menards.com/store-details/store.html?store=3171) |  15.77 miles |

Unsurprisingly, it's just a bunch of really big cities with multiple stores
across their respective metro areas. (With some cities with widely spread
locations highly overrepresented, too!) Here's Indianapolis:

<div id="indianapolis-map" style="height: 400px;"></div>

<script>
    let indianapolis = mapWith('indianapolis-map', store => store.state == "IN" && store.city == "Indianapolis");
</script>
<br>

---

Finally, since I have all this neat data, here's a map of every Culvers, Kwik
Trip, and Menards.

<div id="all-map" style="height: 400px;"></div>

<script>
    let all = mapWith('all-map', ()=>true, setView=false);
    all.setView([42.5, -90], 5);
</script>

<br>

<details>
<summary>Here's how I retrieved the data I used:</summary>
{{% code file="content/posts/2022-04-16-the-holy-trinity/generate.py" language="python" %}}
</details>
