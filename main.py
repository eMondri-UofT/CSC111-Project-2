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
    neighbours: set[_SongVertex | _ValueVertex]

    def __init__(self, item: str, value: float) -> None:
        """
        Initialize a new vertex for a value, with no neighbours.

        Preconditions:
            - (value >= 0.0) and (value < 1.0)
        """
        self.value = value
        super().__init__(item)

    def get_value(self) -> float:
        """
        Return the value of this ValueVertex.
        """

        return self.value


class _SongVertex(_Vertex):
    """
    Vertices for songs
    """
    item: str
    neighbours: set[_ValueVertex]

    def __init__(self, item: str) -> None:
        """
        Initialize a new vertex for a song, with no neighbours.
        """
        super().__init__(item)

    def get_value_of_type(self, type: str) -> float:
        """
        Return the value of a certain type a song is connected to.
        """
        # TODO test

        for vertex in self.neighbours:
            if vertex.item == type:
                return vertex.get_value()


class Graph:
    """
    A graph used to represent a song value network.

    Instance Attributes:
        - _vertices:
            A collection of vertices in this object. Maps item to _Vertex object.
        - song_names:
            A dictionary mapping song ids to song names.
    """
    _vertices: dict[Any, _ValueVertex | _SongVertex | _Vertex]
    song_names = dict[str, str]

    def __init__(self) -> None:
        """
        Initialize an empty graph (no vertices or edges).
        """
        self._vertices = {}
        self.song_names = {}

    def add_vertex(self, item: Any, subclass: str = None, value: float = None) -> None:
        """
        Add a vertex with the given item to this graph, of a given subclass if one is given.

        Preconditions:
            - if subclass == 'value': value != None
        """
        if item not in self._vertices and (item, value) not in self._vertices:
            if subclass == 'value':
                self._vertices[(item, value)] = _ValueVertex(item, value)
            elif subclass == 'song':
                self._vertices[item] = _SongVertex(item)
            else:
                self._vertices[item] = _Vertex(item)

    def add_song(self, song_id: str, song_name: str) -> None:
        """
        Add to the song_names dictionary a mapping between the song_id and the song_name
        """
        if song_id not in self.song_names:
            self.song_names[song_id] = song_name

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

    def get_value_vertex(self, type: str, value: float) -> _Vertex:
        """
        Returns the value vertex in _vertices of the correct type (energy, tempo) with the correct value.
        """

        if (type, value) in self._vertices:
            return self._vertices[(type, value)]
        else:
            raise ValueError

    def get_similarity_by_type(self, song1: str, song2: str, type: str) -> float:
        """
        Returns a similarity score between two songs, using the depth of value vertices.
        """
        # TODO test

        if song1 not in self._vertices or song2 not in self._vertices:
            raise ValueError

        value1 = self._vertices[song1].get_value_of_type(type)
        value2 = self._vertices[song2].get_value_of_type(type)
        # return depth + the two edges from each song to the values.
        return abs(value2 - value1) + 2

    def average_similarity(self, song1: str, song2: str) -> float:
        """
        Returns the average similarity score across typings for the two inputted songs.
        """
        # TODO test

        average = 0
        num_types = 0
        for neighbour in self._vertices[song1].neighbours:
            neighbour_type = neighbour.item
            average += self._vertices[song1].get_value_of_type(neighbour_type)
            num_types += 1

        return average / num_types

    def recommend_songs(self, song: str, limit: int) -> list[str]:
        """
        Return a list of songs based on similarity scores to the given song.
        TODO visualize too
        """
        # TODO write this function

        chosen_songs = set()


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
    # TODO test if any of this works, since I wrote it at like 1 AM and didn't test anything
    # ^ that includes the helper functions, even add_vertex and such

    graph = Graph()

    for i in range(0, 101):
        # Copy this line for every piece of information that's going to be used.
        graph.add_vertex(('energy', i / 100), 'value', i / 100)

    with open(information_file) as file:
        reader = csv.reader(file)
        for row in reader:
            graph.add_vertex(row[0], 'song')
            graph.add_song(row[0], row[1])
            # Copy this line for every piece of information that's going to be used.
            graph.add_edge(row[0], ('energy', row[18]))

    return graph
