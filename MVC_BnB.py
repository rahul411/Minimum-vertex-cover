# implementation of branch_and_bound algorithm

import networkx as nx
from priorityq import indexMinPQ
import time
import sys
import re

class Graph:

    def read_graph(self,filename):
        """read in a graph file from filename, and return a graph object (as in networkx)"""
        with open(filename, 'r') as graphFile:
            nodes, noEdges, _ = graphFile.readline().split(' ')

            G = nx.Graph()
            i = 1
            for line in graphFile:
                edgeEnds = list(map(lambda x: int(x), line.split()))
                edges = [(i, v) for v in edgeEnds]
                G.add_edges_from(edges)
                i += 1

        return G

class MVC:
    traceFileName = ''
    outputFileName = ''

    #This function computes the approximate lower bound by edge deletion. It has an approximation ratio of 2.
    def approxMVC(self, graph):
        visited = set()
        visited_edges = set()

        for u, v in graph.edges_iter():
            # if edge (u, v) is not covered, add u and v to the visited
            #  and add all the edges that are adjacent to u or v to visited_edges
            if (u, v) not in visited_edges and (v, u) not in visited_edges:
                visited.add(u)
                visited.add(v)
                visited_edges = visited_edges | set(graph.edges([u, v]))

        return list(visited)

    #This function returns the vertex with the maximum degree
    def maxDegreeVertex(self, G, sub_V):
        maximum = -1
        vertex = -1
        vertexDict = G.degree(sub_V)
        for i in vertexDict:
            if maximum < vertexDict[i]:
                maximum = vertexDict[i]
                vertex = i
        return vertex        

    #This function constructs the residual graph by removing the nodes in the removal_V and all its neighbors
    def residual_graph(self, G, removal_V):
        if not isinstance(removal_V, list):
            removal_V = [removal_V]
        return [ v for v in G.nodes() if (v not in removal_V
                                 and not set(G.neighbors(v)) < set(removal_V)) ]

    def isCover(self, node, sub_V, G):
        is_cover = True
        neighbors = set(G.neighbors(node))
        if len(neighbors) > 0 and not neighbors <= set(sub_V):
            is_cover = False
        return is_cover

    def MVC_BnB(self, G, cutOffTime):

        initialUpdaterate = 10

        if G.number_of_nodes() > 10000:
            initialUpdaterate = G.number_of_nodes()/500
        
        trace = open(self.traceFileName, 'w')
        start_time = time.time()


        sub_problems = indexMinPQ()
        approxVC = self.approxMVC(G)
        lowerBound = len(approxVC)/2
        sub_problems.push( (None, tuple(G.nodes()), tuple(G.nodes()), lowerBound),
                            G.number_of_edges())

        #Initialize the optimum to the approximate vertex cover
        optimum = (len(approxVC), approxVC)

        current_time = time.time() - start_time
        trace.write(str(current_time) + ', ' + str(optimum[0]) + '\n')
        counter = 0

        while not sub_problems.isEmpty():
            subProblem = sub_problems.pop()

            if subProblem[0] is None:
                sub_cover = []
            else:
                sub_cover = list(subProblem[0])                      
            available_vertices = list(subProblem[1])                 
            remaining_graph = G.subgraph(list(subProblem[2]))        
            currentLowerbound = subProblem[3]

            if currentLowerbound >= optimum[0]:
                pass

            if len(subProblem[2]) < 500:
                updateRate = 1
            else:
                updateRate = initialUpdaterate    

            max_degree_v = self.maxDegreeVertex(remaining_graph, available_vertices) 

            cover_add_v = list(sub_cover)
            cover_add_v.append(max_degree_v)   
            new_residual_vertices = self.residual_graph(remaining_graph, max_degree_v)  
            new_available_vertices = list(set(new_residual_vertices) & set(available_vertices))  
            new_residual_graph = G.subgraph(new_residual_vertices)

            if nx.number_of_edges( new_residual_graph ) == 0:   
                #Check if new optimum found, if yes update the optimum    
                if len(cover_add_v) < optimum[0]:              
                    optimum = (len(cover_add_v), cover_add_v)

                    current_time = time.time() - start_time
                    trace.write(str(current_time) + ', ' + str(optimum[0]) + '\n')

            elif len(new_available_vertices) > 0:                  
                
                if counter % updateRate == 0:
                    lowerBound = len(cover_add_v) + len(self.approxMVC(new_residual_graph))/2
                    counter = 0
                else:
                    lowerBound = currentLowerbound
                counter += 1
                            
                if lowerBound < optimum[0]:                           
                    sub_problems.push((tuple(cover_add_v), tuple(new_available_vertices),
                                       tuple(new_residual_vertices), lowerBound),
                                       new_residual_graph.number_of_edges())

            
            cover_unselect_v = list(sub_cover)
            available_vertices_delete_v = list(available_vertices)
            available_vertices_delete_v.remove(max_degree_v)

            
            if len(available_vertices_delete_v) > 0 and self.isCover(max_degree_v, available_vertices_delete_v, remaining_graph):
                if currentLowerbound < optimum[0]:
                    sub_problems.push((tuple(cover_unselect_v), tuple(available_vertices_delete_v),
                                       subProblem[2], currentLowerbound), remaining_graph.number_of_edges())

            
            if time.time() - start_time > cutOffTime:
                break

        trace.close()
        output = open(self.outputFileName, 'w')
        result = list(optimum[1])
        result = sorted(result)
        output.write(str(optimum[0])+'\n' + ' '.join(str(v)for v in result))
        result = list(optimum[1])
        result = sorted(result)
        output.close()


def BNB(filename,time):

    # num_args = len(sys.argv)

    # if num_args < 3:
    #     print ("error: not enough input arguments")
    #     exit(1)

    graph_file = filename
    
    cutOffTime = time
    minimumVertexCover = MVC()
    graphName = re.findall(r'\\?(\w+\-?\_?\w+).graph',graph_file)
    
    # print(graphName)
    minimumVertexCover.traceFileName = 'output\\' + graphName[0] + '_BnB_' + str(cutOffTime) + '.trace'
    minimumVertexCover.outputFileName = 'output\\' + graphName[0] + '_BnB_' + str(cutOffTime) + '.sol'  

    graph = Graph()
    G = graph.read_graph(graph_file)

    minimumVertexCover.MVC_BnB(G, cutOffTime)

if __name__ == '__main__':
    main()
