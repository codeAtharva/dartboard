from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file
import os
from map import getImage, route, genMapLink
import repoze.lru as functools
import urllib

#app = Flask(__name__)
app = Flask(__name__, static_url_path = "", static_folder = "static")

#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Main page
@app.route("/")
def index():
    return render_template("index.html")

@app.template_filter('rangeFilter')
def reverse_filter(s):
    return range(len(s))

# generate event list
import timing, yelp

def genEventList(location, days, hours):
    try:
        if route(location, location)[0]:
            events = timing.getEvents(location, yelp.businesses(location), hours, days)
            return True, events
        return False, None
    except:
        return False, None

# Trip display
@app.route("/trip", methods=["GET"])
def trip():
    try:
        place = request.args.get("place")
        days = int(request.args.get("quantityDays"))
        hours = int(request.args.get("quantityHours"))
        success, eventList=genEventList(place, days, hours)
        if place == "":
            return render_template("error.html", error="Please enter a location")
        elif hours > 12:
            return render_template("error.html", error="Sorry, too many hours")
        elif days > 14:
            return render_template("error.html", error="Sorry, too many days")
        elif not success:
            return render_template("error.html", error="Sorry, invalid city")
        return render_template("trip.html", home=place, eventList=eventList)
    except:
        return render_template("error.html", error="Sorry, this location is not currently supported")

# image processing
imageLinkTable = []

@functools.lru_cache(128)
def imageLink(a):
    imageLinkTable.append(a)
    return "/map/{}".format(len(imageLinkTable) - 1)

@app.route("/map/<home>/<coordList>")
def mapImg(home, coordList):
    coordList = [float(x) for x in coordList.split(",")]
    coordList = zip(coordList[::2], coordList[1::2])
    urlFile = urllib.urlopen(getImage(home, coordList))
    return send_file(urlFile, urlFile.info().gettype())

@app.context_processor
def utility_processor():
    def format_image(home, day):
        return "/map/" + urllib.quote(home) + "/" + ",".join([str(x) for b in day for x in (b["coordinates"]["latitude"], b["coordinates"]["longitude"])])
    def map_link(home, day):
        return genMapLink(home, day)
    return dict(format_image=format_image, map_link=map_link)
    
if __name__ == "__main__":
    # Specifically for Cloud9, remove for production
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))