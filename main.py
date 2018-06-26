import asyncio
import json
import websockets
import ERParser
import importlib
import geopy
import geopy.distance

hospitals = json.load(open("ambulances.json"))
ambulanceposts = [(a["lat"], a["long"]) for a in hospitals]

pts = [geopy.Point(p[0], p[1]) for p in ambulanceposts]


async def main():
    async with websockets.connect('ws://monitor.livep2000.nl/A/websocket') as webs:
        ## Start Connection
        await webs.send('{"TYP":"ANN","COO":"5db18e81-901f-42f5-ae96-1c5511341aba","UID":"6698853","COM":6}')
        await webs.recv()

        ## Send Start
        await webs.send('{"FRQ":true,"COM":12}')
        await webs.recv()

        while True:
            websocket_data = json.loads(await webs.recv())
            if isinstance(websocket_data, dict):
                pass
            else:
                importlib.reload(ERParser)
                lat, long = ERParser.parse(websocket_data)
                if lat is not None:
                    onept = geopy.Point(lat, long)
                    alldist = [(p, geopy.distance.distance(p, onept).km) for p in pts]
                    nearest_point = min(alldist, key=lambda x: (x[1]))[0]
                    print(onept.latitude, onept.longitude, nearest_point.latitude, nearest_point.longitude)
                    print("https://www.google.nl/maps/dir/{0},{1}/{2},{3}/@{0},{1},18z".format(onept.latitude,
                                                                                               onept.longitude,
                                                                                               nearest_point.latitude,
                                                                                               nearest_point.longitude))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
