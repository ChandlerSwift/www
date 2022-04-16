import json
import math

# Should take ~20 seconds to run

# http://edwilliams.org/avform147.htm#Dist
def dist(store1, store2):
    lat1 = store1['lat'] * math.pi/180
    lon1 = store1['long'] * math.pi/180
    lat2 = store2['lat'] * math.pi/180
    lon2 = store2['long'] * math.pi/180
    distance_in_radians = 2*math.asin(math.sqrt((math.sin((lat1-lat2)/2))**2 + 
                math.cos(lat1)*math.cos(lat2)*(math.sin((lon1-lon2)/2))**2))
    earth_radius = 3959 # freedom units (miles)
    return distance_in_radians * earth_radius

def total_dist(store1, store2, store3):
    return dist(store1, store2) + dist(store2, store3) + dist(store3, store1)

# Format an address
def a(x):
    return  f"[{x['address']}, {x['city']}, {x['state']} {x['zip']}]({x['website']})"

if __name__ == '__main__':
    # A naïve approach might be to check for each city how close the Culver's,
    # Kwik Trip, and Menards are (if a city has all three). However, this would
    # break if there happen to be close clusterings across city lines. Instead,
    # we make a list of the locations of each chain, and process that. (While
    # that does make a difference for some results, none of them make it into
    # the top 10.)
    with open("stores.json", 'r') as f:
        stores = json.loads(f.read())

    culverses = list(filter(lambda s: s['chain'] == "Culver's", stores))
    kwiktrips = list(filter(lambda s: s['chain'] == "Kwik Trip", stores))
    menardses = list(filter(lambda s: s['chain'] == "Menards", stores))

    top_matches = []

    for culvers in culverses:
        for kwiktrip in kwiktrips:
            # This is a hack to speed the program up; without this the program
            # takes hours to run. With this optimization, it takes <1 minute.
            if abs(kwiktrip['lat'] - culvers['lat']) + abs(kwiktrip['long'] - culvers['long']) > 2: # More than ~50 miles apart
                continue
            for menards in menardses:
                if abs(kwiktrip['lat'] - menards['lat']) + abs(kwiktrip['long'] - menards['long']) > 2:
                    continue
                top_matches.append({
                    "culvers": culvers,
                    "kwiktrip": kwiktrip,
                    "menards": menards,
                    "dist": total_dist(culvers, kwiktrip, menards),
                })
                top_matches.sort(key=lambda s: s['dist'])
                top_matches = top_matches[:10]

    print("| Rank | Culver's | Kwik Trip | Menards | Total distance |")
    print("|-|-|-|-|-|")
    for rank, top_match in enumerate(top_matches, start=1):
        print(f"| {rank} | {a(top_match['culvers'])} | {a(top_match['kwiktrip'])} | {a(top_match['menards'])} | {top_match['dist']:.2f} miles |")
