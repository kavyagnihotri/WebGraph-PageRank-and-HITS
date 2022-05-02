# WebGraph-PageRank-and-HITS

This repository has two python code files ``` code1.py ``` and ``` code2.py ```.

Part A: **Web Graph Page Ranking**
This aims at implementing the PageRank Algorithm from stratch. 
The algorithm is implemented with and without teleportations using numerical linear algebra package and **Power Iteration Method**

Usage: 
Run '''code1.py''' to run the program. The program allows user to enter the query.
```Functions and their uses:```


Part B: **Hyperlink Induced Topic Search (HITS) Algorithm**
This aims at implementing the HITS algorithm from stratch.  
The dataset is a Directed NetworkX Graph with web content (string) saved in a GraphPickle (web_graph.gpickle) file which needs to be loaded in the python runtime. You will need to install this library (if not already installed) by ```pip install networkx``` in the command prompt.

Usage:
Run ```code2.py``` to run the program.  The program allows the user to enter query.

The program finds a **root set** containing the nodes from the web graph which contains the query word. The program further finds the **base set** which contains all the nodes which are linked to the nodes in the root set.
The program runs the HITS algorithm on the webgraph/matrix made by this base set and outputs the hubs and authority score of the webpages in the base set.



