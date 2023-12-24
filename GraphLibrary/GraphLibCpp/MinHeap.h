
#include <string>
#include <iostream>
using namespace std;


struct Node {
    string id;
};

struct Item {
    float priority;
    Node* value;
};



class MinHeap {

private:
    void swap(int i, int j);
    int parent(int i);
    int left(int i);
    int right(int i);
public:
    Item* heapArr;
    int size;
    int head;

    MinHeap(int heap_size);

    Item pop();

    void insert(Item item);

    void printHeap();

    bool isEmpty();
};


