"""
Project 3

ADD YOUR CODE HERE

Please read project directions before importing anything
"""
from project import project
from projects import projects

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

class StudentAgent:
    """ADD YOUR CODE HERE"""

    def __init__(self, verbose):
        self._verbose = verbose
        self.green_words = ['project','projects','assignment','assignments','midterm','final','course','announcements','instructor','report','reports','exams','strategies', \
            'exams','strategies','strategy','policy','peer-feedback','office-days','content','communication','submissions','TA','component','code','policies']
        self.nouns = ['AI','piazza','yaroslav','monday','tuesday','slack','python','wednesday','ashok','canvas','thursday','pdf','goel','learning', \
            'friday','start','everyday','saturday','litvak','sunday','procedure','class','reading-list','week','java','weeks','class-grade','videos','morning', \
            'hours','reading','midnight','list','video','human','classroom','book','available','example','docx','files','text','attendance','method','file','planning' \
            'self-reflection', 'cognition','credit','0-100','collaboration','I','zip','grade','work']
        
        self.start = topic('start',['start','begin'])
        self.end = topic('end',['end','due'])
        self.submission_type = topic('submission type',['zip','docx','pdf'])
        self.submission_location = topic('submission location',['canvas'])
        self.topics = [self.start,self.end,self.submission_type,self.submission_location]
        self.projects = projects()

    def load_syllabus(self, list_of_list_of_statement_words):
        """Train agents from statements"""

        for _statement in list_of_list_of_statement_words:
            #print("unmodified: ",_statement.lower().split(' '))

            words = _statement.lower().split(' ')
            #1 Get the green word
            green_word = ""
            for word in words:
                if word in self.green_words:
                    green_word = word

            #print(green_word)
            if green_word == "project":
                print(words)
                
                # Dynamically create an instance 
                # of class based on information present
                module_ = __import__(green_word)
                class_ = getattr(module_, green_word)
                instance = class_()
                if hasattr(instance,"name"):
                    instance.find_and_set_name(words)
                    #print("name:",instance.name)

                # Check if such an instance already exists in the collection
                if instance.name in self.projects.getReferences():
                    #print("old object")
                    instance = self.projects.getReference(instance.name)
                else:
                    #print("new object created")
                    self.projects.addReference(instance)
                    self.projects.setCount(self.projects.getCount() + 1)
                    #print("count:",self.projects.getCount())

                #print(vars(instance))
                # Update the instance with information present from the statement
                words.remove(green_word)
                words.remove(instance.name)

                topic = self.determine_topic(words)
                #print("topic:",topic)

                if topic == "start":
                    instance.find_and_set_start(words)
                if topic == "end":
                    instance.find_and_set_end(words)
                print(vars(instance))

    def input_output(self, word_list):
        """takes in list of words, returns question_object and data_requested"""

        green_word = ""
        #print(word_list) # for debugging only
        for word in word_list:
            if word in self.green_words:
                green_word = word

        if green_word is "":
            return "idk"

        # TODO: Add your code here

        #_answer = "no" # NO - for debugging only, replace with your code
        #_answer = "idk"  # I do not know
        #_answer = "yes"  # YES
        _answer = "no"

        return _answer

    def determine_topic(self,words):
        # Increase score if word appears in topic
        for word in words:
            for topic in self.topics:
                if word in topic.getReferences():
                    topic.incrementOccurences()
        
        # Return the topic name with the highest score
        maxScore = 0
        for topic in self.topics:
            if topic.getOccurences() > maxScore:
                maxScore = topic.getOccurences()
                bestTopic = topic.getName()
            topic.resetOccurences()
        
        return bestTopic