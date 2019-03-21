"""
Project 3

ADD YOUR CODE HERE

Please read project directions before importing anything
"""
from project import project
from assignment import assignment

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
            'exams','strategy','policy','peer-feedback','office-days','content','communication','submissions','TA','component','code','policies']        
        self.nouns = ['AI','piazza','yaroslav','monday','tuesday','slack','python','wednesday','ashok','canvas','thursday','pdf','goel','learning', \
            'friday','start','everyday','saturday','litvak','sunday','procedure','class','reading-list','week','java','weeks','class-grade','videos','morning', \
            'hours','reading','midnight','list','video','human','classroom','book','available','example','docx','text','attendance','method','file','planning' \
            'self-reflection', 'cognition','credit','0-100','collaboration','I','zip','grade','work']
        self.start = topic('start',['start','begin','get','released'])
        self.end = topic('end',['end','due'])
        self.submission_type = topic('submission_type',['zip','docx','pdf','files'])
        self.submission_location = topic('submission_location',['canvas','piazza'])
        self.grade = topic('grade',['worth','contribute'])
        self.duration = topic('duration', ['complete','finish'])
        self.late_policy = topic('late',['late','credit'])
        
        self.topics = [self.start,self.end,self.submission_type,self.submission_location,self.grade,self.duration,self.late_policy]

        self.d = {}

    def load_syllabus(self, list_of_list_of_statement_words):
        """Train agents from statements"""

        for _statement in list_of_list_of_statement_words:
            
            words = _statement.lower().split(' ')
            # Get the green word
            green_word = ""
            for word in words:
                if word in self.green_words:
                    green_word = word

            #print(green_word)
            if green_word == "project" or green_word == "assignment": # singular
                print("======Sentence:",words)

                # Create a new list in the object dictionary
                if green_word not in self.d:
                    self.d[green_word] = {}
                
                # Dynamically create an instance of class based on information present
                module_ = __import__(green_word)
                class_ = getattr(module_, green_word)
                instance = class_()
                if hasattr(instance,"name"):
                    instance.find_and_set_name(words)
    
                # Check if such an instance already exists in the collection
                names = [name for name in self.d[green_word].keys()]
                if instance.name in names:
                    #print("old object")
                    instance = self.d[green_word][instance.name]
                else:
                    #print("new object created")
                    self.d[green_word][instance.name] = instance
                    instance.incrementCount()
                    #print("count:",instance.getCount())

                # Update the instance with information present from the statement
                words.remove(green_word)
                words.remove(instance.name)

                topic = self.determine_topic(words)
                instance.find_and_set(topic,words,self.nouns)
            
            if green_word == "projects" or green_word == "assignments":
                print("======Sentence:",words)

                singular = green_word[:-1]
                module_ = __import__(singular)
                class_ = getattr(module_, singular)
                instance = class_()
                words.remove(green_word)
                topic = self.determine_topic(words)
                instance.find_and_set(topic,words,self.nouns)
                #print("submission type:",instance.submission_type)
                #print("submission location:",instance.submission_location)

        print("======")
        print(self.d)

        print("==project==")
        for name in self.d["project"].keys():
            print(vars(self.d["project"][name]))
        print("submission type:",project.submission_type)
        print("submission location:",project.submission_location)
        print("count:",project.count)

        print("==assignment==")
        for name in self.d["assignment"].keys():
            print(vars(self.d["assignment"][name]))
        print("submission type:",assignment.submission_type)
        print("submission location:",assignment.submission_location)
        print("count:",assignment.count)

        print("=============Post Processing================")        

        # Post Processing
        for green_word_dict in self.d.items():
            for obj_tuple in green_word_dict[1].items():
                obj = obj_tuple[1]
                if hasattr(obj,"duration") and getattr(obj,"start") is not None and getattr(obj,"end") is not None:
                    obj.calculateDuration()
                    print(vars(obj))
        print("=============Done Training================")
        

    def input_output(self, words):
        """takes in list of words, returns question_object and data_requested"""

        green_word = ""
        for word in words:
            if word in self.green_words:
                green_word = word

        if green_word is "":
            return "idk"

        if green_word == "project" or green_word == "assignment": # singular
            print("======Sentence:",words)

            # Create a new list in the object dictionary
            if green_word not in self.d:
                self.d[green_word] = {}
            
            # Dynamically create an instance of class based on information present
            module_ = __import__(green_word)
            class_ = getattr(module_, green_word)
            instance = class_()
            if hasattr(instance,"name"):
                instance.find_and_set_name(words)

            # Update the instance with information present from the statement
            words.remove(green_word)
            if instance.name in words:
                words.remove(instance.name)

            topic = self.determine_topic(words)
            instance.find_and_set(topic,words,self.nouns)

            # Compare the frames
            if instance.name in self.d[green_word]:
                stored = self.d[green_word][instance.name]
            else:
                stored = class_
            print(topic)
            print("stored",vars(stored))
            print("question",vars(instance))
            print("submission_type",stored.submission_type,instance.submission_type)
            
            # Both have the attribute
            if hasattr(stored,topic) and hasattr(instance,topic):
                print("has: yes")
                # They match
                if getattr(stored,topic) == getattr(instance,topic) and getattr(stored,topic) is not None:
                    print("answer: yes \n")
                    _answer = "yes"
                    return _answer
                # They don't match
                elif getattr(stored,topic) != getattr(instance,topic) and getattr(stored,topic) is not None and getattr(instance,topic) is not None:
                    print("answer: no \n")
                    _answer = "no"
                    return _answer
                elif getattr(stored,topic) == None:
                    print("answer: idk \n")
                    _answer = "idk"
                    return _answer
            else:
                print("answer: idk (attribute missing) \n")
                return "idk"

        print()
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
        bestTopic = ""
        for topic in self.topics:
            if topic.getOccurences() > maxScore:
                maxScore = topic.getOccurences()
                bestTopic = topic.getName()
            topic.resetOccurences()
        
        return bestTopic