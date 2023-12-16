#include <Windows.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "CSVParser.h"
#include "MinHeap.h"

using namespace std;
namespace py = pybind11;


class Graph {
public:
    int size;
    //Node names must be unique
    unordered_map<Node*, list<pair<Node*, int>>*> edgeMap;
    unordered_map<string, Node*> nodes;

    Graph() {
        size = 0;
    }

    void add_node(string nodeName) {
        if (nodes.count(nodeName)) {
            cout << "Node " << nodeName << "Already exists in the graph" << endl;
        }
        else {
            Node* node = new Node{ nodeName };
            nodes[nodeName] = node;
        }

    }

    void remove_node(string nodeId) {

        if (!nodes.count(nodeId)) {
            cout << "Attempted removal node " << nodeId << " does not exist in graph" << endl;
            return;
        }
        //remove node
        nodes.erase(nodeId);

        //remove edges to and from node
        for (const auto& p : edgeMap) {
            if (p.first->id == nodeId) {
                edgeMap.erase(p.first);
            }
            else {

                for (const auto& n : *p.second) {
                    if (n.first->id == nodeId) {
                        //O(n^3 time complexity (W rizz))
                        p.second->remove(n);
                    }
                }
            }
        }
    }
    void remove_edge(string nodeAId, string nodeBId) {
        //Check for existence
        if (!nodes.count(nodeAId) || !nodes.count(nodeBId)) {
            cout << "The nodes specified do not exist in the graph" << endl;
            return;
        }
        Node* nodeA = nodes[nodeAId];
        //Remove one directional edge
        if (edgeMap.count(nodeA)) {
            list<pair<Node*, int>>* edgeList = edgeMap[nodeA];
            for (auto& p : *edgeList) {
                if (p.first->id == nodeBId) {
                    edgeList->remove(p);
                }
            }
        }

    }


    void add_edge(string nodeAId, string nodeBId, int weight) {

        //Check for existence
        if (!nodes.count(nodeAId) || !nodes.count(nodeBId)) {
            cout << "Node does not exist in graph" << endl;
            return;
        }
        Node* nodeA = nodes[nodeAId];
        Node* nodeB = nodes[nodeBId];


        //If edge map already contains node A
        if (edgeMap.count(nodeA)) {

            list<pair<Node*, int>>* edgeList = edgeMap[nodeA];

            for (auto& p : *edgeList) {
                if (p.first->id == nodeB->id) {
                    edgeList->remove(p);
                }
            }

            edgeMap[nodeA]->push_back(make_pair(nodeB, weight));
        }
        else {
            list<pair<Node*, int>>* edgeList = new list<pair<Node*, int>>();

            edgeList->push_back(make_pair(nodeB, weight));

            edgeMap[nodeA] = edgeList;

        }
        size++;
    }

    //Dijkstra Algorithm to find the closest node
    string closest_non_friend_node(string startNodeId, unordered_set<string> friendsId) {

        //Find node in graph by name
        Node* node = nodes[startNodeId];

        //Create priority queue for nodes
        MinHeap priorityQueue(size + 1);
        priorityQueue.insert(Item{ 0, node });

        //Create a set for visted nodes
        unordered_set<Node*> visitedNodes;
        visitedNodes.insert(node);

        //Create distance hash map
        unordered_map<Node*, int> distances;
        for (auto& it : nodes) {
            distances[it.second] = INT32_MAX;
        }
        distances[node] = 0;

        while (!priorityQueue.is_empty()) {

            //Get next closest node
            Item top = priorityQueue.pop();

            //Unpackage Item from heap
            int cur_priority = top.priority;
            Node* cur_node = top.value;

            if (!friendsId.count(cur_node->id)) {
                //cout << cur_node->name ;
                for (auto& it : friendsId) {
                    //cout << it << endl;
                }

                return cur_node->id;
            }

            //Mark current node as visited
            visitedNodes.insert(cur_node);

            cout << "\nProcessing Node: " << cur_node->id << endl;


            //if edgeMap doesnt contain the node (i.e node has no outgoing edges)
            if (!edgeMap.count(cur_node)) {
                //skip while loop
                continue;
            }

            //Loop over every edge
            for (auto edge : *edgeMap[cur_node]) {

                //Unpackage Item 
                Node* new_node = edge.first;
                int weight = edge.second;

                //If new node hasnt been visited
                if (!visitedNodes.count(new_node)) {

                    //Add to the priority queue with higher priority
                    priorityQueue.insert(Item{ cur_priority + weight, new_node });
                }

                //Augment shortest distances
                if (distances[new_node] > cur_priority + weight) {
                    distances[new_node] = cur_priority + weight;
                }
            }
        }

        cout << "No node found" << endl;
        
        return "";
    }

    void saveGraph(string filename) {


        list<list<string>> graphData;
        list<string> nodeList;

        for (auto n = nodes.begin(); n != nodes.end(); n++) {
            Node* node = n->second;
            nodeList.push_back(node->id);

            list<string> edgeList;

            //If edge map contains node
            if (edgeMap.count(node)) {
                list<pair<Node*, int>>* edges = edgeMap[node];

                for (auto e = edges->begin(); e != edges->end(); e++) {
                    edgeList.push_back(e->first->id);
                    edgeList.push_back(to_string(e->second));
                }
            }
            if (edgeList.size() == 0) {
                edgeList.push_back("");
            }


            graphData.push_back(edgeList);

        }

        graphData.push_back(nodeList);
        exportCSV(graphData, filename);
    }
    void loadGraph(string filename) {

        list<list<string>> graphData = parseCSV(filename);

        list<string> nodeList = graphData.back();
        vector<Node*> nodeVec;


        //Read over nodes
        for (auto n = nodeList.begin(); n != nodeList.end(); n++) {
            Node* new_node = new Node{ *n };
            nodes[*n] = new_node;
            nodeVec.push_back(new_node);
        }
        size = nodeVec.size();

        //Read over edges
        int i = 0;
        for (auto l = graphData.begin(); l != prev(graphData.end()); l++) {


            list<pair<Node*, int>>* edgeList = new list<pair<Node*, int>>;
            for (auto n = (*l).begin(); n != (*l).end(); n++) {

                string node_name = *n;
                n++;


                //LATER MIGHT BE FLOAT
                int weight = stoi(*n);

                edgeList->push_back(make_pair(nodes[node_name], weight));
            }
            edgeMap[nodeVec[i]] = edgeList;
            i++;
        }
    }

    list<string> getAllNodes() {

        list<string> ns;
        for (auto& n : nodes) {
            ns.push_back(n.first);
        }
        return ns;
    }

};

PYBIND11_MODULE(GraphDB, m) {
    py::class_<Graph>(m, "Graph")
        .def(py::init<>())
        .def_readwrite("size", &Graph::size)
        .def("addNode", &Graph::add_node)
        .def("addEdge", &Graph::add_edge)
        .def("removeEdge", &Graph::remove_edge)
        .def("removeNode", &Graph::remove_node)
        .def("getAllNodes", &Graph::getAllNodes)
        .def("closest_non_friend_node", &Graph::closest_non_friend_node)
        .def("loadGraph", &Graph::loadGraph)
        .def("saveGraph", &Graph::saveGraph);
           

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}