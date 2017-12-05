import networkx as nx
import random
import time
import sys

"""
simple graph test

"""
#
#
# g = nx.Graph()
#
# g.add_node(1)  # specify node number
# g.add_node(5)
#
# g.add_edge(1, 2)
# g.add_edge(2, 1)
# g.add_edge(1, 5)
# g.add_edges_from([(2, 1), (2, 3), (3, 2), (3, 4), (3, 6), (4, 6), (4, 5), (5, 6), (6, 7)])


"""
read graph from file

"""


def create_graph(file_name):

    g = nx.Graph()
    i = 0
    with open(file_name, "r") as my_graph:
        for line in my_graph:
            if i != 0 and i <= v:
                g.add_node(i)
                adj_list = line.strip().split(' ')
                for j in adj_list:
                    if j != '' and j != ' ':
                        j = int(j)
                        g.add_edge(i, j)
            else:
                info = line.strip().split(' ')
                v = info[0]
                e = info[1]
            i += 1

    print i

    print nx.info(g)
    return g


def find_max(sorted_degree):
    max_degree = 0
    for degree in sorted_degree:
        if max_degree < degree:
            max_degree = degree
    return max_degree


def approximation_greedy_vc(g):

    v = nx.number_of_nodes(g)
    e = nx.number_of_edges(g)

    edge_set = set()
    vertex_set = set()
    degree_of_node = dict({})

    for node in nx.nodes(g):
        deg = nx.degree(g, node)
        if deg in degree_of_node:
            degree_of_node[deg].append(node)
        else:
            degree_of_node[deg] = [node]
        # print ("degree of %d is %d" % (node, nx.degree(g, node)))

    """
    for key in degree_of_node:
        print ("degree %d : " % key)
        for node in degree_of_node[key]:
            print ",", node
    """

    sorted_degree = [0]
    for i in range(1, v + 1):
        sorted_degree.append(nx.degree(g, i))
        # print 'node ', i
        # print 'degree', sorted_degree[i]

    while len(edge_set) != 2 * e:
        current_max = find_max(sorted_degree)
        if degree_of_node[current_max] is None or len(degree_of_node[current_max]) == 0:
            current_max -= 1
            continue
        nodes_with_current_degree = degree_of_node[current_max]
        random_choice = random.randint(0, len(nodes_with_current_degree) - 1)   # [0, len-1]
        chosen_node = nodes_with_current_degree[random_choice]

        vertex_set.add(chosen_node)
        for neighbor in nx.all_neighbors(g, chosen_node):
            if neighbor not in vertex_set:
                edge_set.update([(chosen_node, neighbor), (neighbor, chosen_node)])
                degree_of_node[sorted_degree[neighbor]].remove(neighbor)  # remove
                sorted_degree[neighbor] -= 1
                if sorted_degree[neighbor] not in degree_of_node:
                    degree_of_node[sorted_degree[neighbor]] = []
                degree_of_node[sorted_degree[neighbor]].append(neighbor)  # add

        degree_of_node[current_max].remove(chosen_node)
        sorted_degree[chosen_node] = 0

    return vertex_set


def test_and_run(file_name):
    # print 'file name:', str(sys.argv[1])
    # file_name = str(sys.argv[1])
    g = create_graph(file_name)
    graph = file_name.rstrip().split('/')[-1].split('.')[0]
    

    start = time.time()
    vertex_cover = approximation_greedy_vc(g)
    end = time.time()
    print len(vertex_cover)
    print ("time is %f" % (end - start))

    with open('output/'+graph.split('.')[0] + "_approx.sol", "w") as my_output:
        my_output.write(str(len(vertex_cover)) + '\n')
        for vx in vertex_cover:
            my_output.write(str(vx) + ',')


# test_and_run()











