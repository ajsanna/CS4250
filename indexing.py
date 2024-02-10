
#-------------------------------------------------------------------------
# AUTHOR: Alexander J Sanna
# My implementation of indexing.py
# SPECIFICATION: This is my implementation of the indexing program.
# FOR: CS 4250- Assignment #1
# TIME SPENT: Roughly 1 hour

#-----------------------------------------------------------
#
#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH
#AS numpy OR pandas. You have to work here only with standard arrays
#Importing some Python libraries
import csv
import math

documents = []

#Reading the data in a csv file

with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0:  # skipping the header
            documents.append(row[0])


#Conducting stopword removal. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {"I", "and", "her", "she", "they", "their", }
#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
stemming = {"loves": "love", "cats": "cat", "dogs": "dog"}
#Identifying the index terms.
#--> add your Python code here
terms = {"love": 0, "cat": 0, "dog": 0}
docFreq = {"love": 0, "cat": 0, "dog": 0}
termFreq = {"love": 0, "cat": 0, "dog": 0}
termFreqPerDoc = []
for x in documents:
    #print(x)
    words = x.split()
    if 'love' in words:
        docFreq['love'] = docFreq['love'] + 1
    if 'loves' in words:
        docFreq['love'] = docFreq['love'] + 1
    if 'cats' in words:
        docFreq['cat'] = docFreq['cat'] + 1
    if 'dogs' in words:
        docFreq['dog'] = docFreq['dog'] + 1
    if 'cat' in words:
        docFreq['cat'] = docFreq['cat'] + 1
    if 'dog' in words:
        docFreq['dog'] = docFreq['dog'] + 1

    for word in words:
        #print(word)
        if word in terms:
            termFreq[word] = termFreq[word] + 1
            terms[word] = terms[word] + 1
        elif word in stemming:
            terms[stemming[word]] = terms[stemming[word]] + 1
            termFreq[stemming[word]] = termFreq[stemming[word]] + 1
    termFreqPerDoc.append(termFreq)
    termFreq = {"love": 0, "cat": 0, "dog": 0}


#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here
docTermMatrix = []
idf = []
idf.append(math.log10( 3/docFreq['love']))
idf.append(math.log10(3/docFreq['dog']))
idf.append(math.log10(3/docFreq['cat']))



#Printing the document-term matrix.
#--> add your Python code here
print("Total occurances: ", terms)
print("tf-idf values:")
print("Document     Love    Cat     Dog")
print("1    " + str(termFreqPerDoc[0]['love'] * idf[0]) + "  " + str(termFreqPerDoc[0]['cat'] * idf[2]) +"  " +  str(termFreqPerDoc[0]['dog'] * idf[1]))
print("2    " + str(termFreqPerDoc[1]['love'] * idf[0]) + "  " + str(termFreqPerDoc[1]['cat'] * idf[2]) +"  " +  str(termFreqPerDoc[1]['dog'] * idf[1]))
print("3    " + str(termFreqPerDoc[2]['love'] * idf[0]) + "  " + str(termFreqPerDoc[2]['cat'] * idf[2]) +"  " +  str(termFreqPerDoc[2]['dog'] * idf[1]))

