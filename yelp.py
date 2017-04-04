from yelpapi import YelpAPI
import repoze.lru as functools
import configKeys

# Yelp Key
@functools.lru_cache(128)
def businesses(city):
    CLIENT_ID = configKeys.ci
    CLIENT_SECRET = configKeys.cs
    api = YelpAPI(CLIENT_ID, CLIENT_SECRET)
    res = api.search_query(location=city, sort_by='rating', categories="arts", limit=30)
    return res["businesses"]