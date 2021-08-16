'''
Homework 6: Transforming Playlists
Carter King
Dr. Sanders
CS 355 Advanced Algorithms
12 November 2018
Python 3
'''

import sys


'''
Function: playlist_transformation(s, t, tupleIndex)
 This function fills in a 2-D array with optimal moves to transform one music playlist, s, into another music playlist,
 t, at the minimal cost
 parameters: s - an array of triple tuples that will be transformed into t
             t - an array of triple tuples that will have s transform into it
             tupleIndex - this refers to the category that i being transformed on, the tupleIndex integer is either
                          0,1,2 in reference to the tuple location of the desired category
 returns: A[len(s)][len(t)] - this is the bottom right value in the 2-D array and is the same value as the minimum 
                              number of edits
          A - the 2-D array with filled in values for the minimal amount of edits
'''


def playlist_transformation(s, t, tupleIndex):
    A = [[0 for x in range(len(t) + 1)] for m in range(len(s) + 1)] #initiate 2-D array
    for a in range(len(s) + 1):  #initiate 0th row and 0th column with corresponding index
        A[a][0] = a
    for b in range(len(t) + 1):
        A[0][b] = b
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1): #iterate through each value in 2-D array from A[1][1] to A[len(s)][len(t)]
            if tupleIndex == 0: #song
                if s[i - 1] == t[j - 1]: #if songs the same, value is its diagonal
                    A[i][j] = A[i - 1][j - 1]
                else:
                    minD = A[i - 1][j] + 1
                    minI = A[i][j - 1] + 1
                    minS = A[i - 1][j - 1] + 1 #changed from 2 to 1 to match blues.txt
                    A[i][j] = min(minD, minI, minS) #take min. of deleting, inserting, or changing
            elif s[i - 1][tupleIndex] == t[j - 1][tupleIndex]: #artist or genre
                A[i][j] = A[i - 1][j - 1]
            else:
                minD = A[i - 1][j] + 1
                minI = A[i][j - 1] + 1
                minS = A[i - 1][j - 1] + 1 #changed from 2 to 1 to match blues.txt
                A[i][j] = min(minD, minI, minS)
    return A[len(s)][len(t)], A


'''
Function: retrace_steps(A, s, t, i, j)
 This recursive function traces back through the 2-D array starting in the bottom right corner and prints out the proper
 moves to transform playlist s into playlist t
 parameters: A - the filled in 2-D array of optimal values
             s - an array of triple tuples that will be transformed into t
             t - an array of triple tuples that will have s transform into it
             i - the current row index, starts off as len(s), updated through recursion
             j - the current column index, starts off as len(t), updated through recursion
 returns: nothing just prints
'''


def retrace_steps(A, s, t, i, j):
    currValue = A[i][j] #start at bottom-right corner
    if i == 0 and j == 0: #Break the recursion
        return
    else:
        up = A[i - 1][j]
        left = A[i][j - 1]
        diagonal = A[i - 1][j - 1]
        direction = min(diagonal, up, left) #decide minimal direction to travel
        if direction == diagonal:
            if direction == currValue: #Keep the same
                i -= 1
                j -= 1
                retrace_steps(A, s, t, i, j) #recurse on next position in A
                print("Leave", s[i], "unchanged")
            else: #replace
                i -= 1
                j -= 1
                retrace_steps(A, s, t, i, j)
                print("Replace", s[i], "with", t[j])
        elif direction == up: #Delete
            i -= 1
            retrace_steps(A, s, t, i, j)
            print("Delete", s[i])
        else: #Insert
            j -= 1
            retrace_steps(A, s, t, i, j)
            print("Insert", t[j])


'''
Function: parseFile(filename)
 This function takes a .txt file of (song, artist, genre) tuples and appends them to a list  
 parameters: filename - a string of the name of the file 
 returns: list - a list of triple tuples representing a playlist
'''


def parseFile(filename):
    list = []
    infile = open(filename, 'r')  # read the file and add elements to list
    for line in infile:
        line.strip()
        splitLine = line.split(',')
        songTuple = (splitLine[0], splitLine[1], splitLine[2].rstrip()) #triple tuple of (song, artist, genre)
        list.append(songTuple)
    return list


def main():
    # Show them the default len is 1 unless they put values on the command line
    print(len(sys.argv))
    if len(sys.argv) == 4:
        sFileName = sys.argv[1]
        tFileName = sys.argv[2]
        userChoice = sys.argv[3]
    else:
        sFileName = input("Which playlist file would you like to change? ")
        tFileName = input("Which playlist file would you like file 1 to be changed to? ")
        userChoice = str(input("What category would you like to transform off of: Song(s), Artist(a), or Genre(g)? ")) #letter
        s = parseFile(sFileName)
        t = parseFile(tFileName)
        if userChoice == "s":
            category = "song"
            tupleIndex = 0
        elif userChoice == "a":
            category = "artist"
            tupleIndex = 1
        else:
            category = "genre"
            tupleIndex = 2
        minEdits, twoDArray = playlist_transformation(s, t, tupleIndex)
        print("Comparing playlist similarity by",category)
        print("The minimum edit distance was", minEdits)
        retrace_steps(twoDArray, s, t, len(s), len(t)) #prints out moves to edit


main()
