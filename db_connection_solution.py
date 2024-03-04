#-------------------------------------------------------------------------
# AUTHOR: Alexander J Sanna
# FILENAME: INDEX.PY
# SPECIFICATION: This is my version of DB_Connection.py
# FOR: CS 4250- Assignment #2
# TIME SPENT: 9+ hours. This was pain.
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import psycopg2
from psycopg2.extras import RealDictCursor


def connectDataBase():

    DB_NAME = "CPP"
    DB_USER = "postgres"
    DB_PASS = "123"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                cursor_factory=RealDictCursor)
        return conn

    except:
        print("Database not connected successfully")


def createCategory(cur, id, catName):

    sql = "Insert into Category (id, catName) Values (%s, %s) "

    recset = [id, catName]
    cur.execute(sql, recset)

#GOOD
def createDocument(cur, docId, docText, docTitle, docDate, docCat, docTerms=None):

    # 1 Get the category id based on the informed category name
    # --> add your Python code here

    cur.execute("select catName from Category where catID = %(docCat)s")
    catID = cur.fetchall()

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    char_count = 0
    prohibited = [" ", ",", ".", "!", "?"]
    for element in docText:
        if element not in prohibited:
            char_count = char_count + 1

    sql = "Insert into Document (docId, docText, docTitle, docDate, catID, char_count) Values (%s, %s, %s, %s, %s, %s)"

    recset = [docId, docText, docTitle, docDate, catID, char_count]
    cur.execute(sql, recset)

    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here

    words = docText.split(" ")
    for word in words:

        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for x in word:
            if x in punc:
                word = word.replace(x, "")
        word = word.lower

        sql = "Insert into Terms (term, termCount) Values (%s, %s)"
        recset = [word, 1]
        cur.execute(sql, recset)

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python code here

    sql = "select term from index where doc = %(docId)s"
    cur.execute(sql, {'docId': docId})
    currentIndex = cur.fetchall()

    for new_term in docTerms:
        term_count = 0

        for term in docTerms:

            if new_term == term:
                term_count = term_count + 1

        found = False
        for saved_term in currentIndex:
            if new_term == saved_term:
                found = True
        if not found:
            currentIndex.append(new_term)

            sql = "Insert into index (doc, term, term_count) Values (%s, %s, %s)"
            recset = [docId, new_term, term_count]
            cur.execute(sql, recset)


def deleteDocument(cur, docId):

    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here

    sql = "select term from Index where docId = %(docId)s"
    cur.execute(sql, {'docId': docId})
    currentIndex = cur.fetchall()

    for i in currentIndex:
        sql = "Delete from Index where docId = %(docId)s and term = %(term)s"
        cur.execute(sql, {'docId': docId, 'term': i})

    sql = "select term from Index"
    cur.execute(sql)
    others = cur.fetchall()

    for i in currentIndex:
        found = False
        for otherIndex in others:
            if i == otherIndex:
                found = True

        if not found:

            sql = "Delete from terms where term = %(term)s"
            cur.execute(sql, {'term': i})


    # 2 Delete the document from the database
    # --> add your Python code here
    sql = "Delete from Document where docId = %(docId)s"
    cur.execute(sql, {'docId': docId})

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here
    sql = "Delete from document where docId = %(docID)s"
    cur.execute(sql, {'id': id})

    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(cur, docId, docText, docTitle, docDate, docCat)

def getIndex(cur):
    sql = "select term from terms order by term"
    cur.execute(sql)
    all_terms = cur.fetchall()
    return all_terms

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here