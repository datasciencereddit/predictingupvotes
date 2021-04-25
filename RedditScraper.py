#pip install praw
#pip install schedule
import praw, schedule, time, sys, fileinput
from datetime import datetime

def scrape():
    tic = time.perf_counter()
    tempListWrite = []
    counterAdded = 0
    fileNameOne = "redditScraped.txt"

    #This reads the file in from which you have your info in.
    tempFile = open(fileNameOne, "r")
    for line in tempFile:
        tempListWrite.append(line)
    tempFile.close()

    #How many entries were read in
    print("Read in " + str(len(tempListWrite)) + " entries from the file.")

    #This is where you put in the secret information
    reddit = praw.Reddit(client_id = "", client_secret = "", password = "", user_agent = "", username = "",)

    #This will pick the subreddit 
    subredditChoice = reddit.subreddit("popular")

    #This is where you pick which catagory you want to browse and how many posts at a time you want to take in.
    #To change how many posts at a time, simply change the limit.
    #To change the category, simply change the .hot to like .top 
    subredditCategory = subredditChoice.hot(limit=10000)

    for post in subredditCategory:
        if post.stickied == False:
            tempTime = datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            tempTitle = post.title.replace(',', '')
            try:
                tempAuthorName = post.author.name
            except AttributeError:
                continue
            #adding a new line to the list
            try:
                tempString = "\n" + str(post.id) + "," + str(tempTitle) + "," + str(tempAuthorName) + "," + str(post.score) + "," + str(post.upvote_ratio) + "," + str(post.num_comments) + "," + str(post.subreddit.display_name) + "," + str(tempTime)
            except UnicodeEncodeError:
                continue
            tempListWrite.append(tempString)
            counterAdded = counterAdded + 1
    
    #Writes to list
    writeToFile(fileNameOne, tempListWrite)

    #This group of lines eliminates the empty lines from the text file.
    eliminateWhiteSpace(fileNameOne)
    
    #These numbers are not always accurate. Not sure why.
    print("Wrote " + str(counterAdded) + " entries to the file.")

    tempListWrite = []

    #Check for duplicates
    DuplicateChecker(fileNameOne)

    eliminateWhiteSpace(fileNameOne)

    toc = time.perf_counter()

    #Calculating how long the whole process took
    seconds = toc - tic
    seconds = "{:.2f}".format(seconds)

    print("This process took " + str(seconds) + " seconds")

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
            if L[i].partition(',')[0] < R[j].partition(',')[0]:
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

def DuplicateChecker(fileName):
    tempListWrite = []
    startingPoint = 0
    duplicateCounter = 0

    tempFile = open(fileName, "r")
    for line in tempFile:
        tempListWrite.append(line)
    tempFile.close()

    print("Read in " + str(len(tempListWrite)) + " entries from the file.")
    mergeSort(tempListWrite)
    print("Done Sorting")

    while True:
        noDuplicants = True
        for i in range(startingPoint, len(tempListWrite)-1):
            if tempListWrite[i].partition(',')[0] == tempListWrite[i+1].partition(',')[0]:
                tempListWrite.pop(i)
                noDuplicants = False
                duplicateCounter += 1
                startingPoint = i - 1
                break
        if noDuplicants == True:
            break

    print("Found " + str(duplicateCounter) + " duplicates.")

    f = open(fileName, "w")
    for i in range (len(tempListWrite)):
        try:
            f.write(tempListWrite[i])
        except UnicodeEncodeError:
            continue
    f.close()

def writeToFile(fileName, listName):
    f = open(fileName, "w")
    for i in range (len(listName)):
        try:
            f.write(listName[i])
        except UnicodeEncodeError:
            continue
    f.close()

def eliminateWhiteSpace(fileName):
    fh = open(fileName, "r")
    lines = fh.readlines()
    fh.close()
    lines = filter(lambda x: not x.isspace(), lines)
    fh = open(fileName, "w")
    fh.write("".join(lines))
    fh.close()


#This is the area where you can choose to either do every() minutes or seconds. Just input a number to change it if need be.
schedule.every(20).minutes.do(scrape)
#schedule.every(20).seconds.do(scrape)

#This script will run forever until you do ctrl+c in the console.
while True:
    schedule.run_pending()
    time.sleep(1)
