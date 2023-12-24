
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

    def reset(self):
        self.graph = Graph()
        