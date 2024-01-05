
from GraphDB import Graph

from typing import TypeVar, List, Dict, Any
from types import TracebackType

class GraphDBConnection:
    DB_NAME: str

    def __init__(self, database_name: str) -> None:
        self.DB_NAME = database_name
        self.graph = Graph()
        self.graph.loadGraph(self.DB_NAME)
        
    def __enter__(self):
        return self 
    
    def __exit__(self, exc_type: type[BaseException], exc_value: BaseException, trackeback: TracebackType) -> None:
        self.graph.saveGraph(self.DB_NAME)

    def addUser(self, username: str):
        self.graph.addNode(username)

    def addEdge(self, username_1: str, username_2: str, weight: float):
        self.graph.addEdge(username_1, username_2, weight)

    def getUserSuggestion(self, username: str, friends: set[str]):
        return self.graph.closestNonFriendNode(username, friends)

    def reset(self):
        self.graph = Graph()
    