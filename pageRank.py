'''
Web Graph Page Ranking This aims at implementing the PageRank Algorithm from stratch. The algorithm is implemented with and without teleportations using numerical linear algebra package and Power Iteration Method We are taking the teleportation value as 0.1.

The program allows user to enter the query in form of a graph. The user is expected to enter the number of nodes and if the user wants a edge between 1 and 2 then he should enter "1 2" when prompted for the edges.

Functions and their uses:
 
The webpage ranks are calculated through the following methods:
1. Numerical Linear Algebra Package: 
    This method uses the linear algebra package in python to calculate the left eigen values and vectors
2. Power Iteration Method: 
    This method uses power iteration with a precision of 1e-8, and a max iteration limit of 500 to calculate the values.
'''

import numpy as np
import networkx as nx

# number of nodes in the graph 
n=0

# number of edges
e=0
 
n = int(input("Enter number of vertices/nodes in graph: "))
e = int(input("Enter number of edges in graph: "))

# adjecency matrix for the input graph
adjacencyMatrix = [[0 for i in range(n)] for j in range(n)]
 
for i in range(e):
    v1, v2 = map(int, input("Enter pair of vertices: ").split())
    adjacencyMatrix[v1-1][v2-1] = 1
 
G  = nx.from_numpy_array(np.array(adjacencyMatrix),create_using=nx.DiGraph)
 
def vectorDifferenceError(matrix1, matrix2):
    '''Calculates the vector difference error of two matrices given as input'''    
    difference = 0
    for i in range(n):
        difference += abs(matrix1[i] - matrix2[i])
    return difference
 
def PageRank(alpha):
    '''
    Main funciton which calculates the pageRank of the input graph given by the user.
    Input is alpha which is the teleportation value.
    In this program we have taken a default value of 0.1/
    It calculates the rank by two methods - linear algebra method and power method
    Outputs the corresponding ranks calculated in descending order.
    '''
    
    vectorProduct = np.zeros(n)
    vectorProduct[3] = 1
    transitionProbabilityMatrix = []
 
    for i in adjacencyMatrix:
        if 1 not in i:
            transitionProbabilityMatrix.append([x/n for x in range(n)])
        else:
            transitionProbabilityMatrix.append(list(i))
 
    for i in range(n):
        onesCount = transitionProbabilityMatrix[i].count(1)
        for j in range(n):
            if transitionProbabilityMatrix[i][j] == 1:
                transitionProbabilityMatrix[i][j] = 1/onesCount
 
    for i in range(n):
        for j in range(n):
            transitionProbabilityMatrix[i][j] *= (1-alpha)
            transitionProbabilityMatrix[i][j] += (alpha/n)
 
    matrixP = np.array(transitionProbabilityMatrix)

    # iteration limit
    iterationlimit = 500
    while iterationlimit:
        initDistribution = vectorProduct
        vectorProduct = vectorProduct @ matrixP
        if vectorDifferenceError(vectorProduct, initDistribution) < 10**(-8):
            break
        iterationlimit -=1
 
    w,v = np.linalg.eig(matrixP.T)
    x = v[:,0].real
 
    PageRankArrPower = vectorProduct
    PageRankArrLinAlg = x/sum(x)
 
    PageRankPower = []
    PageRankLinAlg =[]
    for i in range(n):
        PageRankPower.append((i, PageRankArrPower[i]))
        PageRankLinAlg.append((i, PageRankArrLinAlg[i]))
 
    # sorting the values in the descending order
    PageRankPower.sort(reverse=True, key=lambda x:x[1])
    PageRankLinAlg.sort(reverse=True, key=lambda x:x[1])
 
    return PageRankPower, PageRankLinAlg
 
PageRankPower, PageRankLinAlg  = PageRank(0.1)
 
# printing values of page rank calculated
print("The ranking of the Pages in descending order, with Random Teleportaion is: ")
print("\t By Power Iteration: ")
for i in range(n):
    print('\t\t', PageRankPower[i][0]+1, "(Weight: ", PageRankPower[i][1], ")")
 
print("\t By Linear Algebra: ")
for i in range(n):
    print('\t\t', PageRankLinAlg[i][0]+1, "(Weight: ", PageRankLinAlg[i][1], ")")
 
 
# alpha is defined as 0 since we don't want any teleportations
pr=nx.pagerank(G,alpha=0,tol=1e-08)
 
adjacencyMatrix = np.array(adjacencyMatrix)
TPMatrix = adjacencyMatrix/adjacencyMatrix.sum(axis=1)
 
def PagerankNoTeleport():
    '''
    Function to calculate the pageRank without teleporation
    Ouputs the pageRank with linear algebra method and power method.
    '''
    rank = 100*np.ones(n)/n
    count = 0
    prevRank = rank
    
    rank = np.dot(TPMatrix, rank)
    while(np.linalg.norm(prevRank-rank) > 0.01 and count<250):
        prevRank = rank
        rank = np.dot(TPMatrix, rank)
        count +=1
 
    w, v = np.linalg.eig(TPMatrix)
    EVOrdering = np.absolute(w).argsort()[::-1]
    eigenVal = w[EVOrdering]
    eigenVec = v[:, EVOrdering]
    linAlgRank = eigenVec[:,0]
 
    PageRankPowerNoTP = []
    PageRankLinAlgNoTP =[]
 
    PageRankArrPower = rank/sum(rank)
    PageRankArrLinAlg = np.abs(np.real(linAlgRank))/2
 
    for i in range(n):
        PageRankPowerNoTP.append((i, PageRankArrPower[i]))
        PageRankLinAlgNoTP.append((i, PageRankArrLinAlg[i]))
 
    PageRankPowerNoTP.sort(reverse=True, key=lambda x:x[1])
    PageRankLinAlgNoTP.sort(reverse=True, key=lambda x:x[1])
 
    return PageRankPowerNoTP, PageRankLinAlgNoTP
 

# calculates the PageRank without teleportation and prints the corresponding values 
PageRankPowerNoTP, PageRankLinAlgNoTP = PagerankNoTeleport()
 
print("The ranking of the Pages in descending order, without Random Teleportaion is: ")
print("\t By Power Iteration: ")
for i in range(n):
    print('\t\t', PageRankPowerNoTP[i][0]+1, "(Weight: ", PageRankPowerNoTP[i][1],")")
 
print("\t By Linear Algebra: ")
for i in range(n):
    print('\t\t', PageRankLinAlgNoTP[i][0]+1, "(Weight: ", PageRankLinAlgNoTP[i][1],")")
 
 
