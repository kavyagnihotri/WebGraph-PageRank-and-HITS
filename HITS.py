'''
HITS Algorithm: This program aims to implement the HITS algorithm in python, with a single-word query. The Algorithm is implemented on a
NetworkX WebGraph. The user inputs a query, and the Hub and Authority scores are calculated using power iteration method.
'''

import networkx as nx
import numpy as np


query = input("Enter a query word: ")
query = query.lower()
rootSet = []
 
web_graph = nx.read_gpickle("web_graph.gpickle")
'''This is the NetworkX WebGraph'''

n = len(web_graph.nodes)
 
for node in web_graph.nodes:
    nodeContent = web_graph.nodes[node]['page_content'].lower()
    if query in nodeContent:
        rootSet.append(node)
 
baseSet = list(rootSet)
 
rootSetEdges = []
baseSetEdges = []
 
for edge in web_graph.edges:
    if edge[0] in rootSet:
        rootSetEdges.append(edge)
        baseSet.append(edge[1])
    elif edge[1] in rootSet:
        baseSetEdges.append(edge)
        baseSet.append(edge[0])

baseSet = list(set(baseSet))
'''This is the BaseSet for the given query''' 

rootSet = list(set(rootSet))
'''This is the RootSet for the given query''' 
 
baseSetAdjMatrix = np.zeros(n)
for i in baseSet:
    baseSetAdjMatrix[i] = 1

subgraph = nx.subgraph(web_graph, sorted(baseSet))
'''This is the subGraph for the given webgraph, which is created from the baseSet''' 
 
mapping = {}
reversemapping = {}
val = 0
for i in baseSet:
    mapping[i] = val
    reversemapping[val] = i
    val+=1
n = len(baseSet)

adjacencyMatrix = [[0 for i in range(n)] for j in range(n)]
'''This is the Adjacency Matrix of the NetworkX WebGraph'''
 
for edge in baseSetEdges:
    edgeFrom, edgeTo = edge
    edgeFrom = mapping[edgeFrom]
    edgeTo = mapping[edgeTo]
    adjacencyMatrix[edgeFrom][edgeTo] = 1
 
for edge in rootSetEdges:
    edgeFrom, edgeTo = edge
    edgeFrom = mapping[edgeFrom]
    edgeTo = mapping[edgeTo]
    adjacencyMatrix[edgeFrom][edgeTo] = 1
 
adjacencyMatrix = nx.to_numpy_array(subgraph)
n = len(adjacencyMatrix)

hubValues = np.ones(n)/n
'''This is the array which stores Hub Scores'''

authValues = np.ones(n)/n
'''This is the array which stores Authority Scores''' 

for i in range(2005):
    hubValues = np.dot(adjacencyMatrix, authValues)
    authValues = np.dot(adjacencyMatrix.T, hubValues)
    hubSum = sum(hubValues)
    authSum = sum(authValues)
    hubValues /= hubSum
    authValues /= authSum
 
print("Base Set: ", baseSet)
print("Root Set: ", rootSet)
 
HubScores = []
AuthorityScores =[]
for i in range(len(baseSet)):
    HubScores.append((baseSet[i], hubValues[i]))
    AuthorityScores.append((baseSet[i], authValues[i]))
 
HubScores.sort(reverse=True, key=lambda x:x[1])
AuthorityScores.sort(reverse=True, key=lambda x:x[1])
 
print("\nHub Scores: ")
for i in range(len(baseSet)):
    print("Node", HubScores[i][0], " : ", HubScores[i][1])
 
print("\nAuthority Scores: ")
for i in range(len(baseSet)):
    print("Node", AuthorityScores[i][0], " : ", AuthorityScores[i][1])
 