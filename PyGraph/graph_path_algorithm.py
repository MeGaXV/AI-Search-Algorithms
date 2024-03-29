import sys
from queue import PriorityQueue

from queue import Queue
from queue import LifoQueue

import heapq
import random

''' Graph Path Algortihm File
  
    Author: Sharif Shaker
    Date: 4/29/2017
    
    Modified: 3/11/2021
    Authors: Abdel-Rahman Megahed, Maryam Nouh, Seif Elewa, Youssef Mansi
    Changes made:  Functionality for running bfs, dfs, ucs, greedy and a* search algorithms added.


    Description:
        This file contains graph shortest path finding, and minimum spanning tree algorithms

'''


#########UCS#########
def UCS(graph, from_v, to_v_list):
    q = PriorityQueue()  # create a priority queue
    node_dict = {}  # create a node dictionary to return a distance, parent pair given a node value
    current = (None, None)  # holds the currently selected node
    edge_w = None  # holds weight

    if to_v_list is None: to_v_list = node_dict.keys()  # if no node was input, find path to all nodes

    # make sure start node is valid
    if from_v not in graph.nodes_dict:
        print('Invalid start node of ' + str(from_v))
        return
    # make sure destination nodes are valid
    for node in to_v_list:
        if node not in graph.nodes_dict:
            print('Invalid end node of ' + str(node))
            return

    # set up algorithm start conditions
    for node in graph.nodes_dict.keys():  # for each node
        if node == from_v:  # if node is the start node
            q.put((0, node))  # put node in queue with 0 distance
            node_dict[node] = (0, node)  # put into dictionary with 0 distance and itself as a parent
        else:
            node_dict[node] = (
                float('inf'), None)  # put all other nodes in dictionary with largest possible distance and no parent
    visited = []  # visited node list
    found = False
    x = None
    # search graph
    while not q.empty():
        current = q.get()  # get node with shortest distance from start
        if current[1] not in visited:
            visited.append(current[1])
        else:
            continue
        for adj_node in graph.nodes_dict[current[1]]:  # for each adjacent node
            edge_w = graph.edges_dict[(current[1], adj_node)]  # find weight
            if edge_w < 0: return [('Invalid', -1, None)]  # negative weight not allowed
            dist = current[0] + edge_w  # find total distance
            if dist < node_dict[adj_node][0]:  # if distance to start is less than it originally was
                q.put((dist, adj_node))  # put new dist parent pair in queue
                node_dict[adj_node] = (dist, current[1])  # change value in node dictionary
        for n in to_v_list:
            if current[1] == n:
                found = True
                x = n
        if found: break

    result = []
    path = [x]
    total_dist = node_dict[x][0]  # set total distance to dist from start to goal node
    if total_dist == float('inf'):  # if path wasn't found
        result.append((x, total_dist, None))  # return result with None
    else:
        while path[0] != from_v:  # while node at 0 index is not start node
            path.insert(0, node_dict[path[0]][1])  # insert parent into 0 index of path
        result.append((x, total_dist, path))  # add path to result list

    return result


#########A*#########
def Astar(graph, from_v, to_v=None):
    q = PriorityQueue()  # Create a priority queue
    node_dict = {}  # create a node dictionary to return a distance, parent pair given a node value
    current = (None, None)  # holds the currently selected node
    node_h = None  # Heuristic for current selected node

    if to_v is None: to_v = node_dict.keys()  # if no node was input, find path to all nodes

    # make start node is valid
    if from_v not in graph.nodes_dict:
        print('Invalid start node of ' + str(from_v))
        return
    # make sure goal nodes are valid
    for node in to_v:
        if node not in graph.nodes_dict:
            print('Invalid end node of ' + str(node))
            return

    # set up algorithm starting conditions
    for node in graph.nodes_dict.keys():  # for each node
        if node == from_v:  # if node is the start node
            q.put((0, node))  # put node in queue with 0 distance
            node_dict[node] = (0, node)  # put into dictionary with 0 distance and itself as a parent

    visited = []  # visited nodes list
    found = False  # Goal found flag
    x = None
    dist = 0
    # search algorithm
    while not q.empty():
        current = q.get()  # get node with shortest distance from start
        if current[1] not in visited:  # check if current selected node is visited
            visited.append(current[1])  # add node to visited list
        else:
            continue  # skip node from search if it is already visited
        for adj_node in graph.nodes_dict[current[1]]:  # for each adjacent node
            edge_w = graph.edges_dict[(current[1], adj_node)]  # find weight
            if edge_w < 0: return [('Invalid', -1, None)]  # negative weight not allowed
            node_h = graph.heuristic_dict[adj_node]  # get the heuristic value for adjacent node
            # dist = graph.edges_dict[(current[1]), adj_node] + edge_w  # add new edge to previous path weight
            if node_h < 0: return [('Invalid', -1, None)]  # negative heuristic not allowed
            if adj_node not in visited:  # check if adjacent node is in visited
                fn = node_h + edge_w  # calculate fn where fn = heuristic value + distance to node
                q.put((fn, adj_node))  # put new fn parent pair in queue
                node_dict[adj_node] = (node_h, current[1])  # change value in node dictionary
        for n in to_v:
            if current[1] == n:
                found = True
                x = n
        if found: break

    result = []
    path = [x]
    if not found:  # if path wasn't found
        result.append((x, dist, None))  # return result with None
    else:
        while path[0] != from_v:  # while node at 0 index is not start node
            path.insert(0, node_dict[path[0]][1])  # insert parent into 0 index of path
        for index, elem in enumerate(path):
            if index + 1 <= len(path) and index - 1 >= 0:
                dist = graph.edges_dict[path[index - 1], elem] + dist  # add new edge to previous path weight
        result.append((x, dist, path))  # add path to result list
    return result


#########GREEDY#########
def Greedy(graph, from_v, to_v=None):
    q = PriorityQueue()  # create a priority queue
    node_dict = {}  # create a node dictionary to return a distance, parent pair given a node value
    current = (None, None)  # holds the currently selected node
    node_h = None  # Heuristic for current selected node

    if to_v is None: to_v = node_dict.keys()  # if no node was input, find path to all nodes

    # make start node is valid
    if from_v not in graph.nodes_dict:
        print('Invalid start node of ' + str(from_v))
        return

    # make sure destination nodes are valid
    for node in to_v:
        if node not in graph.nodes_dict:
            print('Invalid end node of ' + str(node))
            return

    # set up algorithm start conditions
    for node in graph.nodes_dict.keys():  # for each node
        if node == from_v:  # if node is the start node
            q.put((0, node))  # put node in queue with 0 distance
            node_dict[node] = (0, node)  # put into dictionary with 0 distance and itself as a parent

    visited = []  # visited nodes list
    found = False  # Goal found flag
    dist=0
    # search algorithm
    while not q.empty():
        current = q.get()  # get node with shortest distance from start
        if current[1] not in visited:  # check if current selected node is visited
            visited.append(current[1])  # add node to visited list
        else:
            continue  # skip node from search if it is already visited
        for adj_node in graph.nodes_dict[current[1]]:  # for each adjacent node
            node_h = graph.heuristic_dict[adj_node]  # get the heuristic value for adjacent node
            if node_h < 0: return [('Invalid', -1, None)]  # negative heuristic not allowed
            if adj_node not in visited:  # check if adjacent node is in visited
                q.put((node_h, adj_node))  # put new dist parent pair in queue
                node_dict[adj_node] = (node_h, current[1])  # change value in node dictionary
        for n in to_v:
            if current[1] == n:
                x = n
                found = True
        if found: break

    result = []
    path = [x]
    total_dist = node_dict[x][0]  # set total distance to dist from start to goal node
    if not found:  # if path wasn't found
        result.append((x, dist, None))  # return result with None
    else:
        while path[0] != from_v:  # while node at 0 index is not start node
            path.insert(0, node_dict[path[0]][1])  # insert parent into 0 index of path
        for index, elem in enumerate(path):
            if index + 1 <= len(path) and index - 1 >= 0:
                dist = graph.edges_dict[path[index - 1], elem] + dist  # add new edge to previous path weight
        result.append((x, dist, path))  # add path to result list

    return result


#########DFS#########
def DepthFirst(graph, from_v, to_v=None):
    q = LifoQueue()  # create a priority queue
    node_dict = {}  # create a node dictionary to return a distance, parent pair given a node value
    current = (None, None)  # holds the currently selected node
    edge_w = None  # holds weight

    if to_v is None: to_v = from_v  # if no node was input, find path to all nodes
    # to_v = to_v.split()
    # make sure start node is valid
    if from_v not in graph.nodes_dict:
        print('Invalid start node of ' + str(from_v))
        return

    # make sure destination nodes are valid
    for n in to_v:
        if n not in graph.nodes_dict:
            print('Invalid end node of ' + str(to_v))
            return

    # set up algorithm start conditions
    for node in graph.nodes_dict.keys():  # for each node
        if node == from_v:  # if node is the start node
            q.put((0, node))  # put node in queue with 0 distance
            node_dict[node] = (0, node)  # put into dictionary with 0 distance and itself as a parent
        else:
            node_dict[node] = (
                float('inf'), None)  # put all other nodes in dictionary with largest possible distance and no parent

    visited = []
    found = False
    # search graph
    while not q.empty():
        current = q.get()  # get node with shortest distance from start
        # check if node is already visited
        if current[1] not in visited:
            visited.append(current[1])
        else:
            continue
        for adj_node in graph.nodes_dict[current[1]]:  # for each adjacent node
            edge_w = graph.edges_dict[(current[1], adj_node)]  # find weight
            if edge_w < 0: return [('Invalid', -1, None)]  # negative weight not allowed
            dist = current[0] + edge_w  # find total distance
            if adj_node not in visited:  # if distance to start is less than it originally was
                q.put((dist, adj_node))  # put new dist parent pair in queue
                node_dict[adj_node] = (dist, current[1])  # change value in node dictionary
        print(current)
        # check if current is goal
        for n in to_v:
            if current[1] == n:
                found = True
                x = n
        if found: break

    result = []
    path = [x]
    total_dist = node_dict[x][0]  # set total distance to dist from start to goal node
    if total_dist == float('inf'):  # if path wasn't found
        result.append((x, total_dist, None))  # return result with None
    else:
        while path[0] != from_v:  # while node at 0 index is not start node
            path.insert(0, node_dict[path[0]][1])  # insert parent into 0 index of path

        result.append((x, total_dist, path))  # add path to result list

    return result


#########BFS#########
def BreadthFirst(graph, from_v, to_v_list=None):
    q = Queue()  # create a queue
    node_dict = {}  # create a node dictionary to return a distance, parent pair given a node value
    current = (None, None)  # holds the currently selected node
    edge_w = None  # holds weight

    if to_v_list is None: to_v_list = node_dict.keys()  # if no node was input, find path to all nodes

    # make start node is valid
    if from_v not in graph.nodes_dict:
        print('Invalid start node of ' + str(from_v))
        return

    # make sure destination nodes are valid
    for node in to_v_list:
        if node not in graph.nodes_dict:
            print('Invalid end node of ' + str(node))
            return

    # set up algorithm start conditions
    for node in graph.nodes_dict.keys():  # for each node
        if node == from_v:  # if node is the start node
            q.put((0, node))  # put node in queue with 0 distance
            node_dict[node] = (0, node)  # put into dictionary with 0 distance and itself as a parent
        else:
            node_dict[node] = (
                float('inf'), None)  # put all other nodes in dictionary with largest possible distance and no parent

    visited = []
    found = False
    # search graph
    while not q.empty():
        current = q.get()  # get node with shortest distance from start
        # check if node is already visited
        print(current)
        if current[1] not in visited:
            visited.append(current[1])
        else:
            continue
        for adj_node in graph.nodes_dict[current[1]]:  # for each adjacent node
            edge_w = graph.edges_dict[(current[1], adj_node)]  # find weight
            if edge_w < 0: return [('Invalid', -1, None)]  # negative weight not allowed
            dist = current[0] + edge_w  # find total distance
            if adj_node not in visited:  # if node isn't visited
                q.put((dist, adj_node))  # put new dist parent pair in queue
            if node_dict[adj_node][0] == float('inf'):
                node_dict[adj_node] = (dist, current[1])  # change value in node dictionary
        # check if current is goal
        for n in to_v_list:
            if current[1] == n:
                found = True
                x = n
        if found: break

    result = []
    path = [x]
    total_dist = node_dict[x][0]  # set total distance to dist from start to goal node
    if total_dist == float('inf'):  # if path wasn't found
        result.append((x, total_dist, None))  # return result with None
    else:
        while path[0] != from_v:  # while node at 0 index is not start node
            path.insert(0, node_dict[path[0]][1])  # insert parent into 0 index of path
        result.append((x, total_dist, path))  # add path to result list

    return result


#########DIJKSTRA#########
def dijkstra(graph, from_v, to_v_list=None):
    q = PriorityQueue()  # create a priority queue
    node_dict = {}  # create a node dictionary to return a distance, parent pair given a node value
    current = (None, None)  # holds the currently selected node
    edge_w = None

    if to_v_list is None: to_v_list = node_dict.keys()  # if no node was input, find path to all nodes

    # make start node is valid
    if from_v not in graph.nodes_dict:
        print('Invalid start node of ' + str(from_v))
        return

    # make sure destination nodes are valid
    for node in to_v_list:
        if node not in graph.nodes_dict:
            print('Invalid end node of ' + str(node))
            return

    # set up algorithm start conditions
    for node in graph.nodes_dict.keys():  # for each node
        if node == from_v:  # if node is the start node
            q.put((0, node))  # put node in queue with 0 distance
            node_dict[node] = (0, node)  # put into dictionary with 0 distance and itself as a parent
        else:
            node_dict[node] = (
                float('inf'), None)  # put all other nodes in dictionary with largest possible distance and no parent

    while not q.empty():
        current = q.get()  # get node with shortest distance from start
        for adj_node in graph.nodes_dict[current[1]]:  # for each adjacent node
            edge_w = graph.edges_dict[(current[1], adj_node)]
            if edge_w < 0: return [('Invalid', -1, None)]
            dist = current[0] + edge_w
            if dist < node_dict[adj_node][0]:  # if distance to start is less than it originally was
                q.put((dist, adj_node))  # put new dist parent pair in queue
                node_dict[adj_node] = (dist, current[1])  # change value in node dictionary

    result = []
    for node in to_v_list:  # go through all end nodes
        path = [node]
        total_dist = node_dict[node][0]  # set total distance to dist from start to goal node
        if total_dist == float('inf'):  # if path wasn't found
            result.append((node, total_dist, None))  # return result with None
        else:
            while path[0] != from_v:  # while node at 0 index is not start node
                path.insert(0, node_dict[path[0]][1])  # insert parent into 0 index of path
            result.append((node, total_dist, path))  # add path to result list

    return result


#########PRIM#########
def prims(graph):
    if not graph.is_connected(): return None  # if graph is not connected return None
    nodes_list = []
    edges_list = []
    edges_q = PriorityQueue()
    current = random.choice(list(graph.nodes_dict.keys()))  # randomly select a node
    nodes_list.append(current)  # add to list of nodes
    while len(nodes_list) < len(graph.nodes_dict):  # while all nodes have not been added to list
        edges_q.queue.clear()  # clear the queue
        for node in nodes_list:  # for each node in list
            for adj_node in graph.nodes_dict[node]:  # go through adjacent nodes
                weight = graph.edges_dict[(node, adj_node)]
                if adj_node not in nodes_list:  # if the adjacent node is not in the node list
                    edges_q.put((weight, node, adj_node))  # add associated edge to queue
        min_edge = edges_q.get()  # get the smallest weight edge from the queue
        edges_list.append(min_edge)  # add the edge to edge list
        nodes_list.append(min_edge[2])  # add the associated node to node list

    return edges_list  # return list of edges


#########BELLMAN FORD#########
def bellman_ford(graph, from_v, to_v_list=None):
    node_dict = {}  # create a node dictionary to return a distance, parent pair given a node value

    if to_v_list is None: to_v_list = node_dict.keys()  # if no node was input, find path to all nodes

    # make sure start node is valid
    if from_v not in graph.nodes_dict:
        print('Invalid start node of ' + str(from_v))
        return

    # make sure destination nodes are valid
    for node in to_v_list:
        if node not in graph.nodes_dict:
            print('Invalid end node of ' + str(node))
            return

    # set up algorithm start conditions
    for node in graph.nodes_dict.keys():  # for each node
        if node == from_v:  # if node is the start node
            node_dict[node] = (0, node)  # put into dictionary with 0 distance and itself as a parent
        else:
            node_dict[node] = (
                float('inf'), None)  # put all other nodes in dictionary with largest possible distance and no parent

    for i in range(len(graph.nodes_dict.keys()) - 1):  # loop through once for each the number of vertices - 1
        for (u, v), weight in graph.edges_dict.items():  # for each loop get each edge
            if node_dict[u][0] + weight < node_dict[v][0]:  # if shorter path found using that edge
                node_dict[v] = (node_dict[u][0] + weight, u)  # reset node's distance and parent
    result = []
    for (u, v), weight in graph.edges_dict.items():  # try to relax edges one more time
        if node_dict[u][0] + weight < node_dict[v][
            0]:  # if distance to a node can be shortened again a negative cycle exists
            result.append((node, -1, None))  # return result with none path and
            return result

    for node in to_v_list:  # go through all end nodes
        path = [node]
        total_dist = node_dict[node][0]  # set total distance to dist from start to goal node
        if total_dist == float('inf'):  # if path wasn't found
            result.append((node, total_dist, None))  # return result with None
        else:
            while path[0] != from_v:  # while node at 0 index is not start node
                path.insert(0, node_dict[path[0]][1])  # insert parent into 0 index of path
            result.append((node, total_dist, path))  # add path to result list

    return result
