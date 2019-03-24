import json
import operator

class topic:
    def __init__(self, name, singleDescription, multipleDescription, noDescription, references, occurences = None):
        self.name = name
        self.references = references
        self.occurences = 0
        self.singleDescription = singleDescription
        self.multipleDescription = multipleDescription
        self.noDescription = noDescription

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

    def getNoDescription(self):
        return self.noDescription

    def getSingleDescription(self):
        return self.singleDescription
    
    def getMultipleDescription(self):
        return self.multipleDescription

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
            bestTopic = topic
        topic.resetOccurences()
    
    return bestTopic

def handleResponse(topic,topicDict,words,d): # This function needs to be refactored
    courses = list()
    courseString = ""
    for word in words:
        if word in d.keys():
            courses.append(word)
    response = ""

    if len(courses) == 0:
        pass
    elif len(courses) == 1:
        courseString = courses[0]
    elif len(courses) == 2:
        for course in courses:
            courseString += course + ","
        courseString = courseString[:-1]
    
    #print(topic.getName())
    response = ""

    if topic.getName() == topicDict["together"].getName():
        # 0
        if len(courses) == 0:
            response = "The following are good choices based on workload: \n"
            
            diffDict = {course:d[course]["average workload"] for course in d.keys()}
            sorted_diffDict = sorted(diffDict.items(), key=operator.itemgetter(1)) 
            for i in range(5):
                response += sorted_diffDict[i][0] + ", workload: " + format(sorted_diffDict[i][1],'.2f') + " hours\n"

        # 1
        elif len(courses) == 1:
            response = "The workload is around " + format(d[courseString]["average workload"],'.2f') + " hours per week. "
            if d[courseString]["average workload"] > 10:
                response += " You should probably not take other courses"
            else:
                response += " You may be able to fit another course in"
        # 2
        elif len(courses) > 1:
            totalWorkload = 0
            for course in courses:
                totalWorkload += d[course]["average workload"]
            response = "The total workload is around " + format(totalWorkload,'.2f') + " hours per week. "
            if totalWorkload > 25:
                response += " It's your funeral if you decide to do it"
            else:
                response += " It might be manageable"

    elif topic.getName() == topicDict["workload"].getName():
        # 0
        if len(courses) == 0:
            diffDict = {course:d[course]["average workload"] for course in d.keys()}
            sorted_diffDict = sorted(diffDict.items(), key=operator.itemgetter(1)) 
            response = "These classes have the easiest workload: \n"
            for i in range(5):
                response += sorted_diffDict[i][0] + ", workload: " + format(sorted_diffDict[i][1],'.2f') +"\n"
            response += "These classes have the hardest workload: \n"
            for i in range(1,6):
                response += sorted_diffDict[-i][0] + ", workload: " + format(sorted_diffDict[-i][1],'.2f') +"\n"
        # 1
        elif len(courses) == 1:
            response = "The workload is around " + format(d[courseString]["average workload"],'.2f') + " hours per week. "
    
    elif topic.getName() == topicDict["new"].getName():
        # 0
        if len(courses) == 0:
            response = "The following are good choices based on difficulty: \n"
            
            diffDict = {course:d[course]["average difficulty"] for course in d.keys()}
            sorted_diffDict = sorted(diffDict.items(), key=operator.itemgetter(1)) 
            for i in range(5):
                response += sorted_diffDict[i][0] + ", difficulty: " + format(sorted_diffDict[i][1],'.2f') +"\n"
    
    elif topic.getName() == topicDict["when"].getName():
        # 1
        if len(courses) == 1:
            response = "The workload is around " + format(d[courseString]["average workload"],'.2f') + " hours per week. \n"
            if d[courseString]["average workload"] > 10:
                response += "For that reason, this course is best taken late in the program"
            else:
                response += "For that reason, this course is best taken early in the program"

        # 2
        if len(courses) == 2:
            diffDict = {course:d[course]["average workload"] for course in courses}
            sorted_diffDict = sorted(diffDict.items(), key=operator.itemgetter(1))
            response = "The lower workload is " + sorted_diffDict[0][0] + ", so you should take it."
            
    elif topic.getName() == topicDict["language"].getName():
        # 1
        if len(courses) == 1:
            response = "Most students in the course use " + d[courseString]["most popular language"]
        
    elif topic.getName() == topicDict["exams"].getName():
        # 1
        if len(courses) == 1:
            if d[courseString]["exam flag"]:
                response = "Yeah, there are exams"
            else:
                response = "No exams"  

    elif topic.getName() == topicDict["proctor"].getName():
        # 1
        if len(courses) == 1:
            if d[courseString]["proctor flag"]:
                response = "Yup, there are exams and they are proctored"
            else:
                response = "No"  

    elif topic.getName() == topicDict["project"].getName():
        # 1
        if len(courses) == 1:
            if d[courseString]["project flag"]:
                response = "Yes, there are projects"
            else:
                response = "No, there are no projects"  

    elif topic.getName() == topicDict["group"].getName():
        # 1
        if len(courses) == 1:
            if d[courseString]["group flag"]:
                response = "Yeah, there's groupwork"
            else:
                response = "No groupwork"  

    print(response + "\n")

# Main ============================================================

# Load in the OMSCentral data 
with open("anonymized-reviews-2019-01-03.json", "r",encoding="utf8") as read_file:
    data = json.load(read_file)

# Attributes found on every review
standard_attributes = ["difficulty","workload","rating"]

# Attributes that will be found in the text of a review
exam = ["exam","exams"]
proctor = ["proctor","proctored","proctortrack"]
project = ["project","projects"]
group = ["group","team"]

text_attributes = [exam,proctor,project,group]

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
            d[course][attribute[0]] = 0
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
                    d[course][attribute[0]] += 1
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
        if d[course][attribute[0]]/d[course]["total reviews"] > threshold:
            d[course][attribute[0]+" flag"] = True
        else:
            d[course][attribute[0]+" flag"] = False
        #print(course,attribute[0],d[course][attribute[0]],d[course]["total reviews"],d[course][attribute[0]]/d[course]["total reviews"],d[course][attribute[0]+" flag"])
        
# Create topics to analyze questions to the agent
topicDict = {}
topicDict["workload"] = topic("workload","workload","","",["workload","time","allocate"])
topicDict["new"] = topic("new classes","if a new student should take","","what classes a new student should take",["classes","first","new"])
topicDict["language"] = topic("language","programming languages","","",["python","c","java","r","language"])
topicDict["when"] = topic("when","when is a good time","","",["before","after","early","late"])
topicDict["together"] = topic("together","workload when taking other classes together","","",["together","with","itself","classes","alone"])
topicDict["difficulty"] = topic("difficulty","class difficulty","","",["easiest","easy","hard","hardest","difficult"])

topicDict["exams"] = topic("exams","exams","","",["exam","exams","test","tests","midterm","final"])
topicDict["proctor"] = topic("proctor","proctored exams","","",["proctor","proctored","proctortrack","exams"])
topicDict["project"] = topic("project","projects","","",["project","projects"])
topicDict["group"] = topic("group projects","group projects","","",["group","team","groupwork"])

if 0:
    # Sample questions (for debugging)
    questions = [
        "What classes should I take together", #together, 0
        "Should I take CS-6300 alone?", #together, 1
        "Should I take CS-6300 with CS-6505?", #together, 2 no
        "Ok so what about taking CS-6440 with CS-6300?", #together, 2 yes
        "What class has the best workload?", # workload 0
        "How much time does CS-6340 take?", # workload 1
        "What classes should a new student take first?", # new 0
        "Should I take CS-6300 before CS-6505?", # when 2
        "Should I take CS-7637 after CS-6505?", # when 2
        "Should I take CS-6300 early in the program?", # when 1
        "Is CS-7637 taught in Python?", # language 1
        "Do I need to know Java for CS-6505?", # language 1
        "Does CS-7637 have exams?", #exams
        "Are there projects in CS-7637?", #projects
        "Is there groupwork in CS-7637?" #groupwork
    ]

    # Determine topic of a given question
    for question in questions:
        question = question.replace("?","")
        question = question.lower()
        words = question.split(" ")
        topic = determine_topic(words,topicDict.values())
        print(question)
        handleResponse(topic,topicDict,words,d)
        print("")

print("\nHello! You are speaking the OMSCS advising bot. Feel free to ask me some questions. (If you'd like to quit, enter 'quit')")
userInput = ""
while userInput != "quit":
    userInput = input("> ")
    userInput = userInput.replace("?","")
    userInput = userInput.lower()
    if userInput == "quit":
        print("Goodbye")
        break
    words = userInput.split(" ")
    topic = determine_topic(words,topicDict.values())
    if topic != "":
        handleResponse(topic,topicDict,words,d)
    else:
        print("I don't understand what you're asking")