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
    unordered_map<Node*, list<pair<Node*, float>>*> edgeMap;
    unordered_map<string, Node*> nodes;

    Graph() {
        size = 0;
    }

    void addNode(string nodeName) {
        if (nodes.count(nodeName)) {
            cout << "Node " << nodeName << "Already exists in the graph" << endl;
        }
        else {
            Node* node = new Node{ nodeName };
            nodes[nodeName] = node;
        }

    }

    void removeNode(string nodeId) {

        if (!nodes.count(nodeId)) {
            cout << "Attempted removal node " << nodeId << " does not exist in graph" << endl;
            return;
        }
        //remove node
        nodes.erase(nodeId);

        //remove edges to and from node
        for (const auto& p : edgeMap) {
            //Removing edges from node
            if (p.first->id == nodeId) {
                edgeMap.erase(p.first);
            }
            else {
                //LAMBDA FUNCTION ??????? (W RIZZ)
                p.second->remove_if([nodeId](pair<Node*, float> p) {
                    return p.first->id == nodeId;
                });

            }
        }
    }
    void removeEdge(string nodeAId, string nodeBId) {
        //Check for existence
        if (!nodes.count(nodeAId) || !nodes.count(nodeBId)) {
            cout << "The nodes specified do not exist in the graph" << endl;
            return;
        }
        Node* nodeA = nodes[nodeAId];
        //Remove one directional edge
        if (edgeMap.count(nodeA)) {
            list<pair<Node*, float>>* edgeList = edgeMap[nodeA];
            
            edgeList->remove_if([nodeBId](pair<Node*, float> p) {
                return p.first->id == nodeBId;
            });
        }

    }

    void addEdge(string nodeAId, string nodeBId, float weight) {

        //Check for existence
        if (!nodes.count(nodeAId) || !nodes.count(nodeBId)) {
            cout << "Node does not exist in graph" << endl;
            return;
        }
        Node* nodeA = nodes[nodeAId];
        Node* nodeB = nodes[nodeBId];


        //If edge map already contains node A
        if (edgeMap.count(nodeA)) {

            list < pair < Node*, float >> *edgeList = edgeMap[nodeA];

            for (auto& p : *edgeList) {
                if (p.first->id == nodeB->id) {
                    edgeList->remove(p);
                }
            }

            edgeMap[nodeA]->push_back(make_pair(nodeB, weight));
        }
        else {
            list<pair<Node*, float>>* edgeList = new list<pair<Node*, float>>();

            edgeList->push_back(make_pair(nodeB, weight));

            edgeMap[nodeA] = edgeList;

        }
        size++;
    }

    //Dijkstra Algorithm to find the closest node
    string closestNonFriendNode(string startNodeId, unordered_set<string> friendsIdSet) {

        friendsIdSet.insert(startNodeId);

        //Find node in graph by name
        Node* node = nodes[startNodeId];

        //Create priority queue for nodes
        MinHeap priorityQueue(size + 1);
        priorityQueue.insert(Item{ 0, node });

        //Create a set for visted nodes
        unordered_set<Node*> visitedNodes;
        visitedNodes.insert(node);

        //Create distance hash map
        unordered_map<Node*, float> distances;
        for (auto& it : nodes) {
            distances[it.second] = FLT_MAX;
        }
        distances[node] = 0;

        while (!priorityQueue.isEmpty()) {

            //Get next closest node
            Item top = priorityQueue.pop();

            //Unpackage Item from heap
            int curPriority = top.priority;
            Node* curNode = top.value;

            if (!friendsIdSet.count(curNode->id)) {
                return curNode->id;
            }

            //Mark current node as visited
            visitedNodes.insert(curNode);

            //If edgeMap doesnt contain the node (i.e node has no outgoing edges)
            if (!edgeMap.count(curNode)) {
                //skip while loop
                continue;
            }

            //Loop over every edge
            for (auto edge : *edgeMap[curNode]) {

                //Unpackage Item 
                Node* newNode = edge.first;
                float weight = edge.second;

                //If new node hasnt been visited
                if (!visitedNodes.count(newNode)) {

                    //Add to the priority queue with higher priority
                    priorityQueue.insert(Item{ curPriority + weight, newNode });
                }

                //Augment shortest distances
                if (distances[newNode] > curPriority + weight) {
                    distances[newNode] = curPriority + weight;
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
                list<pair<Node*, float>>* edges = edgeMap[node];

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
       
        //Empty file
        if (graphData.size() == 0) {
            return;
        }
        list<string> nodeList = graphData.back();
        vector<Node*> nodeVec;


        //Read over nodes
        for (auto n = nodeList.begin(); n != nodeList.end(); n++) {
            Node* newNode = new Node{ *n };
            nodes[*n] = newNode;
            nodeVec.push_back(newNode);
        }
        size = nodeVec.size();

        //Read over edges
        int i = 0;
        for (auto l = graphData.begin(); l != prev(graphData.end()); l++) {


            list<pair<Node*, float>>* edgeList = new list<pair<Node*, float>>;
            for (auto n = (*l).begin(); n != (*l).end(); n++) {

                string nodeName = *n;
                n++;

                float weight = stof(*n);

                edgeList->push_back(make_pair(nodes[nodeName], weight));
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

    list<list<string>> getAllEdges() {

        list<list<string>> edgesList2D;
        for (const auto& p : edgeMap) {
            list<string> edgesList;

            Node* n = p.first;
            list<pair<Node*, float>>* edges = p.second;

            edgesList.push_back(n->id);

            for (const auto& e : *edges) {
                edgesList.push_back(e.first->id);
                edgesList.push_back(to_string(e.second));
            }
            edgesList2D.push_back(edgesList);
        }
        return edgesList2D;
    }

};

PYBIND11_MODULE(GraphDB, m) {
    py::class_<Graph>(m, "Graph")
        .def(py::init<>())
        .def_readwrite("size", &Graph::size)
        .def("addNode", &Graph::addNode)
        .def("addEdge", &Graph::addEdge)
        .def("removeEdge", &Graph::removeEdge)
        .def("removeNode", &Graph::removeNode)
        .def("getAllNodes", &Graph::getAllNodes)
        .def("getAllEdges", &Graph::getAllEdges)
        .def("closestNonFriendNode", &Graph::closestNonFriendNode)
        .def("loadGraph", &Graph::loadGraph)
        .def("saveGraph", &Graph::saveGraph);
           

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}