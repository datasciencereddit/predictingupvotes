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

tempListWrite = []
startingPoint = 0
duplicateCounter = 0

tempFile = open('redditScraped.txt', "r")
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

f = open('redditScraped.txt', "w")
for i in range (len(tempListWrite)):
    try:
        f.write(tempListWrite[i])
    except UnicodeEncodeError:
        continue
f.close()

if noDuplicants == True:
    print("No duplicants were found.")
