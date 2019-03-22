import numpy as np
import json

with open("anonymized-reviews-2019-01-03-stub.json", "r",encoding="utf8") as read_file:
    data = json.load(read_file)

# Define corpus attributes 
languages = ["python","java","c","r"]
first = ["first"]
background = ["background"]
exams = ["exam","exams"]
project = ["project"]
team = ["team"]

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
        d[course]["languages"] = {}
        for language in languages:
            d[course]["languages"][language] = 0
    

    d[course]["reviews"].append(review)
    d[course]["difficulty"].append(difficulty)
    d[course]["workload"].append(workload)
    d[course]["rating"].append(rating)
    d[course]["text"].append(text)

    # Analyze the text for keywords
    text = text.replace(',','')
    text = text.replace('\n',' ')
    text = text.replace('/',' ')

    text = text.lower()
    words = text.split(" ")

    for word in words:
        for language in languages:
            if language == word:
                #print("\n",language,"============================\n")
                #print(text) 
                d[course]["languages"][language] += 1

#print(d.keys())

# Get aggregate stats
for course in d.keys():
    d[course]["average difficulty"] = np.mean(d[course]["difficulty"])
    d[course]["average workload"] = np.mean(d[course]["workload"])
    d[course]["average rating"] = np.mean(d[course]["rating"])
    #print(course,d[course]["languages"])
    d[course]["most popular language"] = max(d[course]["languages"], key=d[course]["languages"].get)
    #print(d[course]["most popular language"])

# Sample questions
questions = [
            "Should I take CS-6300 with CS-6505?", # Whether a particular class is best taken on its own or with other classes
            "Can I take CS-6300 and CS-6505 together?",
            "Should I take CS-6300 alone?",
            "Should I take CS-6300 by itself?",
            "Should I take CS-6300 with other classes?",
            "How much time does CS-6300 take?", # What amount of time a particular class requires.
            "How much time should I allocate for CS-6300?",
            "How's the workload for CS-6300?",
            "What classes should a new student take?", # What classes a new student should consider taking first.
            "What is the easiest class?",
            "What is the hardest class?",
            "What is the most difficult class?",
            "What is the least difficult class?",            
            "Should I take CS-6300 before CS-6505?", # Whether the class should be taken early or late in the program.
            "Should I take CS-6300 after CS-6505?",
            "What language is CS-6300 taught in?" # What programming languages a particular class requires.
            ] 
