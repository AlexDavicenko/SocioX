

#include "MinHeap.h"


void MinHeap::swap(int i, int j) {
    Item temp = heapArr[i];
    heapArr[i] = heapArr[j];
    heapArr[j] = temp;
}

int MinHeap::parent(int i) {
    return i / 2;
}


int MinHeap::left(int i) {
    return 2 * i;
}
int MinHeap::right(int i) {
    return (2 * i) + 1;
}

MinHeap::MinHeap(int heap_size){
    heapArr = new Item[heap_size];
    for (int i = 0; i < heap_size; i++) {
        heapArr[i].priority = 0;
        heapArr[i].value = 0;
    }
    head = 1;
    size = heap_size;
}

Item MinHeap::pop() {
    //Save top item
    Item out = this->heapArr[1];

    //Swap root with head and remove head
    head--;
    swap(1, head);
    heapArr[head].priority = 0;

    int cur = 1;
    float value = heapArr[1].priority;
    while (left(cur) < head && right(cur) < head)
    {
        float l = heapArr[left(cur)].priority;
        float r = heapArr[right(cur)].priority;
        if (l < value || r < value) {
            if (l < value && r < value) {
                if (l < r) {
                    swap(cur, left(cur));
                    cur = left(cur);
                }
                else {
                    swap(cur, right(cur));
                    cur = right(cur);
                }
            }
            else if (l < value) {
                swap(cur, left(cur));
                cur = left(cur);
            }
            else if (r < value) {
                swap(cur, right(cur));
                cur = right(cur);
            }
        }
        else {
            break;
        }
    }

    //Fix for a special case with a 2 sized heap where the loop above does not run :/ 
    //PS: This is why you test your code Alex
    if (head == 3) {
        if (heapArr[1].priority > heapArr[2].priority) {
            swap(1, 2);
        }
    }

    return out;

}


void MinHeap::insert(Item item) {
    this->heapArr[head] = item;
    int cur = head;
    head++;

    if (cur == 1) {
        return;
    }

    while (cur != 1) {

        if (heapArr[cur].priority < heapArr[parent(cur)].priority) {
            swap(cur, parent(cur));
        }
        else {
            break;
        }
        cur = parent(cur);
    }
}
void MinHeap::printHeap() {
    for (int i = 1; i < size; i++) {
        if (heapArr[i].value == nullptr) {
            cout << "(" << heapArr[i].priority << "," << ")" << ", ";
        }
        else {
            cout << "(" << heapArr[i].priority << "," << heapArr[i].value->id << ")" << ", ";
        }
    }
    cout << endl;
}

bool MinHeap::isEmpty() {
    return this->head == 1;
}