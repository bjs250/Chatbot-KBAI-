import utilities

class project:
	classname = "project"
	submission_type = None
	submission_location = None
	count = 0

	def __init__(self, name = None, start = None, end = None, grade = None):
		self.name = name
		self.start = start
		self.end = end
		self.grade = grade
		self.duration = None

	def getCount(self):
		return project.count

	def setCount(self,value):
		project.count = value

	def incrementCount(self):
		project.count += 1

	def getSubmission_type(self):
		return project.submission_type

	def setSubmission_type(self,value):
		project.submission_type = value

	def getSubmission_location(self):
		return project.submission_location

	def setSubmission_location(self,value):
		project.submission_location = value

	#####################################

	def calculateDuration(self):
		self.duration = str(int(self.end) - int(self.start))

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
				else:
					self.name = project.classname

	# Take whatever number is left in the statement
	def find_and_set(self,topic,statement,nouns):
		if topic == "start":
			for word in statement:
				if utilities.RepresentsInt(word):
					self.start = word
		elif topic == "end":
			for word in statement:
				if utilities.RepresentsInt(word):
					self.end = word
		elif topic == "duration":
			for word in statement:
				if utilities.RepresentsInt(word):
					self.duration = word

		elif topic == "submission_type":
			for word in statement:
				if word in nouns:
					project.submission_type = word
		elif topic == "submission_location":
			for word in statement:
				if word in nouns:
					project.submission_location = word
		elif topic == "grade":
			for word in statement:
				if '%' in word:
					self.grade = word