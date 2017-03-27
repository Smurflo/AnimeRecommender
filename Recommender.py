import Timer as timer
import json
import csv
from numpy import genfromtxt


basepath = "C:/Users/Kyle/PycharmProjects/CSE158/Resources/"
timer.start()

def parseJSON(fname):
    return json.load(open(basepath + fname))


def parseCSV(fname):
    file = basepath + fname
    data = csv.reader(open(file))
    return list(data)


timer.start()
print("Reading data...")
anime = parseJSON("anime.json")

ratings = parseCSV("rating.csv")
timer.end("Done reading data")







