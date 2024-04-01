"""CSC111 Winter 2024 Project 2
    File containing Vertex class and subclasses, as well as Graph Class
"""
from __future__ import annotations
from typing import Any
import python_ta


class Vertex:
    """
    Superclass for vertices

    Instance Attributes:
    - item:
        An item of any type
    - neighbours:
        A set of other vertices
    """
    item: Any
    neighbours: set[Vertex]

    def __init__(self, item: Any) -> None:
        """
        Initialize a new vertex with the given item, and no neighbours.
        """
        self.item = item
        self.neighbours = set()


class ValueVertex(Vertex):
    """
    Vertices for values

    Instance Attributes:
    - item:
        The type of value (energy, danceability, valence, etc.)
    - value:
        The value itself (0.68, 0.34, etc.)
    - neighbours:
        A set of other vertices this one is connected to, being either songs or other values of the same type.
    """

    item: str
    value: float
    neighbours: set[SongVertex | ValueVertex]

    def __init__(self, item: str, value: float) -> None:
        """
        Initialize a new vertex for a value, with no neighbours.
        """

        self.value = value
        super().__init__(item)

    def get_value(self) -> float:
        """
        Return the value of this ValueVertex.

        >>> vv = ValueVertex('energy', 0.67)
        >>> vv.get_value()
        0.67
        """

        return self.value

    def get_song_neighbours(self) -> set[SongVertex]:
        """
        Return a set of all _SongVertex neighbours

        >>> vv = ValueVertex('energy', 0.67)
        >>> vv.neighbours = {SongVertex("Can't Stop The Feeling"), SongVertex("Don't Stop Me Now")}
        >>> all({isinstance(neighbour, SongVertex) for neighbour in vv.get_song_neighbours()})
        True
        """

        return {neighbour for neighbour in self.neighbours if isinstance(neighbour, SongVertex)}

    def get_value_neighbours(self) -> set[ValueVertex]:
        """
        Return a set of all _ValueVertex neighbours

        >>> vv = ValueVertex('energy', 0.67)
        >>> vv.neighbours = {ValueVertex('energy', 0.66), ValueVertex('energy', 0.68)}
        >>> all({isinstance(neighbour, ValueVertex) for neighbour in vv.get_value_neighbours()})
        True
        """

        return {neighbour for neighbour in self.neighbours if isinstance(neighbour, ValueVertex)}


class SongVertex(Vertex):
    """
    Vertices for songs
    """

    item: str
    neighbours: set[ValueVertex]

    def __init__(self, item: str) -> None:
        """
        Initialize a new vertex for a song, with no neighbours.
        """
        super().__init__(item)

    def get_value_of_type(self, vtype: str) -> float:
        """
        Return the value of a certain type a song is connected to.

        >>> sv = SongVertex("Don't Stop Me Now")
        >>> sv.neighbours = {ValueVertex('energy', 0.66), ValueVertex('valence', 0.43)}
        >>> sv.get_value_of_type('energy')
        0.66
        """

        if vtype not in {neighbour.item for neighbour in self.neighbours}:
            raise IndexError
        for vertex in self.neighbours:
            if vertex.item == vtype:
                return vertex.get_value()
        return -1.0


class Graph:
    """
    A graph used to represent a song value network.

    Instance Attributes:
        - _vertices:
            A collection of vertices in this object. Maps item to _Vertex object.
        - song_names:
            A dictionary mapping song names to song ids.
        - song_ids:
            A dictionary mapping song ids to song names.
    """
    _vertices: dict[Any, ValueVertex | SongVertex | Vertex]
    song_names: dict[str, str]
    song_ids: dict[str, str]

    def __init__(self) -> None:
        """
        Initialize an empty graph (no vertices or edges).
        """
        self._vertices = {}
        self.song_names = {}
        self.song_ids = {}

    def add_vertex(self, item: Any, subclass: str = None, value: float = None) -> None:
        """
        Add a vertex with the given item to this graph, of a given subclass if one is given.

        Preconditions:
            - if subclass == 'value': value != None
        """
        if item not in self._vertices:
            if subclass == 'value':
                self._vertices[item] = ValueVertex(item[0], value)
            elif subclass == 'song':
                self._vertices[item] = SongVertex(item)
            else:
                self._vertices[item] = Vertex(item)

    def add_song(self, song_id: str, song_name: str) -> None:
        """
        Add to the song_names dictionary a mapping between the song_id and the song_name in both
        song_names (key = song_id) and song_ids (key = song_name)
        """
        if song_id not in self.song_names:
            self.song_names[song_id] = song_name
        if song_name not in self.song_ids:
            self.song_ids[song_name] = song_id

    def does_song_name_exist(self, song_name: str) -> bool:
        """
        Returns whether song_name has a matching id in this graph
        """

        return song_name in self.song_names

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

    def connect_value_edges(self, item1: tuple, item2: tuple) -> None:
        """
        Add edges between item1 and item2, incrementing by 0.01 per edge value.

        Raise ValueError if item1 or item2 are not vertices in this graph.

        Preconditions:
            - isinstance(self._vertices[item1], _ValueVertex)
            - isinstance(self._vertices[item2], _ValueVertex)
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            if round(v1.value - v2.value, 2) != 0:
                diff = round(abs(v1.value - v2.value) - 0.01, 2)
            else:
                return None

            # lower value + difference = 1 less than upper value. Works for separated by 1, since while loop.
            if v1.value > v2.value:
                while diff > 0.00:
                    self.add_vertex((item1[0], round(v2.value + diff, 2)),
                                    'value', round(v2.value + diff, 2))
                    self.add_edge((item1[0], round(v2.value + diff, 2)),
                                  (item1[0], round(v2.value + diff + 0.01, 2)))
                    diff = round(diff - 0.01, 2)
                self.add_edge((item1[0], v2.value), (item1[0], round(v2.value + 0.01, 2)))
            else:  # v2.value > v1.value
                while diff > 0.00:
                    self.add_vertex((item1[0], round(v1.value + diff, 2)),
                                    'value', round(v1.value + diff, 2))
                    self.add_edge((item1[0], round(v1.value + diff, 2)),
                                  (item1[0], round(v1.value + diff + 0.01, 2)))
                    diff = round(diff - 0.01, 2)
                self.add_edge((item1[0], v1.value), (item1[0], round(v1.value + 0.01, 2)))
        else:
            raise IndexError

        return None

    def get_vertices(self) -> list:
        """
        Return every vertex in this graph in a list
        """

        return list(self._vertices.values())

    def get_edges(self) -> set[tuple]:
        """
        Return every edge in this graph as a set of tuples (first vertex, second vertex)
        """
        edges = set()
        for v in self._vertices.values():
            for n in v.neighbours:
                edges.add((n, v))
        return edges

    def get_song_vertex_by_name(self, song_name: str) -> SongVertex:
        """
        Returns a song vertex given the song's name

        >>> g = Graph()
        >>> g.add_vertex('1010001', 'song')
        >>> g.add_song('1010001', 'Call Me Maybe')
        >>> song_vertex = g.get_song_vertex_by_name('Call Me Maybe')
        >>> song_vertex.item
        '1010001'
        """

        if song_name not in self.song_names:
            raise IndexError
        else:
            return self._vertices[self.song_names[song_name]]

    def get_song_by_name(self, song_name: str) -> str:
        """
        Returns a song's id given its name

        >>> g = Graph()
        >>> g.add_vertex('1010001', 'song')
        >>> g.add_song('1010001', 'Call Me Maybe')
        >>> g.get_song_by_name('Call Me Maybe')
        '1010001'
        """

        if song_name not in self.song_names:
            raise IndexError
        else:
            return self.song_names[song_name]

    def get_song_by_id(self, song_id: str) -> str:
        """
        Returns a song's name given its id

        >>> g = Graph()
        >>> g.add_vertex('1010001', 'song')
        >>> g.add_song('1010001', 'Call Me Maybe')
        >>> g.get_song_by_id('1010001')
        'Call Me Maybe'
        """

        if song_id not in self.song_ids:
            raise IndexError
        else:
            return self.song_ids[song_id]

    def get_value_vertex(self, vtype: str, value: float) -> ValueVertex:
        """
        Returns the value vertex in _vertices of the correct type (energy, tempo) with the correct value.

        >>> g = Graph()
        >>> g.add_vertex(('energy', 0.66), 'value', 0.66)
        >>> g.add_vertex(('energy', 0.67), 'value', 0.67)
        >>> value_vertex = g.get_value_vertex('energy', 0.66)
        >>> value_vertex.item
        'energy'
        >>> value_vertex.value
        0.66
        """

        if (vtype, value) in self._vertices:
            return self._vertices[(vtype, value)]
        else:
            raise ValueError

    def get_similarity_by_type(self, song1: str, song2: str, vtype: str) -> float:
        """
        Returns a similarity score between two songs, using the depth of value vertices.

        >>> g = Graph()
        >>> g.add_vertex('1010001', 'song')
        >>> g.add_vertex(('energy', 0.60), 'value', 0.60)
        >>> g.add_edge('1010001', ('energy', 0.60))
        >>> g.add_vertex(('energy', 0.61), 'value', 0.61)
        >>> g.add_edge(('energy', 0.60), ('energy', 0.61))
        >>> g.add_vertex(('energy', 0.62), 'value', 0.62)
        >>> g.add_edge(('energy', 0.61), ('energy', 0.62))
        >>> g.add_vertex(('energy', 0.63), 'value', 0.63)
        >>> g.add_edge(('energy', 0.62), ('energy', 0.63))
        >>> g.add_vertex(('energy', 0.64), 'value', 0.64)
        >>> g.add_edge(('energy', 0.63), ('energy', 0.64))
        >>> g.add_vertex('1110001', 'song')
        >>> g.add_edge('1110001', ('energy', 0.64))
        >>> g.get_similarity_by_type('1010001', '1110001', 'energy')
        0.06
        """

        if song1 not in self._vertices or song2 not in self._vertices:
            raise ValueError

        value1 = self._vertices[song1].get_value_of_type(vtype)
        value2 = self._vertices[song2].get_value_of_type(vtype)
        # return depth + the two edges from each song to the values.
        return round(abs(value2 - value1) + 0.02, 2)

    def average_similarity(self, song1: str, song2: str) -> float:
        """
        Returns the average similarity score across typings for the two inputted songs.

        >>> g = Graph()
        >>> # energy and song vertices
        >>> g.add_vertex('1010001', 'song')
        >>> g.add_vertex(('energy', 0.60), 'value', 0.60)
        >>> g.add_edge('1010001', ('energy', 0.60))
        >>> g.add_vertex(('energy', 0.61), 'value', 0.61)
        >>> g.add_edge(('energy', 0.60), ('energy', 0.61))
        >>> g.add_vertex(('energy', 0.62), 'value', 0.62)
        >>> g.add_edge(('energy', 0.61), ('energy', 0.62))
        >>> g.add_vertex(('energy', 0.63), 'value', 0.63)
        >>> g.add_edge(('energy', 0.62), ('energy', 0.63))
        >>> g.add_vertex(('energy', 0.64), 'value', 0.64)
        >>> g.add_edge(('energy', 0.63), ('energy', 0.64))
        >>> g.add_vertex('1110001', 'song')
        >>> g.add_edge('1110001', ('energy', 0.64))
        >>> # valence vertices
        >>> g.add_vertex(('valence', 0.30), 'value', 0.30)
        >>> g.add_edge('1010001', ('valence', 0.30))
        >>> g.add_vertex(('valence', 0.31), 'value', 0.31)
        >>> g.add_edge(('valence', 0.30), ('valence', 0.31))
        >>> g.add_vertex(('valence', 0.32), 'value', 0.32)
        >>> g.add_edge(('valence', 0.31), ('valence', 0.32))
        >>> g.add_edge('1110001', ('valence', 0.32))
        >>> # average of 0.04 and 0.06
        >>> g.average_similarity('1010001', '1110001')
        0.05
        """

        average = 0
        num_types = 0
        for neighbour in self._vertices[song1].neighbours:
            neighbour_type = neighbour.item
            average += self.get_similarity_by_type(song1, song2, neighbour_type)
            num_types += 1

        return round(average / num_types, 2)

    def recommend_songs(self, song: str, limit: int) -> list[str]:
        """
        Return a list of songs based on similarity scores to the given song.
        """

        song_similarity_dict = {}
        for vertex in self.get_vertices():
            if isinstance(vertex, SongVertex):
                song_similarity_dict[vertex.item] = self.average_similarity(
                    self.get_song_by_name(song), vertex.item)
        sorted_similarity = sorted(song_similarity_dict, key=song_similarity_dict.get)
        return sorted_similarity[:limit + 1]

    def value_vertex_by_distance(self, vertex: ValueVertex, distance: int) -> Any:
        """
        Return the value vertexes [distance] away from the given vertex

        >>> g = Graph()
        >>> g.add_vertex(('energy', 0.60), 'value', 0.60)
        >>> g.add_vertex(('energy', 0.61), 'value', 0.61)
        >>> g.add_edge(('energy', 0.60), ('energy', 0.61))
        >>> g.add_vertex(('energy', 0.62), 'value', 0.62)
        >>> g.add_edge(('energy', 0.61), ('energy', 0.62))
        >>> g.add_vertex(('energy', 0.63), 'value', 0.63)
        >>> g.add_edge(('energy', 0.62), ('energy', 0.63))
        >>> g.add_vertex(('energy', 0.64), 'value', 0.64)
        >>> g.add_edge(('energy', 0.63), ('energy', 0.64))
        >>> g.add_vertex(('energy', 0.65), 'value', 0.65)
        >>> g.add_edge(('energy', 0.64), ('energy', 0.65))
        >>> two_away = g.value_vertex_by_distance(g.get_value_vertex('energy', 0.63), 2)
        >>> {v.value for v in two_away} == {0.65, 0.61}
        True
        """

        if distance == 0:
            return [vertex]
        else:
            # It's a list for the sake of list.extend, better for this than set.union
            vertices = []
            for neighbour in vertex.get_value_neighbours():
                vertices.extend(self.value_vertex_by_distance(neighbour, distance - 1))

            return {v for v in vertices if round(abs(v.value - vertex.value), 2) == distance / 100}


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['annotations', 'Any'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
