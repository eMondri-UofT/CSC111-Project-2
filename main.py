"""CSC111 Winter 2024 Project 2
    Title: "Music Reccomendations based on key factors"
    Author: Mark Lu, Ethan Mondri, _, _
"""
from __future__ import annotations
import csv
from typing import Any
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx


class _Vertex:
    """
    Superclass for vertices

    Instance Attributes:
    - item:
        An item of any type
    - neighbours:
        A set of other vertices
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
    neighbours: set[_SongVertex | _ValueVertex]

    def __init__(self, item: str, value: float) -> None:
        """
        Initialize a new vertex for a value, with no neighbours.
        """

        self.value = value
        super().__init__(item)

    def get_value(self) -> float:
        """
        Return the value of this ValueVertex.

        >>> vv = _ValueVertex('energy', 0.67)
        >>> vv.get_value()
        0.67
        """

        return self.value

    def get_song_neighbours(self) -> set[_SongVertex]:
        f"""
        Return a set of all _SongVertex neighbours

        >>> vv = _ValueVertex('energy', 0.67)
        >>> vv.neighbours = {_SongVertex("Can't Stop The Feeling"), _SongVertex("Don't Stop Me Now")}
        >>> vv.get_song_neighbours()
        {_SongVertex("Can't Stop The Feeling"), _SongVertex("Don't Stop Me Now")}
        """

        return {neighbour for neighbour in self.neighbours if isinstance(neighbour, _SongVertex)}

    def get_value_neighbours(self) -> set[_ValueVertex]:
        """
        Return a set of all _ValueVertex neighbours

        >>> vv = _ValueVertex('energy', 0.67)
        >>> vv2 = _ValueVertex('energy', 0.66)
        >>> vv.neighbours = {vv2}
        {vv2}
        >>> vv.neighbours = {_ValueVertex('energy', 0.66), _ValueVertex('energy', 0.68)}
        {_ValueVertex('energy', 0.66), _ValueVertex('energy', 0.68)}
        """

        return {neighbour for neighbour in self.neighbours if isinstance(neighbour, _ValueVertex)}


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

        >>> sv = _SongVertex("Don't Stop Me Now")
        >>> sv.neighbours = {_ValueVertex('energy', 0.66)}
        >>> sv.get_value_of_type('energy')
        0.66
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
            A dictionary mapping song names to song ids.
        - song_ids:
            A dictionary mapping song ids to song names.
    """
    _vertices: dict[Any, _ValueVertex | _SongVertex | _Vertex]
    song_names = dict[str, str]
    song_ids = dict[str, str]

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
                self._vertices[item] = _ValueVertex(item[0], value)
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
        if song_name not in self.song_ids:
            self.song_ids[song_name] = song_id

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

    def get_vertices(self) -> list:
        """
        Return every vertex in this graph
        """

        return list(self._vertices.values())

    def get_edges(self) -> set[tuple]:
        """
        Return every edge in this graph, as a set of tuples
        """
        edges = set()
        for v in self._vertices.values():
            for n in v.neighbours:
                edges.add((n.item, v.item))
        return edges

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

    def get_song_vertex_by_name(self, song_name: str) -> _SongVertex:
        """
        Returns a song vertex given the song's id
        """

        if song_name not in self.song_names:
            raise IndexError
        else:
            return self._vertices[self.song_names[song_name]]

    def get_song_by_name(self, song_name: str) -> str:
        """
        Returns a song's id given it's name
        """

        if song_name not in self.song_names:
            raise IndexError
        else:
            return self.song_names[song_name]

    def get_song_by_id(self, song_id: str) -> str:
        """
        Returns a song's name given it's id
        """

        if song_id not in self.song_ids:
            raise IndexError
        else:
            return self.song_ids[song_id]

    def get_value_vertex(self, type: str, value: float) -> _ValueVertex:
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
            average += self.get_similarity_by_type(song1, song2, neighbour_type)
            num_types += 1

        return average / num_types

    def recommend_songs(self, song: str, limit: int) -> list[str]:
        """
        Return a list of songs based on similarity scores to the given song.
        """
        # TODO write this function

        song_similarity_dict = {}
        # Nearest vertices
        for neighbour in self.get_song_vertex_by_name(song).neighbours:
            for neighbour_song in neighbour.get_song_neighbours():
                song_similarity_dict[neighbour_song.item] = self.average_similarity(
                    self.get_song_by_name(song), self.get_song_by_id(neighbour_song.item))
        sorted_one_away = sorted(song_similarity_dict, key=song_similarity_dict.get)
        sorted_one_away = sorted_one_away[:limit // 2]
        average_one_away = int(sorted_one_away[-1])
        for key in song_similarity_dict:
            if song_similarity_dict[key] > average_one_away:
                song_similarity_dict.pop(key)
        while len(song_similarity_dict) < limit:
            distance = 1
            for neighbour in self.get_song_vertex_by_name(song).neighbours:
                for distant_vertex in self.value_vertex_by_distance(neighbour, distance):
                    for neighbour_song in distant_vertex.get_song_neighbours():
                        neighbour_song_similarity = self.average_similarity(
                            self.get_song_by_name(song), self.get_song_by_id(neighbour_song.item))
                        if neighbour_song_similarity <= average_one_away:
                            song_similarity_dict[neighbour_song.item] = neighbour_song_similarity
            distance += 1
        return sorted(song_similarity_dict, key=song_similarity_dict.get)

    def value_vertex_by_distance(self, vertex: _ValueVertex, distance: int) -> Any:
        """
        Return the value vertexes [distance] away from the given vertex
        """

        if distance == 0:
            return {vertex}
        else:
            vertices = set()
            for neighbour in vertex.get_value_neighbours():
                vertices.union(self.value_vertex_by_distance(neighbour, distance - 1))

            return {v for v in vertices if v.value - distance == vertex.value}


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
            song energy THIS WAS ACTUALLY 17, TAKE THAT AS YOU WILL
        - column 19:
            song instrumentalness I REMOVED THIS COLUMN CHANGE THINGS...
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

    for i in range(1, 101):
        # Copy this line for every piece of information that's going to be used.
        graph.add_edge(('energy', (i - 1) / 100), ('energy', i / 100))

    with open(information_file) as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            graph.add_vertex(row[0], 'song')
            graph.add_song(row[1], row[0])
            # Copy this line for every piece of information that's going to be used.
            graph.add_edge(row[0], ('energy', round(float(row[17]), 2)))

    return graph


def load_visualization_graph(main_graph: Graph, songs: list[str], given_song: str) -> Graph:
    """
    Create a graph with all the songs in songs and all the value vertices in between
    """
    # TODO finish this

    graph = Graph()
    given_song_vertex = main_graph.get_song_vertex_by_name(given_song)

    value_edges = set()
    for song in songs:
        # Recommended song vertices
        graph.add_vertex(main_graph.get_song_by_id(song), 'song')
        # Edge value vertices
        for vertex in main_graph.get_song_vertex_by_name(main_graph.get_song_by_id(song)).neighbours:
            graph.add_vertex((vertex.item, vertex.value), 'value', vertex.value)
            graph.add_edge((vertex.item, vertex.value), main_graph.get_song_by_id(song))
            value_edges.add(graph.get_value_vertex(vertex.item, vertex.value))

    # Other value vertices + edges between value vertices
    for edge in value_edges:
        edge_value = edge.value
        song_value = given_song_vertex.get_value_of_type(edge.item)
        difference = int(abs(song_value - edge_value) * 100)
        for i in range(1, difference + 1):
            if song_value > edge_value:
                graph.add_vertex((edge.item, edge_value + i), 'value', edge_value)
                graph.add_edge(graph.get_value_vertex(edge.item, edge_value + i),
                               graph.get_value_vertex(edge.item, edge_value + i - 1))
            elif song_value < edge_value:
                graph.add_vertex((edge.item, edge_value - i), 'value', edge_value)
                graph.add_edge(graph.get_value_vertex(edge.item, edge_value - i),
                               graph.get_value_vertex(edge.item, edge_value - i + 1))
            else:
                pass

    # Song vertex + edges
    graph.add_vertex(given_song, 'song')
    for value_vertex in {v for v in given_song_vertex.neighbours}:
        graph.add_edge(given_song, graph.get_value_vertex(value_vertex.item, value_vertex.value))

    return graph


# visualizing the graph
def display_graph(g: Graph = None):
    """
    Display the graph in the Tkinter window.
    """
    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots()

    if g is None:
        vis = nx.Graph()
        vis.add_node("No data available")
    else:
        vis = nx.Graph()
        for n in g.get_vertices():
            vis.add_node(n)
        for e in g.get_edges():
            vis.add_edge(*e)

    nx.draw(vis, ax=ax, with_labels=True, node_size=700, node_color='skyblue')

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def submission_of_user():
    """
    Handle the submit action: generate graph data based on user input and display the graph.
    """
    song_name = song_entry.get()
    num_recommendations = int(limit_var.get())
    graph_data = graph.recommend_songs(song_name, num_recommendations)
    recommendation_graph = load_visualization_graph(graph, graph_data, song_name)
    display_graph(recommendation_graph)


if __name__ == '__main__':
    # create graph
    graph = load_graph("tracks_features_first_2000.csv")
    # create GUI
    root = tk.Tk()
    root.title("Music Recommendations")

    graph_frame = tk.Frame(root)
    graph_frame.pack(fill=tk.BOTH, expand=True)
    display_graph()

    input_frame = tk.Frame(root)
    input_frame.pack(fill=tk.X)

    tk.Label(input_frame, text="Enter Song Name:").pack(side=tk.LEFT)
    song_entry = tk.Entry(input_frame)
    song_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(input_frame, text="Number of Recommendations:").pack(side=tk.LEFT)
    limit_var = tk.StringVar(root)
    limit_var.set("5")  # default value
    limit_dropdown = ttk.Combobox(input_frame, textvariable=limit_var, values=["5", "10", "20"])
    limit_dropdown.pack(side=tk.LEFT, padx=5)

    submit_button = tk.Button(input_frame, text="Submit", command=submission_of_user)
    submit_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()
