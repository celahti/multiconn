import networkx as nx
import numpy as np
import sys
import matplotlib.pyplot as plt



class Alg():
    def __init__(self):
        self.graph = nx.read_gexf('C:\\Users\\localadmin\\Downloads\\G_final(1).gexf')

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
        self.num_red_layers=3.0
        self.num_blue_layers=7.0


        self.weight_red_layer=1
        self.weight_blue_layer=1
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
        degList=list()
        for neighbor in neighbors:
            degree = self.graph.degree(neighbor)
            degList.append(degree)
            blues=0.0
            reds=0.0
            conn=0.0
            if int(self.graph.edge[node][neighbor][0]['id']) > 1050:
                blues += 1.0
            elif int(self.graph.edge[node][neighbor][0]['id']) < 1050:
                reds += 1.0

            if neighbor not in self.monitor_set and node[0]=='B':
                prev_conn=self.connotations_dict[neighbor]
                conn=float(prev_conn)-float(float(reds)/float(self.num_red_layers))+float(float(blues)/float(self.num_blue_layers))
                self.connotations_dict[neighbor]=conn
                connList.append(conn)
            elif neighbor not in self.monitor_set and node[0]=='R':
                prev_conn=self.connotations_dict[neighbor]
                conn=float(float(float(prev_conn)-float(float(reds)/float(self.num_red_layers))+float(float(blues)/float(self.num_blue_layers)))*float(node_conn))
                self.connotations_dict[neighbor]=conn
                connList.append(conn)
        #2-hop
        for neighbor in neighbors:
            neighbors2=self.graph.neighbors(neighbor)
            for n in neighbors2:
                blues=0.0
                reds=0.0
                conn=0.0
                if int(self.graph.edge[neighbor][n][0]['id']) > 1050:
                    blues += 1.0
                elif int(self.graph.edge[neighbor][n][0]['id']) < 1050:
                    reds += 1.0

                if n not in self.monitor_set and node[0]=='B':
                    prev_conn=self.connotations_dict[n]
                    conn=float(prev_conn)-float(float(reds)/float(self.num_red_layers))+float(float(blues)/float(self.num_blue_layers))
                    self.connotations_dict[n]=conn
                    connList.append(conn)
                elif n not in self.monitor_set and node[0]=='R':
                    prev_conn=self.connotations_dict[n]
                    conn=float(float(float(prev_conn)-float(float(reds)/float(self.num_red_layers))+float(float(blues)/float(self.num_blue_layers)))*float(node_conn))
                    self.connotations_dict[n]=conn
                    connList.append(conn)


        minConn=float('-inf')
        if(len(connList)>0):
            minConn=min(connList)
        for n,conn in self.connotations_dict.items():
            if conn==minConn:
                return n

if __name__ == '__main__':


    alg=Alg()

    currentMon=alg.pick_start()
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

    print ("Red Nodes:" , len(reds), reds)
    print ("Connotations List:", len(conn_list), sorted_reds)
    print ("Seen List:", len(output_seen_list), output_seen_list)
    print ("XY Coordinates:" , red_plot_list)
    plt.plot(mon_list, red_plot_list, 'ro')
    axes=plt.gca()
    axes.set_ylim([0,1])
    axes.set_xlim([0,4000])
    plt.xlabel('Number of Monitors Seen',fontsize=15)
    plt.ylabel('% Red Discovered',fontsize=15)
    plt.title('MultiConn Red Node Discovery', fontsize=18)
    plt.show()
