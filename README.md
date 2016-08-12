# multiconn.py

'''
Efficient multilayer network search algorithm. Find nodes of interest faster and more accurately with
the multiple-version Multilayer Connotation Discovery Algorithm, or MultiConn.
Written by Kushagro Bhattacharjee and Caroline Lahti, under the supervision of
Dr. Ralucca Gera (Naval Postgraduate School) and Prof. Karl Schmitt (Valparaiso University),
sponsored by the Department of Defense.
'''

'''
MultiConn is a new multilayer search algorithm. A given network is separated into layers of edges, according to their level of interest.
In our examples, edges are colored either red or blue. Red signifies an edge within a layer of interest.
Our network contained 3 red layers and 7 blue.

Nodes in our network are colored red or blue, depending on level of interest.
Our network contained 139 red nodes and 7375 blue nodes.

The algorithm searches for red nodes using a variable we like to call "connotation".

There are three versions of the algorithm:
(1) MultiConn (unweighted)
(2) MultiConn-W (auto-weighted) (red layers to 3-1-1 or 3-2-1, blue layers tp 1-1-1-1-1-1-1)
(3) MultiConn-WVar (user-weighted) (requires an IDE that allows input() while running code (ex: PyCharm))

Probed data includes information on a comparatively large and well-documented Indonesian terrorist network.
This data can be found at (https://sites.google.com/site/sfeverton18/research/appendix-1)
    Sean F. Everton, Associate Professor
    Defense Analysis Department
    589 Dyer Road, Root Hall, #203
    Naval Postgraduate School
    Monterey, CA 93943
Data also includes anonymyzed social network information from Facebook, via SNAP (http://snap.stanford.edu/data/index.html)
    Jure Leskovec and Andrej Krevl
    Stanford University
    SNAP Datasets: Large Network Dataset Collection
    June 2014
'''
