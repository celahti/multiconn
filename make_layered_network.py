# Data Source: https://sites.google.com/site/sfeverton18/research/appendix-1
# Code inspiration: Scott Warnke, NPS
# Caroline Lahti
# Supervised by: Dr. Ralucca Gera (Naval Postgraduate School)
# Supervised by: Karl Schmitt (Valparaiso University)
# Sponsored by: U.S. Dept. of Defense

def main():

    R_pct = 0.3; B_pct = 0.5

    R1_org = nx.read_gexf('C://Users/localadmin/Documents/Networks/layers/Knowledge.gexf')
    R2_org = nx.read_gexf('C://Users/localadmin/Documents/Networks/layers/TRUST.gexf')
    R3_org = nx.read_gexf('C://Users/localadmin/Documents/Networks/layers/LOC.gexf')

    R1 = red_node_relabel(R1_org,'R_')
    R2 = red_node_relabel(R2_org,'R_')
    R3 = red_node_relabel(R3_org,'R_')
    R1_final = edge_relabel(R1,'R1')
    R2_final = edge_relabel(R2,'R2')
    R3_final = edge_relabel(R3,'R3')

    R1_np = rand_node_list(R1_final,R_pct,False)
    R2_np = rand_node_list(R2_final,R_pct,False)
    R3_np = rand_node_list(R3_final,R_pct,False)


    print(nx.info(R1_final))
    print R1_final.nodes()
    print R1_final.edges(data=True)
    #print R1['R1_Rosihin Noor']['R1_Abdul Malik'][0]['layer']
    print(nx.info(R2_final))
    print R2_final.nodes()
    print(nx.info(R3_final))


    B1 = nx.read_gexf('C://Users/localadmin/Documents/Networks/layers/Knowledge.gexf')
    B1 = nx.convert_node_labels_to_integers(B1,first_label=1,ordering='default',label_attribute=None)
    B1 = blue_node_relabel(B1,"B1")
    B1_final = edge_relabel(B1,"B1")
    B1_np = rand_node_list(B1_final,B_pct,False)

    B2 = nx.read_gexf('C://Users/localadmin/Documents/Networks/layers/TRUST.gexf')
    B2 = nx.convert_node_labels_to_integers(B2,first_label=1,ordering='default',label_attribute=None)
    B2 = blue_node_relabel(B2,"B2")
    B2_final = edge_relabel(B2,"B2")
    B2_np = rand_node_list(B2_final,B_pct,False)

    B3 = nx.read_gexf('C://Users/localadmin/Documents/Networks/layers/LOC.gexf')
    B3 = nx.convert_node_labels_to_integers(B3,first_label=1,ordering='default',label_attribute=None)
    B3 = blue_node_relabel(B3,"B3")
    B3_final = edge_relabel(B3,"B3")
    B3_np = rand_node_list(B3_final,B_pct,False)

    B4 = nx.read_gexf('C://Users/localadmin/Documents/Networks/layers/NoordinTop.gexf')
    B4 = nx.convert_node_labels_to_integers(B4,first_label=1,ordering='default',label_attribute=None)
    B4 = blue_node_relabel(B4,"B4")
    B4_final = edge_relabel(B4,"B4")
    B4_np = rand_node_list(B4_final,B_pct,False)

    B5 = nx.barabasi_albert_graph(1390, 3)
    B5 = blue_node_relabel(B5,"B5")
    B5_final = edge_relabel(B5,"B5")
    B5_np = rand_node_list(B5_final,B_pct,False)

    B6 = nx.erdos_renyi_graph(1390,0.005)
    B6 = blue_node_relabel(B6,"B6")
    B6_final = edge_relabel(B6,"B6")
    B6_np = rand_node_list(B6_final,B_pct,False)

    B7 = nx.read_edgelist("C://Users/localadmin/Documents/Networks/layers/fb.txt",create_using = nx.Graph(),nodetype = int)
    B7 = blue_node_relabel(B7,"B7")
    B7_final = edge_relabel(B7,"B7")
    B7_np = rand_node_list(B7_final,B_pct,False)

    '''
    print(nx.info(B1))
    print(nx.info(B2))
    print(nx.info(B3))
    print(nx.info(B4))
    print(nx.info(B5))
    print(nx.info(B6))
    print(nx.info(B7))
    '''

    P01 = gen_purple(R1,B1_np,B2_np,B3_np,B4_np,B5_np,B6_np,B7_np)
    P02 = gen_purple(R2,R1_np,B2_np,B3_np,B4_np,B5_np,B6_np,B7_np)
    P03 = gen_purple(R3,B1_np,R1_np,B3_np,B4_np,B5_np,B6_np,B7_np)
    P04 = gen_purple(B1,B1_np,B2_np,R1_np,B4_np,B5_np,B6_np,B7_np)
    P05 = gen_purple(B2,B1_np,B2_np,B3_np,R1_np,B5_np,B6_np,B7_np)
    P06 = gen_purple(B3,B1_np,B2_np,B3_np,B4_np,R1_np,B6_np,B7_np)
    P07 = gen_purple(B4,B1_np,B2_np,B3_np,B4_np,B5_np,R1_np,B7_np)
    P08 = gen_purple(B5,B1_np,B2_np,B3_np,B4_np,B5_np,B6_np,R1_np)
    P09 = gen_purple(B6,B1_np,B2_np,B3_np,B4_np,B5_np,B6_np,R1_np)
    P10 = gen_purple(B7,B1_np,B2_np,B3_np,B4_np,B5_np,B6_np,R1_np)

    #'''
    print(nx.info(P01))
    tot=0
    for i in P01.nodes():
        tot += 1
        if i[3]=='A':
            print i
    print tot
    print(nx.info(P02))
    print(nx.info(P03))
    #'''

    G_final = purple_final(P01,P02,P03,P04,P05,P06,P07,P08,P09,P10)
    print(nx.info(G_final))
    print G_final.edges(data=True)

    '''
    gen_gexf(P01,"P01")
    gen_gexf(P02,"P02")
    gen_gexf(P03,"P03")
    gen_gexf(P04,"P04")
    gen_gexf(P05,"P05")
    gen_gexf(P06,"P06")
    gen_gexf(P07,"P07")
    gen_gexf(P08,"P08")
    gen_gexf(P09,"P09")
    gen_gexf(P10,"P10")
    '''
    gen_gexf(G_final,"G_final")

def gen_gexf(g,g_name):
    nx.write_gexf(g, 'C://Users/localadmin/Documents/Networks/networks_new/' + g_name + '.gexf')

def purple_final(g1,g2,g3,g4,g5,g6,g7,g8,g9,g10):

    g1.add_nodes_from(g2.nodes(data=True))
    g1.add_edges_from(g2.edges(data=True))

    g1.add_nodes_from(g3.nodes(data=True))
    g1.add_edges_from(g3.edges(data=True))

    g1.add_nodes_from(g4.nodes(data=True))
    g1.add_edges_from(g4.edges(data=True))

    g1.add_nodes_from(g5.nodes(data=True))
    g1.add_edges_from(g5.edges(data=True))

    g1.add_nodes_from(g6.nodes(data=True))
    g1.add_edges_from(g6.edges(data=True))

    g1.add_nodes_from(g7.nodes(data=True))
    g1.add_edges_from(g7.edges(data=True))

    g1.add_nodes_from(g8.nodes(data=True))
    g1.add_edges_from(g8.edges(data=True))

    g1.add_nodes_from(g9.nodes(data=True))
    g1.add_edges_from(g9.edges(data=True))

    g1.add_nodes_from(g10.nodes(data=True))
    g1.add_edges_from(g10.edges(data=True))

    return(g1)

def red_node_relabel(g,layer):
    map = {}
    for ix in g.nodes():
        map[ix] =  layer + str(ix)
    g=nx.relabel_nodes(g,map)
    return(g)

def edge_relabel(g,layer):
    nx.set_edge_attributes(g,'layer',layer)
    return(g)

def blue_node_relabel(g, label):
    map = {}
    for ix in g.nodes():
        map[ix] = label + "_" + str(ix)
    g=nx.relabel_nodes(g,map)
    return(g)

def gen_purple(base_g, nl_1, nl_2, nl_3, nl_4, nl_5, nl_6, nl_7):
    base_g = add_nodes(base_g,nl_1,3)
    base_g = add_nodes(base_g,nl_2,3)
    base_g = add_nodes(base_g,nl_3,3)
    base_g = add_nodes(base_g,nl_4,3)
    base_g = add_nodes(base_g,nl_5,3)
    base_g = add_nodes(base_g,nl_6,3)
    base_g = add_nodes(base_g,nl_7,3)
    return(base_g)

def gen_purple_final(base,g1,g2,g3,g4,g5,g6,g7,g8):
    P1 = node_relabel(g1,"P1")
    P2 = node_relabel(g2,"P2")
    P3 = node_relabel(g3,"P3")
    P4 = node_relabel(g4,"P4")
    P5 = node_relabel(g5,"P5")
    P6 = node_relabel(g6,"P6")
    P7 = node_relabel(g7,"P7")
    P8 = node_relabel(g8,"P8")

    if(base in "P1"):
        return(gen_purple(P1,nx.nodes(P2),nx.nodes(P3),nx.nodes(P4),nx.nodes(P5),nx.nodes(P6),nx.nodes(P7),nx.nodes(P8)))
    elif(base in "P2"):
        return(gen_purple(P2,nx.nodes(P1),nx.nodes(P3),nx.nodes(P4),nx.nodes(P5),nx.nodes(P6),nx.nodes(P7),nx.nodes(P8)))
    elif(base in "P3"):
        return(gen_purple(P3,nx.nodes(P1),nx.nodes(P2),nx.nodes(P4),nx.nodes(P5),nx.nodes(P6),nx.nodes(P7),nx.nodes(P8)))
    elif(base in "P4"):
        return(gen_purple(P4,nx.nodes(P1),nx.nodes(P2),nx.nodes(P3),nx.nodes(P5),nx.nodes(P6),nx.nodes(P7),nx.nodes(P8)))
    elif(base in "P5"):
        return(gen_purple(P5,nx.nodes(P1),nx.nodes(P2),nx.nodes(P3),nx.nodes(P4),nx.nodes(P6),nx.nodes(P7),nx.nodes(P8)))
    elif(base in "P6"):
        return(gen_purple(P6,nx.nodes(P1),nx.nodes(P2),nx.nodes(P3),nx.nodes(P4),nx.nodes(P5),nx.nodes(P7),nx.nodes(P8)))
    elif(base in "P7"):
        return(gen_purple(P7,nx.nodes(P1),nx.nodes(P2),nx.nodes(P3),nx.nodes(P4),nx.nodes(P5),nx.nodes(P6),nx.nodes(P8)))
    elif(base in "P8"):
        return(gen_purple(P8,nx.nodes(P1),nx.nodes(P2),nx.nodes(P3),nx.nodes(P4),nx.nodes(P5),nx.nodes(P6),nx.nodes(P7)))

def add_nodes(g, node_list, degree):
    org_g = g
    for ix in node_list:
        rand_nodes = random.sample(nx.nodes(org_g), degree)
        g.add_edge(ix,rand_nodes[0],layer='B0')
        g.add_edge(ix,rand_nodes[1],layer='B0')
        g.add_edge(ix,rand_nodes[2],layer='B0')
    return(g)

def rand_node_list(g, pct, censor):
    nodes = nx.nodes(g)
    node_indicies = random.sample(range(len(nodes)),int(len(nodes)*pct))
    if censor is True:
        return(node_indicies)
    else:
        return([nodes[i] for i in node_indicies])

if __name__=="__main__":
    import numpy as np
    import time, pandas, sys, joblib, random
    import networkx as nx
    import matplotlib.pyplot as plt
    from numpy import linalg as LA
    from joblib import Parallel, delayed

    main()
