import utilities

class projects:
    classname = "projects"

    def __init__(self, submission_type = None, submission_location = None, count = 0):
        self.submission_type = submission_type
        self.submission_location = submission_location
        self.count = count
        self.references = {}

    def addReference(self,project):
        self.references[project.name] = project

    def getReferences(self):
        return self.references.keys()

    def getReference(self,name):
        for reference in self.references.keys():
            if reference == name:
                return self.references[reference]

    def getCount(self):
        return self.count

    def setCount(self,value):
        self.count = value