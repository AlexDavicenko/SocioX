import sys
from typing import List

class Node:
    def __init__(self, value, is_word_end = False) -> None:
        self.value = value
        self.is_word_end = is_word_end
        self.children = {} #str: (Node, weight)

    def get_node_from_letter(self, letter: str):

        return self.children.get(letter, None)

    def add_node(self, letter, weight, is_word_end = False):
        
        node = Node(letter, is_word_end)
        self.children[letter] = (node, weight)
        return node


class PrefixTree:
    def __init__(self) -> None:
        self.root = Node(None)

    
    def add_word(self, word: str, rank: int):
        
        cur_node = self.root

        i = 0
        while i < len(word):
            
            node_data = cur_node.get_node_from_letter(word[i])
            if node_data: # if next node exists
                next_node, w = node_data
                if cur_node.children[word[i]][1] < w:  #Augmenting weight
                    cur_node.children[word[i]] = (next_node, w)

                cur_node = next_node
                i += 1
                continue

            cur_node.add_node(word[i], rank)
            if i == len(word)-1:
                cur_node = cur_node.add_node(word[i], rank, is_word_end = True)
            else:
                cur_node = cur_node.add_node(word[i], rank)
            i += 1
    
    def get_new_root(self, start_str) -> Node:
        cur_node = self.root

        i = 0 
        while i < len(start_str):
            node = cur_node.get_node_from_letter(start_str[i])
            if node:
                cur_node, _ = node
                i += 1
                continue
            return
        return cur_node

    def get_all_words(self, start_str = "") -> list[str]:

        cur_node = self.get_new_root(start_str)
        if not cur_node:
            return []

        
        # DFS
        words = []
        stack = [(cur_node, '', 0)]        

        while len(stack) > 0: 
            
            cur_node, cur_word, cur_w = stack.pop()
            
            if cur_node.is_word_end:
                if cur_w == 0:
                    words.append((start_str + cur_word, sys.maxsize))
                else:
                    words.append((start_str + cur_word, cur_w))

            for node, w in cur_node.children.values():
                stack.append((node, cur_word+node.value, w))

        return words
    
    def get_suggestion(self, start_str = "") -> str:
        
        
        words = self.get_all_words(start_str)
        words.sort(key = lambda x: x[1])
        return words[-3:]
        

class WordSuggestionAPI: 
    def __init__(self) -> None:
        with open('suggestions/filtered10k.txt', 'r') as f:

            self.words = f.read().splitlines()
            
            self.tree = PrefixTree()
            for i, word in enumerate(self.words):
                self.tree.add_word(word, len(self.words) - i)
            
    def get_suggestion(self, prefix: str) -> List[str]:
        return self.tree.get_suggestion(prefix)