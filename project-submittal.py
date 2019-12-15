'''

Input files: first file: movies5000.txt and second file: student_nr_movie_data.csv

'''

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
import numpy as np
import datetime

#these libraries may need to be added before program will execute
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('wordnet')


class Movie:
    '''
    This class stores details about each movie extracted from the two input data files.
    Each movie instance will have a unique title and is represented only once
    as an instance of the Movie class.
    '''
    __lastId = 1                        # used to assign IDs to each new instance
    _instances = {}                     # used to store all instances and the instance attributes
    _directory = []                     # used to store all instances just as objects

    def __init__(self, title, date, summary):
        '''
        This function defines the various instance attributes and the source file
        for each.

        '''

        self.id = Movie.__lastId        # each Movie instance has a unique id
        Movie.__lastId += 1

        self.title = title              # available as title in both files
        self.date = date                # date in movies5000.txt and release_date in
                                        # student_movie_metadata.csv
                                        # if a movie is in both files, used date from
                                        # movies5000.txt
        self.summary = summary          # plot in movies5000.txt and
                                        # overview in student_nr_movie_data.csv
                                        # again movies5000.txt dominates for summary
        self.budget = None              # get from file student_nr_movie_data.csv
        self.vote_count = None          # get from file student_nr_movie_data.csv
        self.vote_average = None        # get from file student_nr_movie_data.csv
        self.popularity = None          # get from file student_nr_movie_data.csv
        self.nouns = []                 # extract from self.summary
                                        # note that this is a distinct set of nouns
                                        # extracted for the movie (i.e., no duplicates)
                                        # no non words
                                        # lower case
        self.adjectives = []            # extract from self.summary
                                        # note that this is a distinct set of adjectives
                                        # extracted for the movie (i.e., no duplicates)
                                        # no non words
                                        # lower case


        # append each instance created to dictionary
        Movie._directory.append(self)


    @classmethod
    def checkIfIn(cls, text):
        '''
        returns True if a movie with text as title is an instance of Movie class
        returns False otherwise
        '''
        if text in Movie._instances:
            return True
        else:
            return False


    def printDetails(self, title):
        '''
        Prints details about the movie with the given title as a sanity check. Output is appended to answers.txt file.
        '''
        with open('answers.txt', 'a') as file_out:
            file_out.write(r'As a sanity check, printing details for one movie: '+ str(title) +"\n\n")
            file_out.write(r'ID: ' + str(Movie._instances[title]['id'])+"\n")
            file_out.write(r'Budget: ' + str(Movie._instances[title]['budget'])+"\n")
            file_out.write(r'Vote Average: ' + str(Movie._instances[title]['vote_average'])+"\n")
            file_out.write(r'Summary: ' + str(Movie._instances[title]['summary'])+"\n")
            file_out.write(r'Popularity: ' + str(Movie._instances[title]['popularity'])+"\n")
            file_out.write(r'Vote Count: ' + str(Movie._instances[title]['vote_count'])+"\n")
            file_out.write(r'Nouns: ' + str(Movie._instances[title]['nouns'])+"\n")
            file_out.write(r'Adjectives: ' + str(Movie._instances[title]['adjectives'])+"\n\n")


def updateInstancesDirectory():
    '''
    After each file is read in and instances created, the Instance Directory is updated with the lastest information.
    '''
    for each in Movie._directory:
        Movie._instances[each.title] = {'classobj': each, 'id':each.id, 'date':each.date, 'summary':each.summary,'budget':each.budget, 'vote_count': each.vote_count, 'vote_average':each.vote_average, 'popularity':each.popularity,'nouns':each.nouns, 'adjectives':each.adjectives}

def removeDups(list):
    '''
    Function to remove duplicates from the input list
    and return the resulting new list
    '''
    setWords = set(list)
    uniqList = []
    for word in setWords:
        uniqList.append(word)

    return uniqList

def removeNonWords(list):
    '''
    Function to remove non words from the input list
    and return the resulting new list.
    We will discuss this in class
    '''
    words = []
    for word in list:
        if wn.synsets(word) != []:
            words.append(word)

    return words

def convertDate(date):
    '''
    Returns a date object from input string date. If the date starts with a question mark, the date is set to none. Else the date is converted to a datetime object.
    '''
    if date[0] == "?":
        date = None
    else:
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        except:
            date = datetime.datetime.strptime(date, '%Y')

    return date

def readFirstFile():
    '''
    Function to process movies5000.txt and create instances of movies
    '''
    with open('movies5000.txt', 'r') as file_in:
        lines = file_in.readlines()

    #remove header line
    lines = lines[1:]

    #parse each line by |
    for movie in lines:
        title = movie.split('|')[0]
        date = convertDate(movie.split('|')[1])
        summary = movie.split('|')[2]

        #create a Movie class instance for each movie
        obj = Movie(title, date, summary)

        nouns, adjectives = populateNounsAdjs(obj)

        obj.nouns = nouns
        obj.adjectives = adjectives

    # update the instances directory with all the instances created thus far from file one
    updateInstancesDirectory()

def readSecondFile():
    '''
    Function to process student_nr_movie_data.csv and create instances of movies.
    '''

    movieData = pd.read_csv("student_nr_movie_data.csv",na_filter= False)
    movieData = movieData.replace(r'^\s*$', np.nan, regex=True)

    # create variable that will be used to track duplicate titles in the two files
    global sameTitleInBoth
    sameTitleInBoth = 0


    # set variables for each movie and check if the Movie is already created as an instance
    for eachmovie in range(0,len(movieData)):

        title = movieData['title'][eachmovie]
        date = movieData['release_date'][eachmovie]
        summary = movieData['overview'][eachmovie]
        budget = movieData['budget'][eachmovie]
        vote_count = movieData['vote_count'][eachmovie]
        vote_average = movieData['vote_average'][eachmovie]
        popularity = movieData['popularity'][eachmovie]


        # If movie title hasn't been created as an instance, create an instance
        # else keep track of the same title in both files
        if Movie.checkIfIn(title) == False:
            obj = Movie(title, date, summary)

            # if the summary is empty, do not call noun and adjective list functions,
            # just set summary to None and nouns and adjectives to empty lists.
            if pd.isna(summary)==False:
                nouns, adjectives = populateNounsAdjs(obj)
            else:
                nouns = []
                adjectives = []
                obj.summary = None

            #set object attributes
            obj.budget = budget
            obj.vote_count = vote_count
            obj.vote_average = vote_average
            obj.popularity = popularity
            obj.nouns = nouns
            obj.adjectives = adjectives

        else:
            sameTitleInBoth += 1
            #titlesInBoth.append(title)
            obj = Movie._instances[title]['classobj']
            #set object attributes
            obj.budget = budget
            obj.vote_count = vote_count
            obj.vote_average = vote_average
            obj.popularity = popularity

    # update the instances directory with all the instances created thus far from file two
    updateInstancesDirectory()

def createMovieDF(moviedict):
    '''
    This function creates a dataframe of all movie instances. This is used for many of the reporting functions.
    '''

    # create blank DF with specified columns
    columns = ['title','id','date','summary','budget','vote_count','vote_average','popularity', 'nouns','adjectives']
    index = range(1,len(Movie._instances)+1)
    movieDF = pd.DataFrame(index=index,columns=columns)

    # populate DF
    i = 1
    for each in Movie._instances:
        movieDF.loc[i]['title'] = each
        movieDF.loc[i]['id'] = Movie._instances[each]['id']
        movieDF.loc[i]['date'] = Movie._instances[each]['date']
        movieDF.loc[i]['summary'] = Movie._instances[each]['summary']
        movieDF.loc[i]['budget'] = Movie._instances[each]['budget']
        movieDF.loc[i]['vote_count'] = Movie._instances[each]['vote_count']
        movieDF.loc[i]['vote_average'] = Movie._instances[each]['vote_average']
        movieDF.loc[i]['popularity'] = Movie._instances[each]['popularity']
        movieDF.loc[i]['nouns'] = Movie._instances[each]['nouns']
        movieDF.loc[i]['adjectives'] = Movie._instances[each]['adjectives']
        i += 1

    return movieDF

def getNthPopularMovieTitle(N):
    '''
    returns the title of the movie that is ranked N by popularity
    '''

    popularmovieDF = movieDF[['title', 'popularity']]
    Nthpopular = popularmovieDF.sort_values(by=['popularity'], ascending=False).reset_index(drop=True).loc[N-1]['title']

    return Nthpopular

def numbNoneVoteMovies():
    '''
    returns the number of movies with None as the number of votes
    '''
    noneCount = 0
    for movie in movieDF.vote_count:
        if movie == None:
            noneCount += 1
    return noneCount

def numbNoneSummaryMovies():
    '''
    returns the number of movies with None as the summary
    '''
    noneCount = 0
    for movie in movieDF.summary:
        if movie == None:
            noneCount += 1
    return noneCount

def populateNounsAdjs(Movie):
    '''
    Function that takes a Movie instance, and extracts a list of nouns and
    a list of adjectives from its summary attribute.
    Each list is cleaned to
        lower case letters,
        remove duplicates and
        remove non words.
    These cleaned lists are assigned to the Movie instance's nouns and adjectives
    attributes
    '''
    string = Movie.summary.lower()
    wordlist = nltk.pos_tag(word_tokenize(string))
    nounlist = []
    for word in wordlist:
        if word[1][0] == 'N':
            nounlist.append(word[0])

    uniqNounList = removeNonWords(nounlist)
    uniqNounList = removeDups(nounlist)

    adjlist = []
    for word in wordlist:
        if word[1][0] == 'J':
            adjlist.append(word[0])

    uniqAdjList = removeNonWords(adjlist)
    uniqAdjList = removeDups(adjlist)

    return uniqNounList, uniqAdjList

def createNounDF(cls):
    '''
    This function creates a dataframe of the nouns from all movies and tracks the number of movies each noun is used in the summary. The dataframe is used in some of the other reporting functions.
    '''

    nounList = {}

    for movie in Movie._instances:
        if Movie._instances[movie]['nouns'] != []:
            for each in Movie._instances[movie]['nouns']:
                if each in nounList:
                    nounList[each] += 1
                else:
                    nounList[each] = 1

    # dataframe columns named and sorted by noun count
    nounDF = pd.DataFrame(list(nounList.items()), columns=['noun', 'count'])
    nounDF = nounDF.sort_values(by=['count'], ascending=False).reset_index(drop=True)

    return nounDF

def findNMostFrequentNouns(cls, N):
    '''
    Function identifies the N most frequent nouns.
    Here frequency refers to the number of movies in which the
    noun occurs.
    '''

    return [nounDF.loc[N-1]['noun'], nounDF.loc[N-1]['count']]


def createAdjDF(cls):
    '''
    This function creates a dataframe of the adjectives from all movies and tracks the number of movies each adjective is used in the summary. The dataframe is used in some of the other reporting functions.
    '''

    adjList = {}

    for movie in Movie._instances:
        if Movie._instances[movie]['adjectives'] != []:
            for each in Movie._instances[movie]['adjectives']:
                if each in adjList:
                    adjList[each] += 1
                else:
                    adjList[each] = 1

    # dataframe columns named and sorted by noun count
    adjDF = pd.DataFrame(list(adjList.items()), columns=['adjective', 'count'])
    adjDF = adjDF.sort_values(by=['count'], ascending=False).reset_index(drop=True)

    return adjDF

def findNMostFrequentAdjectives(cls, N):
    '''
    Function identifies the N most frequent adjectives.
    Here frequency refers to the number of movies in which the
    adjectives occurs.
    '''

    return [adjDF.loc[N-1]['adjective'], adjDF.loc[N-1]['count']]


def getNounFrequency(noun):
    '''
    returns the frequency (number of movies for which the noun is extracted
    from the summary field) for the given noun
    '''
    try:
        freq = nounDF[nounDF.noun == noun]['count'].to_numpy().tolist()[0]
    except:
        freq = 0
    return str(freq)

def numberOfNounInstances():
    '''
    Returns the total number of noun instances in the full set of movies.

    '''

    return nounDF.sum()['count']

def numberOfAdjInstances():
    '''
    Returns the total number of adjective instances in the full set of movies.

    '''
    return adjDF.sum()['count']

def getMoviesInPopRange(low, high):
    '''
    Returns a list of nested lists where each nested list is a [title, popularity].
    these are titles of movies where popularity is >= low and < high.
    '''

    popularmovierankDF = movieDF[['title', 'popularity']].sort_values(by=['popularity'], ascending=False).reset_index(drop=True)

    popularmovierankDF = popularmovierankDF.loc[(popularmovierankDF.popularity >= low) & (popularmovierankDF.popularity < high)]

    return popularmovierankDF.values.tolist()

def longestMovieTitle(cls):
    '''
    This function returns the longest movie title based on length of string.
    '''

    longest = 0

    for movie in Movie._instances.keys():
        if len(movie) > longest:
            longest = len(movie)
            longestTitle = movie
    return longestTitle


def NMostPopularMovie(N):
    '''
    Returns the Nth most popular movie title.
    '''

    popularmovierankDF = movieDF[['title', 'popularity']].sort_values(by=['popularity'], ascending=False).reset_index(drop=True)

    popularmovieNranktitle = popularmovierankDF.loc[N-1].get(0)

    return popularmovieNranktitle


# This is the function that has the specific questions to get assignment
# answers

def printAnswers():
    '''
    This function prints answers to the following questions:

    1) the total number of movie instances created is:
    2) the number of movie instances that appear in both files (same title) is:
    3) the number of movie instances with None as summary is:
    4) the number of instances with None as vote_counts is:
    5) the total number of nouns - not unique - across all movie instances is:
    6) the total number of adjectives - not unique - across all movie instances:
    7) the 5 most frequent nouns are:
    8) the 5 most frequent adjectives are:
    9) the frequency of the nouns: girl, lobster, ox, plant are:
    10) the title of the eighth most popular movie is:
    11) the movie with the longest title is:
    12) Is 'Gone with the wind' the title of a movie instance?
    13) Is 'Call the midwife' the title of a movie instance
    14) Print a list of movie titles and their popularities that have popularity in the range >= 0.34 and < 0.35
    '''

    q1 = len(Movie._directory)
    q2 = sameTitleInBoth
    q3 = numbNoneSummaryMovies()
    q4 = numbNoneVoteMovies()
    q5 = numberOfNounInstances()
    q6 = numberOfAdjInstances()
    q7 = [findNMostFrequentNouns(Movie._instances, 1), findNMostFrequentNouns(Movie._instances,2), findNMostFrequentNouns(Movie._instances,3), findNMostFrequentNouns(Movie._instances,4), findNMostFrequentNouns(Movie._instances,5)]
    q8 = [findNMostFrequentAdjectives(Movie._instances, 1), findNMostFrequentAdjectives(Movie._instances,2), findNMostFrequentAdjectives(Movie._instances,3), findNMostFrequentAdjectives(Movie._instances,4), findNMostFrequentAdjectives(Movie._instances,5)]
    q9 = getNounFrequency('girl') + " " + getNounFrequency('lobster') + " " + getNounFrequency('ox') + " " + getNounFrequency('plant')
    q10 = NMostPopularMovie(8)
    q11 = longestMovieTitle(Movie._instances)
    q12 = 'Yes' if 'Gone with the Wind' in Movie._instances else 'No'
    q13 = 'Yes' if 'Call the Midwife' in Movie._instances else 'No'
    q14 = getMoviesInPopRange(0.34, 0.35)

    with open('answers.txt', 'w') as file_out:
        file_out.write(r'1) the total number of movie instances created is: ' + str(q1) +"\n")
        file_out.write(r'2) the number of movie instances that appear in both files (same title) is: ' + str(q2) +"\n")
        file_out.write(r'3) the number of movie instances with None as summary is: ' + str(q3) +"\n")
        file_out.write(r'4) the number of instances with None as vote_counts is: ' + str(q4) +"\n")
        file_out.write(r'5) the total number of nouns - not unique - across all movie instances is: ' + str(q5) +"\n")
        file_out.write(r'6) the total number of adjectives - not unique - across all movie instances: ' + str(q6) +"\n")
        file_out.write(r'7) the 5 most frequent nouns are: ' + str(q7) +"\n")
        file_out.write(r'8) the 5 most frequent adjectives are: ' + str(q8) +"\n")
        file_out.write(r'9) the frequency of the nouns: girl, lobster, ox, plant are: ' + str(q9) +"\n")
        file_out.write(r'10) the title of the eighth most popular movie is: ' + str(q10) +"\n")
        file_out.write(r'11) the movie with the longest title is: ' + str(q11) +"\n")
        file_out.write(r'12) Is "Gone with the Wind" the title of a movie instance? ' + str(q12) +"\n")
        file_out.write(r'13) Is "Call the Midwife" the title of a movie instance ' + str(q13) +"\n")
        file_out.write(r'14) Print a list of movie titles and their popularities that have popularity in the range >= 0.34 and < 0.35 ' + str(q14) +"\n\n\n")

    # Sanity check for one movie.
    Movie._instances['Aladdin']['classobj'].printDetails('Aladdin')


if __name__ == '__main__':
    '''
    Sequence of commands for processing movie files and printing answers
    '''

    # read in files
    readFirstFile()
    readSecondFile()

    #create dataframes used in the reporting functions
    movieDF = createMovieDF(Movie._instances)
    nounDF = createNounDF(Movie._instances)
    adjDF = createAdjDF(Movie._instances)

    # print answers to assignment questions
    printAnswers()
