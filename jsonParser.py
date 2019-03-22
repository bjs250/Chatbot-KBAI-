import numpy as np
import json

with open("anonymized-reviews-2019-01-03-stub.json", "r",encoding="utf8") as read_file:
    data = json.load(read_file)

# Put the data into buckets by class
d = {}
for review in data["reviews"]:
    course = review["course"]
    difficulty = review["difficulty"]
    workload = review["workload"]
    rating = review["rating"]
    text = review["text"]
    
    if course not in d.keys():
        d[course] = {}
        d[course]["reviews"] = list()
        d[course]["difficulty"] = list()
        d[course]["workload"] = list()
        d[course]["rating"] = list()
        d[course]["text"] = list()

    d[course]["reviews"].append(review)
    d[course]["difficulty"].append(difficulty)
    d[course]["workload"].append(workload)
    d[course]["rating"].append(rating)
    d[course]["text"].append(text)

    # Analyze the text for keywords

# Get aggregate stats
for course in d.keys():
    d[course]["average difficulty"] = np.mean(d[course]["difficulty"])
    d[course]["average workload"] = np.mean(d[course]["workload"])
    d[course]["average rating"] = np.mean(d[course]["rating"])
    
