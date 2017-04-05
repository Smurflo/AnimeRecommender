import random
import json
import csv

basePath = "Resources/"


def parseJSON(fname):
    return json.load(open(basePath + fname))


def parseCSV(fname):
    file = basePath + fname
    data = csv.reader(open(file))
    return list(data)


# Remove unrated entries (-1), Remove users with <= (cutoff) ratings
def cleanRatings(data, cutoff):
    cleanData = []
    numRatings = defaultdict(int)

    # remove unrated entries
    for rating in data:
        if int(rating[-1]) == -1:
            # ignore the entry
            continue
        cleanData.append(rating)
        numRatings[rating[0]] += 1

    print("here")

    # remove users with less than (cutoff) ratings
    tooFewEntries = [key for key in numRatings.keys() if numRatings[key] < cutoff]
    for id in tooFewEntries:
        timer.start()
        cleanData = [data for data in cleanData if data[0] != id]

        timer.end("Finished with id " + id)

    # cleanData = [data for data in cleanData if data[0] not in tooFewEntries]
    print("here three")

    return cleanData


def create_ratings_no_unrated():
    lines = list(open(basePath + "rating.csv"))
    toWrite = open(basePath + "ratings_no_unrated.csv", 'w')
    for l in lines:
        if l.startswith("user_id"):
            # header
            toWrite.write(l)
            continue
        if l.__contains__(','):
            info = l.strip().split(',')
        else:
            print("ERROR processing line:")
            print(l)
            info = ""

        if info[2] != '-1':
            toWrite.write(l)


def parseDuration(durationString):
    # turns input string into an int value (number of minutes)
    # input formatted as "X min. per ep." or "X hr. X min."

    durationString = durationString.split(" ")

    if durationString[1] == "min.": # string is formatted as "X min. per ep."
        return int(durationString[0])
    elif durationString[1] == "hr.": # string is formatted as "X hr. X min."
        hours = int(durationString[0])
        minutes = int(durationString[2])
        return (60*hours) + minutes
    else:
        print("ERROR parsing duration: %s" % durationString)

    return -1   # should never get here


def pickRandomUserID(ratings, cutoff=5):
    # selects a user that has at least (cutoff) ratings
    bound = ratings[-1][0]

    while True:
        uid = random.randint(1, bound)
        user_ratings = [r for r in ratings if r[0] == str(uid)]
        if len(user_ratings) >= cutoff:
            return uid


def getRandomUserData(ratings, cutoff=5):
    # selects a user that has at least (cutoff) ratings
    bound = int(ratings[-1][0])

    while True:
        uid = random.randint(1, bound)
        user_ratings = [r for r in ratings if r[0] == str(uid)]
        if len(user_ratings) >= cutoff:
            return user_ratings

# create_ratings_no_unrated()