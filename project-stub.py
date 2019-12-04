'''
Final Project Stub

Input files: first file: movies5000.txt and second file: student_nr_movie_data.csv

You cannot change the arguments given to each function specified below.

'''

def Movie:
    '''
    This class stores details about each movie extracted from the two input data files.
    Each movie instance will have a unique title and is represented only once
    as an instance of the Movie class. 
    '''
    
    def __init__(self, title, date, summary):
        '''
        This function defines the various instance attributes and the source file
        for each.

        You may add any other attributes that might help in achieving project goals.
        
        '''
        self.id                         # each Movie instance has a unique id
        self.title = title              # available as title in both files
        self.date = date                # date in movies5000.txt and release_date in
                                        # student_movie_metadata.csv
                                        # if a movie is in both files, used date from
                                        # movies5000.txt
        self.summary = summary          # plot in movies5000.txt and
                                        # overview in student_nr_movie_data.csv
        self.budget = None              # get from file student_nr_movie_data.csv
        self.vote_count = None          # get from file student_nr_movie_data.csv
        self.vote_average = None        # get from file student_nr_movie_data.csv
        self.popularity = None          # get from file student_nr_movie_data.csv
        self.nouns = []                 # extract from self.summary
                                        # note that this is a distinct set of nouns
                                        # extracted for the movie (i.e., no duplicates)
        self.adjectives = []            # extract from self.summary
                                        # note that this is a distinct set of adjectives
                                        # extracted for the movie (i.e., no duplicates)

  
    def checkIfIn(cls, text):
        '''
        returns True if a movie with text as title is an instance of Movie class
        returns False otherwise
        '''




# functions outside the class definition

# a helper function that might be useful
def removeDups(list):
    '''
    Function to remove duplicates from the input list
    and return the resulting new list
    '''

# a helper function that might be useful
def removeNonWords(list):
    '''
    Function to remove non words from the input list
    and return the resulting new list.
    We will discuss this in class
    '''
    
def readFirstFile():
    '''
    Function to process movies5000.txt and create instances of movies
    '''
    

def readSecondFile():
    '''
    Function to process student_nr_movie_data.csv and create instances of movies
    Note you are *required* to use Pandas to load and extract the pieces of
    information you need from this file.
    '''

# the remaining functions provide answers to most of the questions
def getNthPopularMovieTitle(N):
    '''
    returns the title of the movie that is ranked N by popularity
    '''

def numbNoneVoteMovies():
    '''
    returns the number of movies with None as the number of votes
    '''

def numbNoneSummaryMovies():
    '''
    returns the number of movies with None as the summary
    '''

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
    
def findNMostFrequentNouns(cls, n):
    '''
    Function identifies the n most frequent nouns.
    Here frequency refers to the number of movies in which the
    noun occurs.
    '''
        
def findNMostFrequentAdjectives(cls, n):
    '''
    Function identifies the n most frequent adjectives.
    Here frequency refers to the number of movies in which the
    adjectives occurs.
    '''

def getNounFrequency(noun):
    '''
    returns the frequency (number of movies for which the noun is extracted
    from the summary field) for the given noun
    '''
        

def numberOfNounInstances():
    '''
    Returns the total number of noun instances in the full set of movies.
        
    (To explain, the number of instances for the noun 'boy' is
    the number of movies in which 'boy' is a noun extracted from the summary
    field. So the function returns the sum of instances for all nouns.)
    '''
    
def numberOfAdjInstances():
    '''
    Returns the total number of adjective instances in the full set of movies.
        
    (To explain, the number of instances for the adjective 'good' is
    the number of movies in which 'good' is an adjective extracted from the summary
    field.  So the function returns the sum of instances for all adjectives.)
    '''

def getMoviesInPopRange(low, high):
    '''
    Returns a list of nested lists where each nested list is a [title, popularity].
    these are titles of movies where popularity is >= low and < high.
    '''
  
# This is the function that has the specific questions you need to get
# answers for programatically

def printAnswers():
    '''
    Add code to answer the following questions and print the answers.
    Use the functions that I have outlined above and any others you may need.

    Note: the answers should be printed to a file called Answers.
    
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

    

if __name__ == '__main__':
    '''
    This will hold a sequence of commands to complete the requirements of the
    project from the initial reading of files and creating instances to
    printing the answers.
    '''
    
    # you are to read the files in the following sequence
    readFirstFile()
    readSecondFile()
    
    # add your sequence of functions here if and as necessary

    printAnswers()  # this will be the last function to call and will
                    # store results in the file Answers which you should submit
                    # along with your code
