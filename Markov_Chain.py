#!/usr/bin/env python3
import random
import re
import sys
import os
import time

def runTest():
    test1()
    test2()
    test3()
    test4()

#LOOK HERE TO TEST
def test1():
    # reg ex tests
    print("Test 1 - regEx test's")
    print("--------------------------------")
    wordList = parseWordsIntoList(testfilePath + "regExTest.txt")
    print("Correct symbol/word count: ", end="")
    print(passFail(len(wordList) == 21))
    print()
    print("Correct pasing of words: ")
    print("Parses conjugates: ", passFail("don't" in wordList))
    print("Parses honorifics: ", passFail("mr.bond" in wordList))   # checking for titles
    print("Parses ellipse: ", passFail("..." in wordList))       # checking for elipse
    print("Parses possesive apostrophes: ", passFail("general’s" in wordList)) # using an actual apostrphe
    print("Parses ending punctuation: ", passFail("?" in wordList))         # checking for ending punctuation
    print()

#LOOK HERE TO TEST
def test2():
    # checks for correct markov matrix generation
    markovMatrix = createMarkovArray(testfilePath + "genMarkovTests.txt")
    print("Test 2 - Markov generation tests")
    print("--------------------------------")
    print("All starter words are correct:")
    starterDict = markovMatrix[starterWordsKey]
    print("Starter word count is correct: ", passFail(len(starterDict) == 5))
    print("Contains all starting words: ")
    print(passFail("what" in starterDict))
    print(passFail("i" in starterDict))
    print(passFail("well" in starterDict))
    print(passFail("think" in starterDict))
    print()
    testRow = starterDict = markovMatrix["think"]
    print("Total sum for \"think\" is correct: ", passFail(testRow[sumKey] == 3))
    print("Entries for \"think\" is correct: ")
    print(passFail("about" in testRow))
    print(passFail("they" in testRow))
    print()

#LOOK HERE TO TEST
def test3():

    # a smaller test checking for correct traversal of the markov matrix
    markovMatrix = createMarkovArray(testfilePath + "sentenceGenTests.txt")
    sentences = []
    # gen all the sentences possible
    # this should never take long due to the low possiblities of sentences
    while len(sentences) != 4:
        newSentence = getRandSentence(markovMatrix)
        if not newSentence in sentences:
            sentences.append(newSentence)

    print("Test 3 - Sentence generation tests")
    print("----------------------------------")
    print("Check that all sentences have been generated properly")
    print(passFail("one two three." in sentences))
    print(passFail("first, second third." in sentences))
    print(passFail("wow!" in sentences))
    print(passFail("really?" in sentences))
    print()

#LOOK HERE TO TEST
def test4():
    # test that you can combine files into the markov matrix
    markovMatrix = createMarkovArray(testfilePath + "combineTest1.txt")
    markovMatrix = AddFileToMarkovArray(testfilePath + "combineTest2.txt", markovMatrix)

    print("Test 4 - Add files tests")
    print("----------------------------------")
    print("Correct number of words found: ", passFail(len(markovMatrix) == 9))
    starWords = markovMatrix[starterWordsKey]
    print("Correct number of start words found: ", passFail(starWords[sumKey] == 3))
    testRow = markovMatrix["is"]
    print("Updated a row from both files correctly: ")
    print(passFail(testRow[sumKey] == 2))
    print(passFail("jim" in testRow))
    print(passFail("bob" in testRow))
    print()

def passFail(passed):
    if passed:
        return "PASS"
    else:
        return "FAIL"

def runTimeTest():
    timeFilePath = "testFiles/timeFiles/"
    for fileName in os.listdir(cwd + "/testFiles/timeFiles"):
        print("Timings for file: ", fileName)
        start = time.time()
        markovArray = createMarkovArray(timeFilePath+fileName)
        end = time.time()
        print("Creating the markov array: ", end-start)
        start = time.time()
        for i in range(0, 10000):
            getRandSentence(markovArray)
        end = time.time()
        print("Generating 10,000 random sentences: ", end-start)
        print()
    return

def getNextWord(word, markovMatrix):
    if word in markovMatrix:
        wordDict = markovMatrix[word]
        total = wordDict[sumKey]
        randNum = random.randint(1,total)
        for word in wordDict:
            if word != sumKey:
                randNum -= wordDict[word]
                if randNum <= 0:
                    return word
    else:
        print("sorry something went wrong")
        return "."

def createMarkovArray(fileName):
    wordList = []

    # init the dictionary
    markovMatrix = {}

    # parse all words into an array
    wordList = parseWordsIntoList(fileName)

    # add a sum to the starter words row
    markovMatrix[starterWordsKey] = {sumKey:0}
    # add the first word of the file to the start words row
    startWords = markovMatrix[starterWordsKey]
    startWords[wordList[0]] = 1
    startWords[sumKey] += 1

    # for each word in the word list
    for i  in range(0,len(wordList)):
        curWord = wordList[i]
        # if it not the last word get the next word
        if i + 1 < len(wordList):
            nextWord = wordList[i+1]
            # if the current word is an end punctuation
            if curWord in ".?;!":
                # add the next word to the start words dict
                startWords = markovMatrix[starterWordsKey]
                if nextWord in startWords:
                    startWords[nextWord] += 1
                else:
                    startWords[nextWord] = 1
                startWords[sumKey] += 1
            else:
                # check if we've seen this word before
                if curWord in markovMatrix:
                    wordDict = markovMatrix[curWord]
                else:
                    markovMatrix[curWord] = {sumKey:0}
                    wordDict = markovMatrix[curWord]

                # check if the next word is in this words dictionary
                if nextWord in wordDict:
                    wordDict[nextWord] += 1
                else:
                    wordDict[nextWord] = 1

                # incr the sum of words after the cur word
                wordDict[sumKey] += 1

    return markovMatrix

def AddFileToMarkovArray(fileName, markovMatrix):
    # parse all words into an array
    wordList = parseWordsIntoList(fileName)

    startWords = markovMatrix[starterWordsKey]

    # check if the starting word is in this startWords dictionary
    if wordList[0] in startWords:
        startWords[wordList[0]] += 1
    else:
        startWords[wordList[0]] = 1

    startWords[sumKey] += 1

    # for each word in the word list
    for i  in range(0,len(wordList)):
        curWord = wordList[i]
        # if it not the last word get the next word
        if i + 1 < len(wordList):
            nextWord = wordList[i+1]
            # if the current word is an end punctuation
            if curWord in ".?;!":
                # add the next word to the start words dict
                startWords = markovMatrix[starterWordsKey]
                if nextWord in startWords:
                    startWords[nextWord] += 1
                else:
                    startWords[nextWord] = 1
                startWords[sumKey] += 1
            else:
                # check if we've seen this word before
                if curWord in markovMatrix:
                    wordDict = markovMatrix[curWord]
                else:
                    markovMatrix[curWord] = {sumKey:0}
                    wordDict = markovMatrix[curWord]

                # check if the next word is in this words dictionary
                if nextWord in wordDict:
                    wordDict[nextWord] += 1
                else:
                    wordDict[nextWord] = 1

                # incr the sum of words after the cur word
                wordDict[sumKey] += 1

    return markovMatrix

def getRandSentence(markovMatrix):
    sentence = ""
    startWord = getNextWord(starterWordsKey, markovMatrix)
    sentence += startWord

    nextWord = startWord

    # checking for eclipses and end punctuation
    while not nextWord in "?;!....":
        nextWord = getNextWord(nextWord, markovMatrix)
        if nextWord not in "?;!,....":
            sentence += (" " + nextWord)
        else:
            sentence += nextWord

    return sentence

def genRandomSentences(markovMatrix):
    choice = input("press enter to generate a random sentence or enter q to quit: ")
    while 1 == 1:
        if choice == 'q':
            return
        elif choice != "":
            choice = input("press enter to generate a random sentence or enter q to quit: ")
        else:
            print()
            print(getRandSentence(markovMatrix))
            choice = input()

def parseWordsIntoList(fileName):
    regEx = "Mrs\.[\w']*|Dr.[\w']*|Ms.[\w']*|Mr.[\w']*|[\w]+’[\w]+|[\w']+|\.\.+|[.,!?;]"
    wordList = []

    with open(fileName, encoding="utf8") as file:
        for line in file:
            parsedWordList = re.findall(regEx,  line)
            # make all the words lower case
            parsedWordList = [word.lower() for word in parsedWordList]
            wordList += parsedWordList

    return wordList

def printMenu():
    print("-------------------------------")
    print("  Markov Chain Text Generator ")
    print("-------------------------------")
    print()
    print("1 - Generate random sentences from the input files")
    print("2 - Run Tests")
    print("3 - Run Time Tests")
    print("q - exit program")
    print()

def main(argv):
    global sumKey, starterWordsKey, testfilePath, cwd

    testfilePath = "testFiles/"
    inputPath = "inputFiles/"
    cwd = os.getcwd()
    inputDir = cwd + "/inputFiles"

    starterWordsKey = "_start_"
    sumKey = "_sum_"

    choice = ""
    while  1 == 1 :
        printMenu()
        choice = input("Select an option: ")
        if choice == '1':
            print("Creating markov chain...")
            print()
            firstFile = True;
            for fileName in os.listdir(inputDir):
                if firstFile:
                    markovMatrix = createMarkovArray(inputPath+fileName)
                    firstFile = False
                else:
                    markovMatrix = AddFileToMarkovArray(inputPath+fileName, markovMatrix)

            genRandomSentences(markovMatrix)
        if choice == '2':``
            runTest()
        if choice == '3':
            runTimeTest()
        if choice == 'q':
            return
        else:
            print("invalid input!")
            print()

if __name__ == "__main__":
    main(sys.argv)
