import utilities

class assignment:
	classname = "assignment"
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
		return assignment.count

	def setCount(self,value):
		assignment.count = value

	def incrementCount(self):
		assignment.count += 1

	def getSubmission_type(self):
		return assignment.submission_type

	def setSubmission_type(self,value):
		assignment.submission_type = value

	def getSubmission_location(self):
		return assignment.submission_location

	def setSubmission_location(self,value):
		assignment.submission_location = value

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
					assignment.submission_type = word
		elif topic == "submission_location":
			for word in statement:
				if word in nouns:
					assignment.submission_location = word
		elif topic == "grade":
			for word in statement:
				if '%' in word:
					self.grade = word