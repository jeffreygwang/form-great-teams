# The Team Selection Algorithm™

This is **Release 1.0**, a production version using naïve randomness. **Version 1.1**, using simulated annealing, is in development. 

> Used by: Harvard Consulting on Business and the Environment, Harvard Undergraduate Data Analytics Group, Harvard Computer Society, and other clubs.

## Introduction

Let's say that we are building teams, where $cn$ people will be split into $n$ teams, where $c, n \in \mathbb{Z}^+$). 

Each of the $cn$ people get to express some preference choice in the group of permutations on $[n]$. For instance, if there are 4 people per team, and 12 teams, then each of the 48 people express preferences, where each does so in some vector like $<12, 6, 3, 11, 1, 7, 2, 10, 9, 4, 5, 8>$. 

For instance, consider a set of rankings like this (identifying information omitted): 

<img width="300" class="center" alt="Screen Shot 2022-09-14 at 2 30 20 PM" src="https://user-images.githubusercontent.com/39931478/190234151-8a640d4f-cbd3-4a37-9419-c43dfa151221.png">

- As you can see above, some teams are very popular (like Team 7), whereas others are less so (like Team 1). How can we assign teams such that every person will be _relatively satisfied_ with their rankings?
- How can we make our algorithm robust, so that even if the number of teams and prospective people don't quite align, it still works?

## The Algorithm

Simply put, the algorithm here uses a stochastic greedy approach, which starts with the least favored teams upward: 

- The total ranking sum for each team is computed.
- Starting from the highest sum (least favored) downward, the top $c$ people who have pref'd that option, as well as anyone with the same ranking for this team as one of those $c$ people, are selected. 
- Out of that pool, $c$ people are randomly selected for that team and taken out of contention for other teams' selections. 
- This is repeated for every team. Once that is done, a complete set of team assignments has been given. 
- This repeated a set number of times (e.g. 100). 

I'm not sure if this problem is NP-complete, although it certainly seems like some variation of an NP-complete linear programming problem. As such, the Team Selection Algorithm™ uses some simplex-like stochastic heuristics to work. 

## Behavior Notes

This algorithm works better for data that is at least somewhat well-distributed (e.g. not everyone ranked T1 as their first choice). In my testing, out of 48 people and 12 teams, in taking the best choice out of a 100-time simulation, everyone received their fourth choice or higher. The distribution of preferences in final team assignments for the sample data of 48 people is given below:

<img width="361" alt="image" src="https://user-images.githubusercontent.com/39931478/190240382-dda68a1b-f24d-4633-8a2a-e9a66a31e758.png">

## Running On Sample Data

There are two sample files provided, one with teams of 4, and one with teams of 1. 

To run each, you will have to adjust some of the run parameters at the top of the file:
- NUM = # of people in the team
- MINVAL = # of teams
- NUM_TRIES = # of iterations to run algorithm
- FILENAME = csv file name
- NUM_COLS_METADAT = number of columns before rankings (5 in both)
- PREFIX = output file prefix

# Permissions

Originally made as the team selection algorithm for Harvard Consulting on the Business and the Environment. Used for F2022 recruiting cycle. Available on an MIT license. 

![image](https://user-images.githubusercontent.com/39931478/190246797-1119b8c2-2647-44c3-a42b-f24515ee540d.png)

