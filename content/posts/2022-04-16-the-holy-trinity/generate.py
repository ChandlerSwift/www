#!/usr/bin/python3

import csv
import requests
import json # TODO: remove

stores = []

# Culvers
print("Searching for Culver's locations")
response = requests.get('https://hosted.where2getit.com/lite?action=getstategeojsonmap&appkey=EC84928C-9C0B-11E4-B999-D8F4B845EC6E').json()

state_names = {}
for f in response['states']['features']:
    state_names[f['properties']['name']] = f['properties']['regiondesc']

for s in response['labels']['features']:
    if s['properties']['num_stores'] > 0:
        state = s['properties']['name']
        print(f"Searching {state}...", end="")
        json_data = {
            'request': {
                'appkey': '1099682E-D719-11E6-A0C4-347BDEB8F1E5',
                'formdata': {
                    'geolocs': {
                        'geoloc': [
                            {
                                'addressline': state,
                                'state': state_names[state],
                            },
                        ],
                    },
                    'stateonly': 1,
                },
            },
        }

        response = requests.post('https://hosted.where2getit.com/culvers/rest/locatorsearch', json=json_data)
        count = 0
        for store in response.json()['response']['collection']:
            # I tried a bunch of other things and this is the only one that matched :facepalm:
            if "coming soon" in store['name'].lower(): # store['comingsoondate']: # not store['dine_in'] and not store['takeout']: # not store['opendate']: # store['comingsoondate']:
                # print(f"{store['name']} not yet open")
                continue
            stores.append({
                'chain': "Culver's",
                'lat':  float(store['latitude']),
                'long': float(store['longitude']),
                'address': store['address1'],
                'city': store['city'],
                'state': store['state'],
                'zip': store['postalcode'],
                'website': store['url'],
            })
            count += 1
        print(count)
        if not count == s['properties']['num_stores']:
            print(f"Inequal for {state}: {count} != {s['properties']['num_stores']}")
print(f"""{len(stores)} locations found""")


# Kwik Trip
# Export to CSV from https://www.kwiktrip.com/Maps-Downloads/Store-List
print("Searching for Kwik Trip locations")
kwiktrip_count = 0
with open('stores.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        kwiktrip_count += 1
        stores.append({
            'chain': "Kwik Trip",
            'lat':  float(row['Latitude']),
            'long': float(row['Longitude']),
            'address': row['Address'].title(),
            'city': row['City'].title(),
            'state': row['State'],
            'zip': row['Zip'],
            'website': f"https://www.kwiktrip.com/locator/store?id={row['Store Number']}",
        })
print(f"{kwiktrip_count} locations found")


# # Menards
print("Searching for Menards locations")

# Visit https://www.menards.com/store-details/locator.html; view source; find a
# value for `data-initial-stores`; copy its value into data here. Incapsula, the
# DDoS mitigation platform that Menards uses, makes this reeeeaaaally hard to do
# with `requests`. Those lines should look something like this:
#
# 125 | <meta
# 126 |     id="initialStores"
# 127 |     data-initial-stores="[{&quot;number&quot;:3132,..."
# 128 |   >
# 129 | </head>
#
# (line 127 is the one you want here)
data="[]"

menardses = json.loads(data.replace("&quot;", '"'))
for menards in menardses:
    stores.append({
        'chain': "Menards",
        'lat':  float(menards['latitude']),
        'long': float(menards['longitude']),
        'address': menards['street'].title(),
        'city': menards['city'].title(),
        'state': menards['state'],
        'zip': menards['zip'],
        'website': f"https://www.menards.com/store-details/store.html?store={menards['number']}",
    })
print(f"{len(menardses)} locations found")

with open('stores.json', 'w') as f:
    f.write(json.dumps(stores))
