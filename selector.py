import pandas as pd
import random
import time
import sys

# Customizable Parameters
NUM = 4                 # number of people per team
MINVAL = 13             # number of teams
NUM_TRIES = 200         # number of runs to pull best from
FILENAME = "s2022prefs_real.csv" # file name
NUM_COLS_METADATA = 5   # number of columns with just metadata
PREFIX = "f2022_analysts" # prefix

# Utility constants (don't change)
EMAIL = "email"     
MAX = 50000         

# Helper Methods

def getMaxAndIndex(arr: list[int]) -> list[int, int]:
    """Gets maximum element number that is not already processed (set to MAX), and index. 
    """
    maximum = -MAX
    for a in arr:
        if a != MAX and a > maximum:
            maximum = a
    index = arr.index(maximum)
    return [maximum, index]

def nonMaxed(arr: list[int]) -> int:
    """Gets # of non-processed (=MAX) elements.
    """
    numNotMax = 0
    for c in arr:
        if c != MAX:
            numNotMax += 1
    return numNotMax

# Pre-Processing

def init() -> list[list[str], pd.DataFrame, list[int]]:
    """Return initial data:
    - the case names
    - the full CSV pandas data frame
    - the sum of preferences for each team
    """
    # Filters
    prefs = pd.read_csv(FILENAME)

    # Get cases
    cases = prefs.columns[NUM_COLS_METADATA:]
    print(cases)

    # Switch by columns
    colsums = []
    for c in cases:
        colsums.append(sum(prefs[c]))

    print(colsums)

    # First make it alphabetical filtered
    prefs.sort_values('first_name')

    return [cases, prefs, colsums]

def getMinArrLen(arr: list[int]) -> list[int]:
    """Given sorted array of preferences, take the top NUM people who want this team. 
    If there are more people than NUM that have a preference in the top NUM, take all of them. 
    Randomly return NUM of them (or less if we've run out of people).
    """

    # Get all the people with numbers in the top NUM numbers
    i = NUM-1 
    while i < len(arr) and minArr[i] == minArr[NUM-1]:
        i += 1
    print(i)

    # Randomly select NUM people from the group
    if NUM == 1: # if there's just one person per group 
        return [random.randrange(i)]

    else:        # if there's > 1 person
        retarr = []
        notMax = nonMaxed(arr)

        if notMax >= NUM: # if there are more than NUM people left
            retarr.append(random.randrange(i))
            next = random.randrange(i)
            while len(retarr) < NUM:
                if next not in retarr:
                    retarr.append(next)
                else:
                    next = random.randrange(i)
            return retarr

        elif notMax < NUM and notMax > 0: # if there are less than NUM people left
            for j in range(notMax):
                retarr.append(j)
            return retarr
        else: # edge case
            return [random.randrange(len(arr))]

# The Algorithm Itself

currentRun:   int = 0                                # the run number
globalConfig: dict[int, dict[str, list[str]]] = {}   # global dictionary to save results across runs

while currentRun <= NUM_TRIES:

    # Initialize randomness and set up data 
    random.seed(random.randrange(100000))
    cases, prefs, colsums = init()
    maxedOut: int = MAX * len(colsums)                  # stop execution when list sum hits this
    totalRankingSum: int = 0                            # total ranking sum for each group
    currentConfig: dict[str, list[str]] = {}            # assignments for this run

    while sum(colsums) < maxedOut:
        minNum, index = getMaxAndIndex(colsums)
        casename: str = cases[index]

        minVal: int         = MINVAL
        minArr: list[int]   = []
        indices: list[int]  = [i for i in range(len(prefs[casename]))]

        for i in range(len(prefs[casename])):
            minArr.append(prefs[casename][i])
            if prefs[casename][i] < minVal:
                minVal = prefs[casename][i]
        
        minArr, indices = (list(t) for t in zip(*sorted(zip(minArr, indices))))

        # Get randomly chosen top indices
        chosenIndices: list[int] = getMinArrLen(minArr)
        currentConfig[casename] = []

        print(f"\n{casename}\n")
        print(minArr)
        print(indices)

        # Print information and clear the rows
        for chosen in chosenIndices:
            print(f" - Chosen: {prefs[EMAIL][indices[chosen]]}")
            print(f" - Value: {prefs[casename][indices[chosen]]}")
            totalRankingSum += prefs[casename][indices[chosen]]

            # Clearing
            for c in cases:
                prefs[c][indices[chosen]] = MAX
            
            currentConfig[casename].append(prefs[EMAIL][indices[chosen]])
        
        # Wipe out processed entry
        colsums[index] = MAX
    
    # For each run, print total ranking sum (less is better)
    print(f" - TOTAL RANKING SUM: {totalRankingSum}")
    globalConfig[totalRankingSum] = currentConfig
    currentRun += 1

print(globalConfig)
print(f"\nBest Ranking : [{min(globalConfig.keys())}]\n")
print(globalConfig[min(globalConfig.keys())])

# Re-Assemble Original CSV

reassembled = prefs[prefs.columns[:5]]
reassembled = reassembled.reindex(columns = prefs.columns)   
names = list(reassembled['email'])

for c in globalConfig[min(globalConfig.keys())]:
    for email in globalConfig[min(globalConfig.keys())][c]:
        reassembled[c][names.index(email)] = 1

reassembled.to_csv(f"{PREFIX}_prefs.csv")


