import Timer as timer
import timeit
import json
import csv
import random
import urllib.request
from sklearn import svm
from collections import defaultdict
from bs4 import BeautifulSoup


basepath = "C:/Users/Kyle/PycharmProjects/CSE158/Resources/"
list_url = "https://myanimelist.net/animelist/"
mal_username = "Smurflo"   # default to my personal list for now
# user_id = 51614  # TODO update this so it's random (avg num of entries: 106)
user_id = 1  # TODO update this so it's random (avg num of entries: 106)

def parseJSON(fname):
    return json.load(open(basepath + fname))


def parseCSV(fname):
    file = basepath + fname
    data = csv.reader(open(file))
    return list(data)


def calcMSE(predictions, actual):
    if len(predictions) != len(actual):
        print("ERROR: length of predictions and actual do not match (in MSE calc)")

    SE = 0
    for i in range(len(predictions)):
        dif = predictions[i] - actual[i]
        SE += dif**2
    return SE/len(predictions)


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



def animeToFeature(anime_id):
    info = anime[anime_id]
    feat = [1]  # bias term

    feat.append(int(info["Episodes"]))
    feat.append(int(info["Favorites"]))
    feat.append(int(info["Members"]))
    feat.append(int(info["Popularity"]))
    feat.append(int(info["Ranked"]))
    feat.append(float(info["Score"]))

    # TODO add duration, aired date, genres, licensors, producers, rating, status, studios, synopsis, type

    return feat

# read the data
timer.start()
print("Reading data...")
anime = parseJSON("anime.json")

ratings = parseCSV("rating.csv")
header = ratings[0]
ratings = ratings[1:]
timer.end("Done reading data")

# timeit.timeit(cleanRatings(ratings, 5))

# print(ratings[:100])
# ratings = cleanRatings(ratings, 5)
# print(ratings[:100])

# get training set and test set
# TODO handle -1 entries here
user_data = [r for r in ratings if r[0] == str(user_id)]
random.shuffle(user_data)
x = [animeToFeature(r[1]) for r in user_data]
y = [int(r[2]) for r in user_data]
numTrain = int(0.9*len(x))
x_train = x[:numTrain]
y_train = y[:numTrain]
x_test = x[numTrain:]
y_test = y[numTrain:]

print(numTrain)
print(x_train)
print(y_train)
print(user_data)
print(y_test)

# start prediction task
c_values = [0.00001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 1000000]
bestMSE = 10000
bestC = 10
for c in c_values:
    clf = svm.SVC(C=c)
    clf.fit(x_train, y_train)

    # validation_predictions = clf.predict([wordFeat(v) for v in validation])
    test_predictions = clf.predict(x_test)
    # acc = calculateAccuracy(validation_predictions, validation_actual_cat)
    mse = calcMSE(test_predictions, y_test)
    print("C:",c,"- MSE:", mse)

    if mse < bestMSE:
        bestMSE = mse
        bestC = c

print("bestC: " + str(bestC))
print("bestMSE: " + str(bestMSE))





# user_data = [d for d in ratings if d[1] == "1" and d[2] == "2"]
# potentially_me = [d[0] for d in user_data]
# print(potentially_me)
# print(len(potentially_me))
# print(header)
#
# for id in potentially_me:
#     print(id)
#     r = [r for r in ratings if r[0] == id]
#     print(r)
#     print(len(r))

# get data for the user we're interested in
# url = list_url + mal_username
# page = urllib.request.urlopen(url).read()
# soup = BeautifulSoup(page, "html.parser")
# soup.prettify()

# will be a list of (anime_id, rating) tuples (want watching(1), completed(2), dropped(4))
# user_data = []
# table = soup.find("table")["data-items"]
#
# print(table.split("{"))








