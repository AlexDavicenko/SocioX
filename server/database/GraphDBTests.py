from GraphDB import Graph
TEST_DB_NAME = "graphdbtest.csv"


def run_tests():
    print("\t---RUNNING ALL TESTS---")
    for test in [add_node_test, add_edge_test, save_graph_test, load_graph_test, remove_node_test, remove_edge_test, get_user_suggestions_test]:

        print(f"Running: [{test.__name__}]")
        if test():
            print(f"[{test.__name__}]: Passed")
        else:
            print(f"[{test.__name__}]: Failed")

    print("\t---ALL TESTS RAN---")

def add_node_test():
    g = Graph()
    g.addNode("A")
    g.addNode("B")
    g.addNode("C")
    g.addNode("D")
    g.addNode("E")
    g.addNode("F")
    g.addNode("G")
    g.addNode("H")
    g.addNode("J")
    return True

def add_edge_test():
    g = Graph()
    g.addNode("A")
    g.addNode("B")
    g.addNode("C")
    g.addNode("D")
    g.addNode("E")
    g.addNode("F")
    g.addNode("G")
    g.addNode("H")
    g.addNode("J")

    g.addEdge("A", "B", 10)
    g.addEdge("B", "A", 20)
    g.addEdge("A", "C", 12.2)
    g.addEdge("C", "B", 54.3)
    g.addEdge("D", "E", 12.3)
    g.addEdge("H", "J", 5.5)
    g.addEdge("A", "J", 100)
    g.addEdge("H", "G", 100.3)
    return True


def create_mock_graph():
    g = Graph()
    g.addNode("A")
    g.addNode("B")
    g.addNode("C")
    g.addNode("D")
    g.addNode("E")
    g.addNode("F")
    g.addNode("G")
    g.addNode("H")
    g.addNode("I")
    g.addNode("J")


    g.addEdge("A", "B", 0.33)
    g.addEdge("B", "A", 0.21)
    g.addEdge("A", "C", 1)
    g.addEdge("C", "A", 0.5)
    g.addEdge("A", "H", 2)

    g.addEdge("C", "H", 1.23)
    g.addEdge("H", "C", 1.55)

    g.addEdge("C", "G", 3)
    g.addEdge("G", "C", 4)

    g.addEdge("G", "D", 1.9)
    g.addEdge("D", "G", 1.3)
    g.addEdge("G", "E", 1.7)
    g.addEdge("E", "G", 0.7)
    g.addEdge("D", "E", 0.5)
    g.addEdge("E", "D", 0.4)

    g.addEdge("G", "J", 1.17)
    g.addEdge("J", "G", 0.94)

    g.addEdge("F", "J", 0.45)
    g.addEdge("J", "F", 0.35)
    return g

def cmp_file_and_graph(data: str, g: Graph):
    #Creating an edge map Node -> (Node, Weight) 
    e_map = {}
    for e in g.getAllEdges():
        outgoing_edges = []
        for i in range(1, len(e), 2):
            outgoing_edges.append((e[i], e[i+1]))
        e_map[e[0]] = outgoing_edges
    
    graph_data = data.splitlines()
    nodes = graph_data[-1].split(", ")
    for i in range(len(nodes)):
        edge_data = graph_data[i].split(", ")

        if nodes[i] not in e_map:
            #Isolated node (No edges)
            if graph_data[i] == "":
                continue
            return False

        edges = e_map[nodes[i]]

        #Isolated node
        if not edges and edge_data == [""]:
            continue


        for j in range(0, len(edge_data), 2):
            
            if (edge_data[j], edge_data[j+1]) in edges:
                edges.remove((edge_data[j], edge_data[j+1]))
            else:
                return False
        if edges != []:
            return False
    return True


def save_graph_test():
    g = create_mock_graph()
    g.saveGraph(TEST_DB_NAME)

    with open(TEST_DB_NAME, "r") as f:
        data = f.read()
    
    return cmp_file_and_graph(data, g)



def load_graph_test():
    g = Graph()
    g.loadGraph(TEST_DB_NAME)
    
    with open(TEST_DB_NAME, "r") as f:
        data = f.read()

    return cmp_file_and_graph(data, g)


def remove_node_test():
    g = create_mock_graph()
    g.removeNode("A")
    if g.getAllNodes() != ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
        return False
    g.removeNode("D")
    if g.getAllNodes() != ['B', 'C', 'E', 'F', 'G', 'H', 'I', 'J']:
        return False
    
    g.removeNode("H")
    if g.getAllNodes() != ['B', 'C', 'E', 'F', 'G', 'I', 'J']:
        return False
    
    return True


def remove_edge_test():

    g = create_mock_graph()
    g.removeEdge("A", "B")
    g.removeEdge("A", "C")
    g.removeEdge("A", "H")
    g.removeNode("A")
    
    return True

def get_user_suggestions_test():

    g = create_mock_graph()
    


    #Test for node A
    friends = set()
    closest = []
    for _ in range(8):
        ans = g.closestNonFriendNode("A", friends)
        closest.append(ans)
        friends.add(ans)
    
    if closest != ['B', 'C', 'H', 'G', 'J', 'F', 'E', 'D']:
        return False

    
    #Test for node G
    friends = set()
    closest = []
    for _ in range(8):
        ans = g.closestNonFriendNode("G", friends)
        closest.append(ans)
        friends.add(ans)
    if closest != ['J', 'F', 'E', 'D', 'C', 'A', 'B', 'H']:
        return False
    

    #Test for node H
    friends = set()
    closest = []
    for _ in range(8):
        ans = g.closestNonFriendNode("H", friends)
        closest.append(ans)
        friends.add(ans)
    if closest != ['C', 'A', 'B', 'G', 'J', 'F', 'E', 'D']:
        return False

    return True

if __name__ == "__main__":
    run_tests()