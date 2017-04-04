import map
import repoze.lru as functools

def evtLoc(bus):
    return bus["coordinates"]["latitude"], bus["coordinates"]["longitude"]

def approxPathHelper(curr, arr, order):
    if len(arr) <= 0:
        return
    pushMe = arr[0]
    min = map.durBetween(curr, evtLoc(arr[0]));
    for x in arr:
        timeBetween = map.durBetween(curr, evtLoc(x))
        if timeBetween < min:
            min = timeBetween
            pushMe = x
    curr = pushMe
    arr.remove(pushMe)
    order.append(pushMe)
    approxPathHelper(curr, arr, order)
    
def approxPath(start, arr):
    order = []
    approxPathHelper(start, arr, order)
    return order

def getEvents(home, arr, hours, days):
    i = 0
    eventTime = 1
    result = []
    while(days > 0 and i < len(arr)):
        result.append([])
        todayHours = hours
        todayHours -= map.durBetween(home, evtLoc(arr[i]))
        while(todayHours > 0):
            todayHours -= eventTime
            timeToHere = map.durBetween(home, evtLoc(arr[i]))
            timeToNext = map.durBetween(evtLoc(arr[i]), evtLoc(arr[i+1]))
            if todayHours - timeToHere < 0 or todayHours - timeToNext < 0:
                break
            todayHours -= timeToNext
            result[-1].append(arr[i])
            i += 1
        days -= 1
    betterResult = []
    for x in result:
        betterResult.append(approxPath(home, x))
    return betterResult