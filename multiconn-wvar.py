# Kushagro Bhattacharjee, Caroline Lahti
# Supervised by: Dr. Ralucca Gera (Naval Postgraduate School)
# Supervised by: Karl Schmitt (Valparaiso University)
# Sponsored by: U.S. Dept. of Defense

import networkx as nx
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.axis as ax

class Alg():
    def __init__(self):
        self.graph = nx.read_gexf('C:\\Users\\localadmin\\Documents\\Networks\\networks_new\\G_final.gexf')

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

        self.connotation=0.0
        self.num_red_layers= int(input("How many red layers are in your graph (Default = 3)? "))
        self.num_blue_layers= int(input("How many blue layers are in your graph (Default = 7)? "))

        self.red_weights = []
        self.blue_weights = []
        print "Set your layer weights (Default = 1.0):"
        for rl in range(1,self.num_red_layers+1):
            rw = float(input("R"+str(rl)+" = "))
            self.red_weights.append(rw)
        for bl in range(1,self.num_blue_layers+1):
            bw = float(input("B"+str(bl)+" = "))
            self.blue_weights.append(bl)

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
            prev_conn = self.connotations_dict[neighbor]
            r1,r2,r3,b0,b1,b2,b3,b4,b5,b6,b7,b,r = (0,)*13
            if self.graph.edge[node][neighbor][0]['layer'] == 'R1':
                r1 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'R2':
                r2 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'R3':
                r3 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'B0':
                b0 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'B1':
                b1 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'B2':
                b2 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'B3':
                b3 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'B4':
                b4 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'B5':
                b5 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'B6':
                b6 += 1
            elif self.graph.edge[node][neighbor][0]['layer'] == 'B7':
                b7 += 1

            r=float(r1*self.red_weights[0]+r2*self.red_weights[1]+r3*self.red_weights[2])
            b=float(b0+b1*self.blue_weights[0]+b2*self.blue_weights[1]+b3*self.blue_weights[2]+b4*self.blue_weights[3]+b5*self.blue_weights[4]+b6*self.blue_weights[5]+b7*self.blue_weights[6])

            if neighbor not in self.monitor_set and node[0]=='B':
                conn=float(prev_conn)-float(float(r)/float(self.num_red_layers))+float(float(b)/float(self.num_blue_layers))
                self.connotations_dict[neighbor]=conn
                connList.append(conn)
            elif neighbor not in self.monitor_set and node[0]=='R':
                conn=float(float(float(prev_conn)-float(float(r)/float(self.num_red_layers))+float(float(b)/float(self.num_blue_layers)))*float(node_conn))
                self.connotations_dict[neighbor]=conn
                connList.append(conn)

        minConn=float('-inf')
        if(len(connList)>0):
            minConn=min(connList)
        for n,conn in self.connotations_dict.items():
            if conn==minConn:
                return n

if __name__ == '__main__':


    alg=Alg()

    currentMon = np.random.choice([x for x in alg.graph.nodes() if x not in alg.monitor_set and x[0]=='R'])
    #currentMon=alg.pick_start()
    mon_list=list()
    reds=list()
    output_seen_list=list()
    conn_list=list()
    red_plot_list=list()
    i=1

    while True:
        if(not alg.stop(len(alg.monitor_set))):
            if(alg.graph.has_node(currentMon) and currentMon not in alg.monitor_set):
                mon_list.append(i)
                i=i+1
                alg.monitor_set.add(currentMon)
                alg.monitor_free.remove(currentMon)
                output_seen_list.append(currentMon)
                if currentMon[0] == 'R':
                    alg.connotations_dict[currentMon] = -5
                    reds.append(currentMon)
                else:
                    alg.connotations_dict[currentMon] = 5
                currentMon=alg.place_next_monitor(currentMon)
            else:
                currentMon=alg.pick_start()
        else:
            break

    for node, conn in alg.connotations_dict.items():
        if(node not in conn_list):
            conn_list.append((node, conn))
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
    plt.margins(0.06, 0.05)
    plt.xlim(0,4000)
    plt.ylabel('% Discovered')
    plt.xlabel('Monitor')
    plt.plot(red_plot_list, color='red', label='MultiConn-WVar: '+str(alg.red_weights[0])+','+str(alg.red_weights[1])+','+str(alg.red_weights[2]))
    plt.legend(loc='lower right')
    fig = plt.gcf()
    #fig.savefig('json_multi.png',dpi=800)

    plt.figure(2)
    plt.margins(0.06, 0.05)
    plt.xlim(0,250)
    plt.ylabel('% Discovered')
    plt.xlabel('Monitor')
    plt.plot(red_plot_list, color='red', label='MultiConn-WVar: '+str(alg.red_weights[0])+','+str(alg.red_weights[1])+','+str(alg.red_weights[2]))
    plt.legend(loc='lower right')
    fig = plt.gcf()
    #fig.savefig('json_multi.png',dpi=800)
    plt.show()
