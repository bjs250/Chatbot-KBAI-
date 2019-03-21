import utilities

class project:
    classname = "project"

    def __init__(self, name = None, start = None, end = None):
        self.name = name
        self.start = start
        self.end = end
        self.duration = 0

    def getName(self):
        return self.name

    # Look adjacent to green word for a number --> make that the name
    def find_and_set_name(self,statement):
        for index,word in enumerate(statement):
            if word == self.classname:
                if index - 1 >= 0 and utilities.RepresentsInt(statement[index-1]):
                    self.name = statement[index-1]
                elif index + 1 < len(statement) and utilities.RepresentsInt(statement[index+1]):
                    self.name = statement[index+1]

    # Take whatever number is left in the statement
    def find_and_set_start(self,statement):
        for word in statement:
            if utilities.RepresentsInt(word):
                self.start = word
    
    def find_and_set_end(self,statement):
        for word in statement:
            if utilities.RepresentsInt(word):
                self.end = word
    