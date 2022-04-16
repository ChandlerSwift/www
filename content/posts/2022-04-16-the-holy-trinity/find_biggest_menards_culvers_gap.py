import json
import math
from find_closest_trio import dist, a

if __name__ == '__main__':
    most_widely_spaced_pairs = []
    with open("stores.json", 'r') as f:
        stores = json.loads(f.read())

    culverses = list(filter(lambda s: s['chain'] == "Culver's", stores))
    menardses = list(filter(lambda s: s['chain'] == "Menards", stores))

    for culvers in culverses:
        for menards in menardses:
            if culvers['city'] == menards['city'] and culvers['state'] == menards['state']:
                most_widely_spaced_pairs.append((culvers, menards))
                most_widely_spaced_pairs.sort(key=lambda x: dist(x[0], x[1]), reverse=True)
                most_widely_spaced_pairs = most_widely_spaced_pairs[:10]

    print("| Rank | Culver's | Menards | Distance |")
    print("|-|-|-|-|")
    for rank, pair in enumerate(most_widely_spaced_pairs):
        print(f"| {rank+1} | {a(pair[0])} | {a(pair[1])} | {dist(pair[0], pair[1]):.2f} miles |")
