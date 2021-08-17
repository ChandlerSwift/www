---
title: Retrieving Kwik Trip Gas Prices
layout: post
IncludeSyntaxStyles: yes
---
Kwik Trip (a popular gas station in the MN-WI-IA area, if you're not from the
Midwest) has an API to display their fuel prices, among other things. Here's a
short Python program to retrieve pricing of nearby stores.

<!--more-->

```python
import requests

# Burnsville, MN
lat=44.767778
long=-93.2775

params = {
    'latitude': lat,
    'longitude': long,
    'limit': 20 # 1-255
}
stores = requests.get("https://api.kwiktrip.com/api/stores/nearby", params=params).json()["stores"]

for store in stores:
    has_gas = [p for p in store['properties'] if p['name'] == 'GAS'][0]
    if not has_gas:
        continue

    storedata = requests.get(f"https://api.kwiktrip.com/api/location/store/information/{store['id']}").json()

    unleaded_price = [p for p in storedata["fuel"] if p["type"] == "UNLEADED"][0]
    location_str = f'{store["address"]["city"].title()}, {store["address"]["state"]}'
    print(f'{store["id"]} ({location_str}): {unleaded_price["currentPrice"]}')
```

Sample output (as of date of publishing):
```text
585 (Burnsville, MN): 3.099
695 (Apple Valley, MN): 2.999
309 (Burnsville, MN): 3.099
179 (Eagan, MN): 3.099
406 (Apple Valley, MN): 3.059
694 (Lakeville, MN): 3.049
663 (Savage, MN): 3.099
421 (Apple Valley, MN): 3.059
343 (Lakeville, MN): 3.059
397 (Apple Valley, MN): 3.059
447 (Shakopee, MN): 3.099
443 (Farmington, MN): 3.059
281 (Prior Lake, MN): 3.099
692 (Lakeville, MN): 3.099
697 (Rosemount, MN): 3.099
662 (Eagan, MN): 3.099
693 (Farmington, MN): 3.099
441 (Shakopee, MN): 3.049
492 (Chanhassen, MN): 3.099
178 (South St Paul, MN): 3.099
```

If you want pricing information on _all_ Kwik Trip stores, it's a bit more
difficult, as the `limit` parameter on the `/stores/nearby` request is capped at
a maximum of 255. In this case, a CSV of all Kwik Trip stores can be found at
https://www.kwiktrip.com/Maps-Downloads/Store-List (click Export to CSV above
the table), and that can be used as a basis for the requests:

```python
import csv
import requests

with open('stores.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["Sells Gas"] == "No":
            continue
        if row["State"] != "MN":
            continue
        r = requests.get(f"https://api.kwiktrip.com/api/location/store/information/{row['Store Number']}").json()
        unleaded_price = [p for p in r["fuel"] if p["type"] == "UNLEADED"][0]
        print(f'{row["Store Number"]} ({row["City"]}, {row["State"]}): {unleaded_price["currentPrice"]}')
```
<details>
<summary>Output</summary>

```
804 (ALBERT LEA, MN): 3.049
805 (ALBERT LEA, MN): 3.049
875 (ALBERT LEA, MN): 3.049
1020 (ALBERTVILLE, MN): 3.049
812 (ANDOVER, MN): 3.099
1017 (ANOKA, MN): 3.099
474 (ANOKA, MN): 3.039
406 (APPLE VALLEY, MN): 3.059
695 (APPLE VALLEY, MN): 2.819
397 (APPLE VALLEY, MN): 3.099
421 (APPLE VALLEY, MN): 3.059
250 (AUSTIN, MN): 3.099
689 (AUSTIN, MN): 3.099
246 (AUSTIN, MN): 3.099
445 (AUSTIN, MN): 3.099
330 (BELLE PLAINE, MN): 3.049
168 (BIG LAKE, MN): 3.149
925 (BLAINE, MN): 3.049
1022 (BLAINE, MN): 2.999
896 (BLAINE, MN): 3.049
1014 (BLAINE, MN): 2.999
646 (BLUE EARTH, MN): 3.089
880 (BROOKLYN PARK, MN): 3.099
448 (BROOKLYN PARK, MN): 3.099
458 (BUFFALO, MN): 3.039
309 (BURNSVILLE, MN): 3.099
585 (BURNSVILLE, MN): 3.099
1045 (BYRON, MN): 3.149
622 (BYRON, MN): 3.149
code 733 (CALEDONIA, MN): 3.099
571 (CARLTON, MN): 3.149
1095 (CARVER, MN): 2.989
492 (CHANHASSEN, MN): 3.099
402 (CHANHASSEN, MN): 3.099
886 (CHASKA, MN): 3.099
608 (CHATFIELD, MN): 3.079
874 (CHISAGO CITY, MN): 3.059
206 (CIRCLE PINES, MN): 3.099
104 (CLEARWATER, MN): 3.099
247 (CLOQUET, MN): 3.149
234 (CLOQUET, MN): 3.149
144 (CLOQUET, MN): 3.149
1120 (COLD SPRING, MN): 2.999
465 (COON RAPIDS, MN): 3.059
497 (DAKOTA, MN): 3.049
1031 (DELANO, MN): 3.099
789 (DODGE CENTER, MN): 3.149
273 (DULUTH, MN): 3.099
274 (DULUTH, MN): 3.099
941 (DULUTH, MN): 3.099
218 (DULUTH, MN): 3.099
117 (DULUTH, MN): 3.099
224 (DULUTH, MN): 3.059
489 (DUNDAS, MN): 3.099
179 (EAGAN, MN): 3.099
662 (EAGAN, MN): 3.099
753 (EYOTA, MN): 3.099
424 (FAIRMONT, MN): 3.049
744 (FARIBAULT, MN): 3.099
745 (FARIBAULT, MN): 3.099
793 (FARIBAULT, MN): 3.099
772 (FARIBAULT, MN): 3.099
693 (FARMINGTON, MN): 3.099
443 (FARMINGTON, MN): 3.059
429 (FOREST LAKE, MN): 3.089
1049 (GLENCOE, MN): 3.149
848 (HARMONY, MN): 3.079
249 (HASTINGS, MN): 3.039
220 (HERMANTOWN, MN): 3.059
572 (HERMANTOWN, MN): 3.059
216 (HERMANTOWN, MN): 3.059
186 (HINCKLEY, MN): 3.199
825 (HOKAH, MN): 3.099
454 (HUGO, MN): 3.099
316 (HUTCHINSON, MN): 2.919
1019 (ISANTI, MN): 2.979
619 (KASSON, MN): 3.149
814 (KELLOGG, MN): 2.999
614 (LA CRESCENT, MN): 3.099
437 (LA CRESCENT, MN): 3.099
844 (LAKE CITY, MN): 3.049
600 (LAKE CITY, MN): 3.049
1078 (LAKE ELMO, MN): 3.099
248 (LAKE ELMO, MN): 3.099
343 (LAKEVILLE, MN): 3.059
692 (LAKEVILLE, MN): 3.099
694 (LAKEVILLE, MN): 3.049
737 (LEWISTON, MN): 3.059
449 (MANKATO, MN): 3.049
1011 (MANKATO, MN): 3.049
344 (MANKATO, MN): 3.049
334 (MANKATO, MN): 3.049
379 (MANKATO, MN): 3.049
275 (MANKATO, MN): 3.049
431 (MANKATO, MN): 3.049
1026 (MILACA, MN): 3.099
623 (MINNESOTA CITY, MN): 3.099
345 (MONTICELLO, MN): 3.149
177 (MONTICELLO, MN): 3.149
166 (MOOSE LAKE, MN): 3.199
1037 (MORA, MN): 3.079
926 (NEW PRAGUE, MN): 2.959
1090 (NEW PRAGUE, MN): 2.959
432 (NEW ULM, MN): 3.049
931 (NORTH BRANCH, MN): 3.099
930 (NORTH BRANCH, MN): 3.099
615 (NORTH MANKATO, MN): 3.049
385 (NORTHFIELD, MN): 3.099
854 (NORWOOD YOUNG AMERICA, MN): 3.099
111 (OAK PARK HEIGHTS, MN): 3.099
869 (OAKDALE, MN): 3.099
162 (OTSEGO, MN): 3.099
1088 (OWATONNA, MN): 2.929
403 (OWATONNA, MN): 2.959
641 (OWATONNA, MN): 2.929
806 (OWATONNA, MN): 2.929
237 (OWATONNA, MN): 2.929
435 (OWATONNA, MN): 2.929
598 (PAYNESVILLE, MN): 3.099
640 (PINE ISLAND, MN): 3.099
245 (PLAINVIEW, MN): 3.099
411 (PLYMOUTH, MN): 3.099
928 (PRINCETON, MN): 2.959
281 (PRIOR LAKE, MN): 3.099
481 (RED WING, MN): 2.999
305 (RED WING, MN): 2.999
376 (RED WING, MN): 2.999
590 (ROCHESTER, MN): 3.099
672 (ROCHESTER, MN): 3.099
279 (ROCHESTER, MN): 3.099
418 (ROCHESTER, MN): 3.099
659 (ROCHESTER, MN): 3.099
341 (ROCHESTER, MN): 3.099
382 (ROCHESTER, MN): 3.099
388 (ROCHESTER, MN): 3.099
321 (ROCHESTER, MN): 3.099
438 (ROCHESTER, MN): 3.099
335 (ROCHESTER, MN): 3.099
357 (ROCHESTER, MN): 3.099
364 (ROCHESTER, MN): 3.099
433 (ROCHESTER, MN): 3.099
464 (ROCHESTER, MN): 2.999
570 (ROCKFORD, MN): 3.099
697 (ROSEMOUNT, MN): 3.099
592 (RUSH CITY, MN): 3.149
609 (RUSHFORD, MN): 3.099
477 (SAINT BONIFACIUS, MN): 3.099
754 (SAINT CHARLES, MN): 3.029
120 (SAINT CLOUD, MN): 2.999
158 (SAINT CLOUD, MN): 2.999
146 (SAINT CLOUD, MN): 2.999
151 (SAINT CLOUD, MN): 2.999
150 (SAINT CLOUD, MN): 2.999
149 (SAINT CLOUD, MN): 2.999
943 (SAINT FRANCIS, MN): 2.939
147 (SAINT JOSEPH, MN): 2.999
575 (SAINT JOSEPH, MN): 2.999
681 (SAINT MICHAEL, MN): 3.099
466 (SAINT PETER, MN): 3.099
153 (SARTELL, MN): 2.999
154 (SAUK RAPIDS, MN): 2.999
663 (SAVAGE, MN): 3.099
441 (SHAKOPEE, MN): 3.049
447 (SHAKOPEE, MN): 3.099
178 (SOUTH ST PAUL, MN): 3.099
736 (SPRING GROVE, MN): 3.099
831 (SPRING VALLEY, MN): 3.149
213 (STACY, MN): 3.149
803 (STEWARTVILLE, MN): 3.149
414 (STEWARTVILLE, MN): 3.149
415 (STILLWATER, MN): 3.099
141 (TWO HARBORS, MN): 3.049
152 (VADNAIS HEIGHTS, MN): 3.099
843 (WABASHA, MN): 2.999
460 (WACONIA, MN): 3.099
137 (WAITE PARK, MN): 2.999
160 (WAITE PARK, MN): 2.999
1034 (WASECA, MN): 3.049
442 (WASECA, MN): 3.049
937 (WILLMAR, MN): 3.099
944 (WILLMAR, MN): 3.099
945 (WILLMAR, MN): 3.099
746 (WINONA, MN): 3.099
810 (WINONA, MN): 3.099
654 (WINONA, MN): 3.099
778 (WINONA, MN): 3.099
824 (WINONA, MN): 3.099
811 (WINONA, MN): 3.099
407 (WOODBURY, MN): 3.099
408 (WOODBURY, MN): 3.099
1028 (WORTHINGTON, MN): 3.099
463 (ZUMBROTA, MN): 2.989
```
</details>

Although, of course:
[![](https://imgs.xkcd.com/comics/working.png)](https://xkcd.com/951/)
