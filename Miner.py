import urllib.request
import json
import time
from bs4 import BeautifulSoup


def parseData(fname):
    for l in urllib.request.urlopen(fname):
        yield eval(l)

def stripNonNumeric(val):
    return ''.join([c for c in val if c in '1234567890.'])

start_time = time.time()

# Extract all ids, so we can scrape the data with BeautifulSoup
print("Reading data...")
dataFile = open("C:/Users/Kyle/PycharmProjects/CSE158/Resources/anime.csv", encoding="utf8")
header = dataFile.readline()
fields = ["constant"] + header.strip().replace('"', '').split(',')
ids = []
for l in dataFile:
    ids.append(l.split(',')[0])
print("done")

animeInfo = {}
numDone = 0

# Scrape info for all 12294 anime
for id in ids:
    try:
        url = "https://myanimelist.net/anime/" + id
        # print(url)

        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")
        soup.prettify()

        animeInfo[id] = {}  # init empty dict for this entry

        # get the title
        title = soup.find("span", {"itemprop": "name"}).text
        animeInfo[id]["Title"] = title

        # Extract rating, type, episodes, status(?), aired, producers (list), licensors (list),
        #   studios (list), genres (list), duration, rating [from Information section]
        # Extract score, ranked, popularity, members, favorites [from Statistics section]
        # Alternative Titles? (e.g english version of title)

        desiredCategories = ["Episodes", "Type", "Status", "Aired", "Producers", "Licensors",
                             "Studios","Genres", "Duration", "Rating", "Score", "Ranked",
                             "Popularity", "Members", "Favorites"]
        listCategories = ["Producers", "Licensors", "Studios", "Genres"]
        additionalCleanupCategories = ["Score", "Ranked", "Popularity", "Episodes"]
        firstStatus = True  # there are two status labels, we want the second one
        status = "Status"

        infoDiv = (soup.find("td", {"class" : "borderClass"})).div
        # infoDivs = soup.findAll("div", {"class" : "spaceit"})
        infoDivs = soup.findAll("div")

        for div in infoDivs:
            text = div.text
            textList = [t.strip() for t in text.split(":")]
            category = textList[0]
            if category in desiredCategories:  # only get the stuff from desired categories

                if category == status and firstStatus:  # ignore the first status we see
                    firstStatus = False
                    continue

                if category in listCategories:
                    info = [t.strip() for t in textList[1].split(",")]
                else:
                    info = textList[1]

                # Clean up some categories
                if category == "Score":
                    score = info.split(" ")[0]  # strip off extra stuff
                    score = score[:-1]          # strip off extra 1 at the end
                    info = score
                elif category == "Ranked":
                    info = info.split("\n")[0]   # strip off extra stuff
                    info = stripNonNumeric(info)
                elif category == "Popularity" or category == "Members" or category == "Favorites"\
                        or category == "Episodes":
                    info = stripNonNumeric(info)

                animeInfo[id][category] = info

        # get the synopsis
        try:
            synopsis = soup.find("span", {"itemprop": "description"}).text
        except AttributeError:  # if there's no description
            synopsis = ""
        animeInfo[id]["Synopsis"] = synopsis

        numDone += 1

        if numDone % 250 == 0:
            print("Done scraping " + str(numDone))
            totaltime = time.time() - start_time
            print("--- %s seconds ---" % totaltime)
            rate = totaltime / numDone
            timeRemaining = (rate * (len(ids) - numDone)) / 3600
            print("--- %s hours left (%s sec/page) ---" % (timeRemaining, rate))



        # if numDone > 5:
        #     break
    except:
        print("problem with id = " + id)
        continue

# save the dict as json
with open('C:/Users/Kyle/PycharmProjects/CSE158/Resources/anime.json', 'w') as fp:
    json.dump(animeInfo, fp, sort_keys=True, indent=2)

print("--- %s seconds ---" % (time.time() - start_time))

print("Done!")

