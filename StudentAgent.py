"""
Project 3

ADD YOUR CODE HERE

Please read project directions before importing anything
"""


class StudentAgent:
    """ADD YOUR CODE HERE"""

    def __init__(self, verbose):
        self._verbose = verbose
        # TODO: Add your init code here

    def load_syllabus(self, list_of_list_of_statement_words):
        """Train agents from statements"""

        for _statement in list_of_list_of_statement_words:
            print(_statement)   # for debugging
            print(_statement.lower().split(' '))


    def input_output(self, word_list):
        """takes in list of words, returns question_object and data_requested"""

        print(word_list) # for debugging only

        # TODO: Add your code here

        _answer = "no" # NO - for debugging only, replace with your code
        _answer = "idk"  # I do not know
        _answer = "yes"  # YES

        return _answer
