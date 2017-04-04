import eventful

EVENTFUL_API_KEY = "htRqcVMMsFsD2QxV"

def events(city):
    api = eventful.API(EVENTFUL_API_KEY)
    events = api.call('/events/search', l=city)
    return events['events']['event']

for event in events("Los Angeles"):
        print "%s at %s" % (event['title'], event['venue_name'])