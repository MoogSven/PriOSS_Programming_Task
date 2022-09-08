import folium
import requests
import json

# load city location dataset
cities_location = requests.get(
    "https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json"
).json()

# TODO: use different cities data set with the same city names as in the dataset.
with open("loginsample.json") as f:
    text = f.read()
    text = text.replace("Munchen", "Munich")
    text = text.replace("Dusseldorf", "Düsseldorf")
    dataset = json.loads(text)
print(dataset)


# create a City to location dict for the used cities, also count how often the city is present.

city_dict = dict()

for activity in dataset["account_activity"]:
    if activity["city"] not in city_dict:
        city_dict[activity["city"]] = dict()
        
        city_dict[activity["city"]]["country"] = activity["country"]
        city_dict[activity["city"]]["count"] = 1
    else:
        city_dict[activity["city"]]["count"] += 1

cities_location = filter(lambda item: item["name"] in city_dict and item["country"] == city_dict[item["name"]]["country"], cities_location)


for city in cities_location:
    city_dict[city["name"]]["location"] = [city["lat"], city["lng"]]
    
print(city_dict)

m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)
for name, city in city_dict.items():
    print(city)
    folium.CircleMarker(location=city["location"], radius=city["count"]*10 , fill=True, popup=f'{name}\n{city["count"]}').add_to(m)


m.save("index.html")
