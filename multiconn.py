# Kushagro Bhattacharjee, Caroline Lahti
# Supervised by: Dr. Ralucca Gera (Naval Postgraduate School)
# Supervised by: Karl Schmitt (Valparaiso University)
# Sponsored by: U.S. Dept. of Defense

import networkx as nx
import numpy as np
import sys
import matplotlib.pyplot as plt


class Alg():
    def __init__(self):
        self.graph = nx.read_gexf('./networks_new/G_final.gexf')

        self.result_graph = nx.Graph()

        # Sets with/without monitors.
        self.monitor_set = set()
        self.monitor_free = nx.nodes(self.graph)  # Save this list to speed computations.

        # Internal dictionaries
        self.next_highest = {}
        self.seen = list()

        # Initialize all fake degrees to degree
        self.fake_degree = dict()
        # for node in self.monitor_free:
        for node in nx.nodes(self.graph):
            self.fake_degree[node] = self.graph.degree(node)

        # Set number of layers per color
        # (Layer weights do not play a factor in this version of MultiConn)
        self.num_red_layers=3.0
        self.num_blue_layers=7.0

        # Initialize all connotations to 0
        self.connotations_dict = dict()
        # for node in self.monitor_free:
        for node in nx.nodes(self.graph):
            self.connotations_dict[node] = 0

    # public method. Picks a random node that hasn't seen a monitor yet.
    # returns the node number
    def pick_start(self):
        start_node = np.random.choice([x for x in self.graph.nodes() if x not in self.monitor_set])
        #print("start_node: " + start_node)
        return start_node

    # public method. adds all edges (in NetworkX adding an edge adds the nodes if not already there)
    # from the node to all of its neighbors

    def stop(self, nodeNumber):
        if(self.graph.number_of_nodes()==nodeNumber):
            return True
        else:
            return False

    def place_next_monitor(self, node):
        self.monitor_set.add(node)

        node_conn = self.connotations_dict[node]

        neighbors = self.graph.neighbors(node)
        connList=list()
        for neighbor in neighbors:
            # Initialize blue edge sum and red edge sum between a node and its neighbor to 0
            blues=0.0
            reds=0.0
            # Set connotation of neighbor to 0 within this scope
            # prev_conn takes values of neighbor's previous connotation
            conn=0.0
            prev_conn=self.connotations_dict[neighbor]

            # check color of edge between neighbor and node
            if 'R' in self.graph.edge[node][neighbor][0]['layer']:
                blues += 1.0
            elif 'B' in self.graph.edge[node][neighbor][0]['layer']:
                reds += 1.0

            # check if source node of neighborhood is red or blue
            # (connotation of a neighbor is affected by color of source node)
            if neighbor not in self.monitor_set and node[0]=='B':
                conn=float(prev_conn)-float(float(reds)/float(self.num_red_layers))+float(float(blues)/float(self.num_blue_layers))
                self.connotations_dict[neighbor]=conn
                connList.append(conn)
            elif neighbor not in self.monitor_set and node[0]=='R':
                conn=float(float(float(prev_conn)-float(float(reds)/float(self.num_red_layers))+float(float(blues)/float(self.num_blue_layers)))*float(node_conn))
                self.connotations_dict[neighbor]=conn
                connList.append(conn)

        # Find most negative connotation among the node's neighbors, and return it
        minConn=float('-inf')
        if(len(connList)>0):
            minConn=min(connList)
        for n,conn in self.connotations_dict.items():
            if conn==minConn:
                return n

if __name__ == '__main__':


    alg=Alg()

    # Start algorithm on random red node
    currentMon = np.random.choice([x for x in alg.graph.nodes() if x not in alg.monitor_set and x[0]=='R'])

    mon_list=list()
    reds=list()
    # List of nodes in the order that they are seen
    output_seen_list=list()
    conn_list=list()
    red_plot_list=list()
    i=1

    while True:
        # If the number of nodes seen does not equal the total number of nodes in the graph
        if(not alg.stop(len(alg.monitor_set))):
            # If monitored node exists and has not been seen yet
            if(alg.graph.has_node(currentMon) and currentMon not in alg.monitor_set):
                mon_list.append(i)
                i=i+1
                alg.monitor_set.add(currentMon)
                alg.monitor_free.remove(currentMon)
                output_seen_list.append(currentMon)
                #print output_seen_list[0]

                if currentMon[0] == 'R':
                    # Set found red nodes to automatic connotation of -5
                    alg.connotations_dict[currentMon] = -5
                    # Append currentMon to list of red nodes in order they are seen
                    reds.append(currentMon)
                else:
                    # Set found blue nodes to automatic connotation of 5
                    alg.connotations_dict[currentMon] = 5
                currentMon=alg.place_next_monitor(currentMon)
            else:
                currentMon=alg.pick_start()
        else:
            break

    for node, conn in alg.connotations_dict.items():
        if(node not in conn_list):
            # Append tuple to conn_list
            conn_list.append((node, conn))
    # Sort tupled connotations list, most negative to most positive
    sorted_reds = sorted(conn_list, key=lambda tup: tup[1])

    red_plot_list = list()
    percent = 0
    for n in output_seen_list:
        if n in reds:
            percent = percent + (float(1)/len(reds))
            red_plot_list.append(percent)
        else:
            red_plot_list.append(percent)

    print "Red Nodes:" , len(reds), reds
    print "Connotations List:", len(conn_list), sorted_reds
    print "Seen List:", len(output_seen_list), output_seen_list
    print "XY Coordinates:" , red_plot_list

    plt.figure(1)
    # Margins aren't working on the y-axis
    plt.margins(0.06, 0.05)
    plt.xlim(0,4000)
    plt.ylabel('% Discovered')
    plt.xlabel('Monitor')
    plt.plot(red_plot_list, color='red', label='MultiConn')
    plt.legend(loc='lower right')
    plt.savefig('./MultiConn-4000.png', bbox_inches='tight')

    plt.figure(2)
    # Margins aren't working on the y-axis
    plt.margins(0.06, 0.05)
    plt.xlim(0,250)
    plt.ylabel('% Discovered')
    plt.xlabel('Monitor')
    plt.plot(red_plot_list, color='red', label='MultiConn')
    plt.legend(loc='lower right')
    plt.savefig('./MultiConn-250.png', bbox_inches='tight')

    plt.show()
