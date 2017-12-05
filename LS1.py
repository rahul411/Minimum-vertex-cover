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
    
    
# cost function to calculate the cost of a certain solution
def cost(G,C):
    #Cost(G, C) = number of edges not covered by C′
    A = G.copy()
    A.remove_nodes_from(C)
    return A.number_of_edges()
    
def is_vertex_cover(G,C):
    if len(G.edges())==len(G.edges(C)):
        return True
    else:
        return False

def decision(probability):
    return random.random() < probability

def one_exchange(all,C):
    C_complement = [x for x in all if x not in C]
    u = random.choice(C)
    v = random.choice(C_complement)
    C_copy = C.copy()
    C_copy.remove(u)
    new_C = C_copy.copy()
    new_C.append(v)
    return new_C
    
def two_exchange(all,C):
    new_C = one_exchange(all,C)
    new_C = one_exchange(all,new_C)
    return new_C
    
    
    
def heuristic(C):  
    h_set = [] 
    for edge in C.edges():  
        if not edge[0] in h_set and not edge[1] in h_set:
#             if C.degree(edge[0]) >= C.degree(edge[1]):  
#                 node_choice = edge[0] 
#             else:  
#                 node_choice = edge[1] 

            node_choice = random.choice([edge[0],edge[1]])  
            h_set.append(node_choice) 
    return h_set
    
    

def LS1(graph,time_cutoff,random_seed,opt_solution_frame,graph_file):
    random.seed(random_seed)
    cutoff = time_cutoff
    filename = graph_file
    solution_file = './Output/'+graph+'_LS1_'+str(time_cutoff)+'_'+str(random_seed)+'.sol'
    trace_file = './Output/'+graph+'_LS1_'+str(time_cutoff)+'_'+str(random_seed)+'.trace'
    
    #graph_name = filename.split('/')[-1]
    #pdb.set_trace()
    graph_name = graph+'.graph'
    graph_opt_solution = opt_solution_frame.loc[graph_name][1]
    # read in the graph
    data = read_graph(filename)
    all_nodes = data.nodes()
    local_set = heuristic(data)
    start = time.time()
    elapsed_time = 0
#    pdb.set_trace()
    new_cost = -1
    previous_cost = 100
    with open(trace_file,'w') as output:
        
        while elapsed_time < cutoff:
            if new_cost < previous_cost:
                if is_vertex_cover(data,local_set):
                    print('%.2f,%d' % (elapsed_time,len(local_set)),file = output)
                    #print('%.2f,%d' % (elapsed_time,len(local_set)))
                    if len(local_set) == graph_opt_solution:
                        break
                    Temp = 100
                    cooling_ratio = 0.95
        #            print(str(len(local_set)))
        #            print(str(elapsed_time))
                    flag = False
                    for element in local_set:
                        local_set.remove(element)
                        
                        if is_vertex_cover(data,local_set):
                            flag = True
                            new_cost = 0
                            end = time.time()
                            elapsed_time = end-start
                            break
                        else:
                            local_set.append(element)
                    if flag == False:
                        eliminated_element = random.choice(local_set)
                        local_set.remove(eliminated_element)
                    continue
            # apply local search
            previous_cost = cost(data,local_set)
            loop_start = time.time()
            while True:
                loop_end = time.time()
                loop_time = loop_end - loop_start
                if loop_time < 100:
                    new_C = one_exchange(all_nodes,local_set)
                    #print('one exchanged')
                else:
                    new_C = two_exchange(all_nodes,local_set)
                new_cost = cost(data,new_C)
                if new_cost <= previous_cost:
                    local_set = new_C
                    Temp = Temp*cooling_ratio
                    break
                else:
                    delta = new_cost - previous_cost
                    p = math.exp(-delta / Temp)
                    if decision(p):
                        local_set = new_C
                        Temp = Temp*cooling_ratio
        #                print('uphill with probility '+str(p))
                        break
            end = time.time()
            elapsed_time = end-start
    with open(solution_file,'w') as output:
        output.write(str(len(local_set))+'\n')
        output.write(','.join(list(map(str, local_set))))
        
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
    LS1(graph,cutoff,random_seed,opt_solution_frame,graph_file)
    
#LS1('jazz',cutoff,random_seed,opt_solution_frame)

    
if __name__ == '__main__':
    main()


