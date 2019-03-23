import json

class topic:
    def __init__(self, name = None, references = None, occurences = None):
        self.name = name
        self.references = references
        self.occurences = 0

    def getName(self):
        return self.name

    def getReferences(self):
        return self.references

    def getOccurences(self):
        return self.occurences

    def incrementOccurences(self):
        self.occurences += 1
    
    def resetOccurences(self):
        self.occurences = 0

def determine_topic(words,topics):
    # Increase score if word appears in topic
    for word in words:
        for topic in topics:
            if word in topic.getReferences():
                topic.incrementOccurences()
    
    # Return the topic name with the highest score
    maxScore = 0
    bestTopic = ""
    for topic in topics:
        if topic.getOccurences() > maxScore:
            maxScore = topic.getOccurences()
            bestTopic = topic.getName()
        topic.resetOccurences()
    
    return bestTopic

#============================================================

# Load in the OMSCentral data 
with open("anonymized-reviews-2019-01-03-stub.json", "r",encoding="utf8") as read_file:
    data = json.load(read_file)

# Attributes found on every review
standard_attributes = ["difficulty","workload","rating"]

# Attributes that will be found in the text of a review
exams = ["exam","exams"]
proctor = ["proctor","proctored","proctortrack"]
project = ["project","projects"]
group = ["group","team"]

text_attributes = ["exams","proctor","project","group"]

languages = ["python","java","c","r"]

# Put the data into buckets by course...
d = {}
for review in data["reviews"]:
    course = review["course"].lower()
    
    # New course encountered --> initialize data structure
    if course not in d.keys():
        d[course] = {}
        for attribute in standard_attributes:
            d[course][attribute] = list()
        d[course]["text"] = list()
        for attribute in text_attributes:
            d[course][attribute] = 0
        d[course]["languages"] = {}
        for language in languages:
            d[course]["languages"][language] = 0
        d[course]["total reviews"] = 0

    # Add in new data to course
    for attribute in standard_attributes:
        instance = float(review[attribute])
        d[course][attribute].append(instance)
    d[course]["total reviews"] += 1

    # Clean and split the text
    text = review["text"]
    text = text.replace(',','')
    text = text.replace('\n',' ')
    text = text.replace('/',' ')
    text = text.lower()
    d[course]["text"].append(text)
    words = text.split(" ")

    # Analyze the text for keywords
    for word in words:
        for attribute in text_attributes:
            for keyword in attribute:
                if keyword == word:
                    d[course][attribute] += 1
        for language in languages:
            if language == word:
                d[course]["languages"][language] += 1

# Determine aggregate stats by course from the data structure
for course in d.keys():
    d[course]["average difficulty"] = sum(d[course]["difficulty"])/len(d[course]["difficulty"])
    d[course]["average workload"] = sum(d[course]["workload"])/len(d[course]["workload"])
    d[course]["average rating"] = sum(d[course]["rating"])/len(d[course]["rating"])
    d[course]["most popular language"] = max(d[course]["languages"], key=d[course]["languages"].get)
    threshold = 0.1
    for attribute in text_attributes:
        if d[course][attribute]/d[course]["total reviews"] > threshold:
            d[course][attribute+" flag"] = True
        else:
            d[course][attribute+" flag"] = False
    print(course, d[course]["total reviews"])
    for attribute in text_attributes:
        print(attribute,d[course][attribute],d[course][attribute+" flag"])

# Create topics to analyze questions to the agent
workload = topic("workload",["workload","time","allocate"])
new = topic("what a new student should take",["classes","first","new"])
language = topic("programming languages",["python","c","java","r","language"])
when = topic("when to take a class",["before","after","early","late"])
together = topic("taking classes together",["together","with","itself","classes","alone"])
difficulty = topic("class difficulty",["easiest","easy","hard","hardest","difficult"])

exams = topic("exams",["exam","exams","test","tests","midterm","final"])
proctor = topic("proctored exams",["exam","exams","test","tests","midterm","final","proctor","proctored","proctortrack"])
projects = topic("projects",["project","projects"])
group = topic("group projects",["project","projects","group","team","groups","teams","groupwork","teamwork"])

topics = [workload,new,language,when,together,difficulty]

# Sample questions (for debugging)
questions = [
            "Should I take CS-6300 with CS-6505?", # Whether a particular class is best taken on its own or with other classes (together)
            "Can I take CS-6300 and CS-6505 together?",
            "Should I take CS-6300 alone?",
            "Should I take CS-6300 by itself?",
            "Should I take CS-6300 with other classes?",
            "How much time does CS-6300 take?", # What amount of time a particular class requires. (workload) x
            "How much time should I allocate for CS-6300?",
            "How's the workload for CS-6300?",
            "What classes should a new student take first?", # What classes a new student should consider taking first. (new)
            "What is the easiest class?", # difficulty
            "What is the hardest class?",
            "What is the most difficult class?",
            "What is the least difficult class?",            
            "Should I take CS-6300 before CS-6505?", # Whether the class should be taken early or late in the program. (when)
            "Should I take CS-6300 after CS-6505?",
            "Should I take CS-6300 early in the program?",
            "Should I take CS-6300 late in the program?",            
            "What language is CS-6300 taught in?", # What programming languages a particular class requires. (language)
            "Is CS-6300 taught in Python?",
            "Do I need to know Java for CS-6505?",
            "Does CS-6300 have exams?", # Whether a given course requires projects, proctored exams, team projects, etc.
            "Are there exams in CS-6300?",
            "Are the exams in CS-6300 proctored?",
            "Does CS-6300 have projects?",
            "Are there projects in CS-6300?",
            "Are there group projects in CS-6300?",            
            "Is grad algo still hard?" # Fun/Robustness
            ] 

# Determine topic of a given question
for question in questions:
    question = question.replace("?","")
    question = question.lower()
    words = question.split(" ")
    topic = determine_topic(words,topics)

    # Respond based on topic
    if topic == workload.getName():
        #print(topic,"|",question)
        for word in words:
            if word in d.keys():
                pass
                #print("-----It sounds like you're asking about the " + topic + " for " + word.upper())
                #print("-----It appears to be around " + str(d[word]["average workload"]) + " hours per week on average")           
    elif topic == language.getName():
        print(topic,"|",question)
        for word in words:
            if word in d.keys():
                print("-----It sounds like you're asking about the " + topic + " for " + word.upper())
                print("-----It appears to be " + d[word]["most popular language"])  

"""
print("\nHello! You are speaking the OMSCS advising bot. Feel free to ask me some questions. (If you'd like to quit, enter 'quit')")
userInput = ""
while userInput != "quit":
    userInput = input("> ")
    userInput = userInput.replace("?","")
    userInput = userInput.lower()
    words = userInput.split(" ")
    topic = determine_topic(words,topics)
    print(topic)

"""
