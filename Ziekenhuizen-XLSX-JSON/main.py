import requests
import json
file = open("ambulanceposten.txt", "r")
lines = file.readlines()
i = 0
ziekenhuizen = []
ziekenhuis = {}
for line in lines:
    line = line.replace("\n", "")
    l = line.split(";")

    if i % 2 is 0:
        ziekenhuis["plaatsnaam"] = l[1]
        post = l[3].split(",")[1].replace(" ", "")
        try:
            loc = requests.get("https://hack-a-train.9292.nl/v1/api/Locations?query={0}".format(post),
                               headers={"Authorization": "Token nGZC03b1F0Z8VI2fG49r"}).json()["Locations"][0]["Coordinate"]
            ziekenhuis["lat"] = loc["Latitude"]
            ziekenhuis["long"] = loc["Longitude"]
        except IndexError:
            pass
    else:
        # print(l[3])
        ziekenhuis["beschikbaarheid"] = (1 if l[3] == "24 uur" else 0)
        ziekenhuizen.append(ziekenhuis)
        ziekenhuis = {}

    i += 1
json.dump(ziekenhuizen,open("ambulances.json","w"))

