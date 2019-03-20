"""
Project 3

ADD YOUR CODE HERE

Please read project directions before importing anything
"""


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
            

    def load_syllabus(self, list_of_list_of_statement_words):
        """Train agents from statements"""

        for _statement in list_of_list_of_statement_words:
            print(_statement)   # for debugging
            print(_statement.lower().split(' '))

    def input_output(self, word_list):
        """takes in list of words, returns question_object and data_requested"""

        green_word = ""
        print(word_list) # for debugging only
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
