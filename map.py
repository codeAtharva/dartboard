from urllib import urlencode, quote
import requests
import json
import collections
import repoze.lru as functools
import configKeys

start = "Half Moon Bay High School"
end = "530 Ferdinand Avenue, Half Moon Bay"

BING_MAPS_KEY = configKeys.bms

def gen_waypoint(loc):
    if isinstance(start, collections.Sequence) and len(loc) == 2:
        return "{},{}".format(loc[0], loc[1])
    else:
        return loc

def route(start, end):
    args  = {"key": BING_MAPS_KEY}
    args["wp.1"] = gen_waypoint(start)
    args["wp.2"] = gen_waypoint(end)
    url = "http://dev.virtualearth.net/REST/v1/Routes?" + urlencode(args)
    resp = requests.get(url)
    if resp.ok:
        json = resp.json()
        if json["statusCode"] == 200:
            return True, json
    return False, None

def getImage(home, locs):
    args = {"key": BING_MAPS_KEY}
    args["wp.0"] = home + ";0;start"
    for i, loc in enumerate(locs):
        args["wp.{}".format(i+1)] = gen_waypoint(loc) +";48;{}".format(i+1)
    args["wp.{}".format(i+2)] = args["wp.0"]
    return "http://dev.virtualearth.net/REST/v1/Imagery/Map/Road/Routes?" + urlencode(args).replace("%3B", ";")

def genMapLink(home, locs):
    link = "http://bing.com/maps/default.aspx?rtp=adr." + quote(home)
    for loc in locs:
        link += "~pos." + str(loc["coordinates"]["latitude"]) + "_" + str(loc["coordinates"]["longitude"])
    link += "~adr." + quote(home)
    return link

def durBetween(start, end):
    return travelDur(route(start, end)[1])

def travelDur(route):
    if route == None:
        return 0
    routeInfo = route["resourceSets"][0]["resources"][0]
    return float(routeInfo["travelDuration"])/60.0/60.0 # duration in hours