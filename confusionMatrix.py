import pandas as pd
import numpy as np

df = pd.read_csv("results.log")
#print(df)

confusion_matrix = np.zeros((3,3))
d = {}
d['yes'] = 0
d['no'] = 1
d['idk'] = 2

for index, row in df.iterrows():
    #print(index,row['answer'],row['studentAnswer'])
    if index <= 30:
        currentAnswer = row['answer']
        currentStudentAnswer = row['studentAnswer']
        confusion_matrix[d[currentAnswer]][d[currentStudentAnswer]] += 1    

print(confusion_matrix)