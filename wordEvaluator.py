import string, time

class wordValue:
    def __init__(self, word):
        self.word = word
        self.value = 0.0
        self.upvoteValue = []
        self.upvoteRatio = []
        self.averageUpvoteValue = 0.0
        self.averageUpvoteRatio = 0.0

def readFromFile(writeList):
    fileNameOne = "redditScraped.txt"
    tempFile = open(fileNameOne, "r")
    for line in tempFile:
        writeList.append(line)
    tempFile.close()

    print("Read in " + str(len(writeList)) + " entries from the file.")
    return writeList

def splitTitles(writeList, titleList):
    for entry in writeList:
        titleList.append(entry.partition(',')[2].partition(',')[0])
    return titleList

def splitUpvotes(writeList, upvoteList):
    for entry in writeList:
        upvoteList.append(entry.partition(',')[2].partition(',')[2].partition(',')[2].partition(',')[0])
    return upvoteList

def splitUpvoteRatios(writeList, upvoteRatioList):
    for entry in writeList:
        upvoteRatioList.append(entry.partition(',')[2].partition(',')[2].partition(',')[2].partition(',')[2].partition(',')[0])
    return upvoteRatioList


def evaluateWords(titleList, upvoteList, upvoteRatioList):
    wordValueList = []
    table = str.maketrans('', '', string.punctuation)
    tic = time.perf_counter()
    #for i in range(0, len(titleList)):
    for i in range(0, 100000):
        tempString = titleList[i]
        words = tempString.split()
        stripped = [w.translate(table) for w in words]
        normalizedStripped = [w.lower() for w in stripped]
        for w in normalizedStripped:
            flag = False
            for word in wordValueList:
                if word.word == w:
                    flag = True
                    word.upvoteValue.append(upvoteList[i])
                    word.upvoteRatio.append(upvoteRatioList[i])
                    break
            if flag == True:
                continue
            tempWord = wordValue(w)
            tempWord.upvoteValue.append(upvoteList[i])
            tempWord.upvoteRatio.append(upvoteRatioList[i])
            wordValueList.append(tempWord)
        if i % 1000 == 0:
            print("It has gone through " + str(i) + " titles!")
            mergeSort(wordValueList)

    print("Starting to evaluate averages!")

    for word in wordValueList:
        average = averageList(word.upvoteValue)
        word.averageUpvoteValue = average
        average = averageList(word.upvoteRatio)
        word.averageUpvoteRatio = average
        word.upvoteValue = []
        word.upvoteRatio = []
        word.value = word.averageUpvoteValue * word.averageUpvoteRatio

    print("Calculating Max Value!")

    maxValue = 0.0
    for word in wordValueList:
        if float(word.value) > maxValue:
            maxValue = float(word.value)

    print("Normalizing values!")
        
    for word in wordValueList:
        word.value = word.value / maxValue

    toc = time.perf_counter()
    #Calculating how long the whole process took
    seconds = toc - tic
    seconds = "{:.2f}".format(seconds)
    print("This process took " + str(seconds) + " seconds")

    return wordValueList

def averageList(tempList):
    total = 0
    entries = 0
    for i in tempList:
        total = total + float(i)
        entries = entries + 1
    average = total / entries
    return average

def mergeSort(arr):
    if len(arr) > 1:
 
         # Finding the mid of the array
        mid = len(arr)//2
 
        # Dividing the array elements
        L = arr[:mid]
 
        # into 2 halves
        R = arr[mid:]
 
        # Sorting the first half
        mergeSort(L)
 
        # Sorting the second half
        mergeSort(R)
 
        i = j = k = 0
 
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i].word < R[j].word:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def evaluateTitles(titleList, wordValueList, titleValue):
    print("Evaluating titles!")
    tic = time.perf_counter()
    table = str.maketrans('', '', string.punctuation)
    #for i in range(0, len(titleList)):
    for i in range(0, 100000):
        total = 0.0
        tempValue = 0.0
        totalWords = 0
        tempString = titleList[i]
        words = tempString.split()
        stripped = [w.translate(table) for w in words]
        normalizedStripped = [w.lower() for w in stripped]
        for w in normalizedStripped:
            for j in wordValueList:
                if w == j.word:
                    total = total + j.value
                    totalWords = totalWords + 1
        if totalWords != 0:
            tempValue = total / totalWords
        else:
            tempValue = 0.0
        tempValue = "{:.2f}".format(tempValue)
        titleValue.append(tempValue)
        if i % 1000 == 0:
            print("It has gone through " + str(i) + " titles!")
            mergeSort(wordValueList)
    
    toc = time.perf_counter()
    #Calculating how long the whole process took
    seconds = toc - tic
    seconds = "{:.2f}".format(seconds)
    print("This process took " + str(seconds) + " seconds")
    return titleValue
        
def writeToFile(titleValue):
    f = open("titlevalue.txt", "w")
    for i in range (len(titleValue)):
        try:
            f.write(titleValue[i] + "\n")
        except UnicodeEncodeError:
            continue
    f.close()

writeList = []
titleList = []
upvoteList = []
upvoteRatioList = []
wordValueList = []
titleValue = []

tic = time.perf_counter()
writeList = readFromFile(writeList)
titleList = splitTitles(writeList, titleList)
upvoteList = splitUpvotes(writeList, upvoteList)
upvoteRatioList = splitUpvoteRatios(writeList, upvoteRatioList)
wordValueList = evaluateWords(titleList, upvoteList, upvoteRatioList)
titleValue = evaluateTitles(titleList, wordValueList, titleValue)
writeToFile(titleValue)
toc = time.perf_counter()
#Calculating how long the whole process took
seconds = toc - tic
seconds = "{:.2f}".format(seconds)
print("The the complete program took " + str(seconds) + " seconds to run.")
