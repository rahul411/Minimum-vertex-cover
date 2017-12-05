import networkx as nx
import time
import sys
from networkx.utils import UnionFind
import pdb
import matplotlib.pyplot as plt
import random
import math
import pandas as pd
import os

def read_graph(filename):

    G = nx.MultiGraph()
    #if you want to use networkx
    #Write code to add nodes and edges
    with open(filename,'r') as input_f:
        info = input_f.readline().rstrip().split(' ')
        total_N, total_E = map(lambda x: int(x), info[:2])
        G.add_nodes_from(range(1,total_N+1))
        i = 1
        #pdb.set_trace()
        
        for line in input_f:
            if line.strip() != '':
                start = i
                ends = map(lambda x: int(x), line.rstrip().split(' '))
                for end in ends:
                    G.add_edge(start,end)
                i += 1
    return G

def is_vertex_cover(G,C):
    if len(G.edges())==len(G.edges(C)):
        return True
    else:
        return False

def heuristic(C):  
    h_set = [] 
    for edge in C.edges():  
        if not edge[0] in h_set and not edge[1] in h_set:
            if C.degree(edge[0]) >= C.degree(edge[1]):  
                node_choice = edge[0] 
            else:  
                node_choice = edge[1] 
            h_set.append(node_choice) 
    return h_set

def LS2(graph,time_cutoff,random_seed,opt_solution_frame,graph_file):
    #pdb.set_trace()
    start = time.time()
    random.seed(random_seed)
    cutoff = time_cutoff
    filename = graph_file
    solution_file = './Output/'+graph+'_LS2_'+str(time_cutoff)+'_'+str(random_seed)+'.sol'
    trace_file = './Output/'+graph+'_LS2_'+str(time_cutoff)+'_'+str(random_seed)+'.trace'
    graph_name = graph+'.graph'
    graph_opt_solution = opt_solution_frame.loc[graph_name][1]
    # read in the graph
    data = read_graph(filename)
    all_nodes = data.nodes()
    all_edges = data.edges()
    #local_set = heuristic(data)
    local_set = all_nodes
    local_set_length = len(local_set)
    best_so_far = local_set
    best_so_far_len = local_set_length
    i = 0
    elapsed_time = 0
    Temp = 100
    cooling_ratio = 0.999
    with open(trace_file,'w') as output:
        while elapsed_time < cutoff:
            if best_so_far_len == graph_opt_solution:
                break
            while i < 10:
                index = random.choice(local_set)
                remove = True
                for edge in data.edges(index):
                    if edge[1] not in local_set:
                        remove = False
                if remove:
                    local_set.remove(index)
                    local_set_length -= 1
                    i += 1
                    if local_set_length < best_so_far_len:
                        best_so_far = local_set
                        best_so_far_len = local_set_length
                        end = time.time()
                        elapsed_time = end-start
                        print('%.2f,%d' % (elapsed_time,len(local_set)),file = output)
#                        print('%.2f,%d' % (elapsed_time,local_set_length))
                else:
                    p = math.exp(-1 / Temp)
                    if random.random() < p:
                        index = random.choice(list(set(data.nodes()) - set(local_set)))
                        local_set.append(index)
                        local_set_length += 1
                        i += 1
                        #print('set increased')
                end = time.time()
                elapsed_time = end-start
            i = 0
            Temp *= cooling_ratio
    with open(solution_file,'w') as output:
        output.write(str(best_so_far_len)+'\n')
        output.write(','.join(list(map(str, best_so_far))))
        

def main():
    #pdb.set_trace()
    opt_solutions = './optimum_solution.xlsx'
    opt_solution_frame = pd.read_excel(opt_solutions, sheetname='Sheet1',header = None,index_col = 0)

   
    num_args = len(sys.argv)
    if num_args < 4:
        print ("error: not enough input arguments")
        exit(1)
    graph_file = sys.argv[1]
    graph = graph_file.rstrip().split('/')[-1].split('.')[0]
    
    cutoff = int(sys.argv[2]) 
    random_seed = int(sys.argv[3]) 
    LS2(graph,cutoff,random_seed,opt_solution_frame,graph_file)
    
#LS1('jazz',cutoff,random_seed,opt_solution_frame)

    
if __name__ == '__main__':
    main()
