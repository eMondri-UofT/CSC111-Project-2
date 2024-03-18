"""CSC111 Winter 2024 Project 2
    Title: "Music Reccomendations based on key factors"
    Author: Mark Lu, Ethan Mondri, _, _
"""
from __future__ import annotations
import csv
from typing import Any


class _Vertex:
    """
    Superclass for vertices
    """
    item: Any
    neighbours: set[_Vertex]

    def __init__(self, item: Any) -> None:
        """
        Initialize a new vertex with the given item, and no neighbours.
        """
        self.item = item
        self.neighbours = set()


class _ValueVertex(_Vertex):
    """
    Vertices for values
    """
    item: str
    value: float
    neighbours: set[_Vertex]

    def __init__(self, item: str, value: float) -> None:
        """
        Initialize a new vertex for a value, with no neighbours.

        Preconditions:
            - (value >= 0.0) and (value < 1.0)
        """
        self.value = value
        super().__init__(item)


class _SongVertex(_Vertex):
    """
    Vertices for songs
    """
    item: str
    neighbours: set[_Vertex]

    def __init__(self, item: str) -> None:
        """
        Initialize a new vertex for a song, with no neighbours.
        """
        super().__init__(item)


class Graph:
    """
    A graph used to represent a song value network.

    Instance Attributes:
        - _vertices:
            A collection of vertices in this object. Maps item to _Vertex object.
    """
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """
        Initialize an empty graph (no vertices or edges).
        """
        self._vertices = {}

    def add_vertex(self, item: Any, subclass: str = None, value: float = None) -> None:
        """
        Add a vertex with the given item to this graph, of a given subclass if one is given.

        Preconditions:
            - if subclass == 'value': value != None
        """
        if item not in self._vertices:
            if subclass == 'value':
                self._vertices[item] = _ValueVertex(item, value)
            elif subclass == 'song':
                self._vertices[item] = _SongVertex(item)
            else:
                self._vertices[item] = _Vertex(item)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """
        Add an edge between the two vertices with the given items in the graph.

        Raise ValueError if item1 or item2 do not appear as vertices in this graph

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """
        Return whether item1 and item2 are adjacent vertices.

        Return false if either item is not in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """
        Returns the items neighbouring the given item.

        Raise a ValueError if the given item is not in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError


def load_graph(information_file: str) -> Graph:
    """
    Return a graph containing the information in information_file.

    information_file format: (only needed items)
        - column 0:
            song ID
        - column 1:
            song name
        - column 11:
            song duration
        - column 13:
            song modality
        - column 16:
            song acousticness
        - column 17:
            song danceability
        - column 18:
            song energy
        - column 19:
            song instrumentalness
        - column 23:
            song valence
        - column 24:
            song tempo

    Preconditions:
        - information_file is the path to a CSV file with the dataset in the specified format.
    """
