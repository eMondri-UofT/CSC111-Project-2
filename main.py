"""CSC111 Winter 2024 Project 2
    Title: "Music Reccomendations based on key factors"
    Author: Mark Lu, Ethan Mondri, _, _
"""
from __future__ import annotations
import csv
from typing import Any
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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
        """
        Return a set of all _SongVertex neighbours

        >>> vv = _ValueVertex('energy', 0.67)
        >>> vv.neighbours = {_SongVertex("Can't Stop The Feeling"), _SongVertex("Don't Stop Me Now")}
        >>> all({isinstance(neighbour, _SongVertex) for neighbour in vv.get_song_neighbours()})
        True
        """

        return {neighbour for neighbour in self.neighbours if isinstance(neighbour, _SongVertex)}

    def get_value_neighbours(self) -> set[_ValueVertex]:
        """
        Return a set of all _ValueVertex neighbours

        >>> vv = _ValueVertex('energy', 0.67)
        >>> vv.neighbours = {_ValueVertex('energy', 0.66), _ValueVertex('energy', 0.68)}
        >>> all({isinstance(neighbour, _ValueVertex) for neighbour in vv.get_value_neighbours()})
        True
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
        >>> sv.neighbours = {_ValueVertex('energy', 0.66), _ValueVertex('valence', 0.43)}
        >>> sv.get_value_of_type('energy')
        0.66
        """

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

    def get_song_vertex_by_name(self, song_name: str) -> _SongVertex:
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

    def get_value_vertex(self, type: str, value: float) -> _ValueVertex:
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

        if (type, value) in self._vertices:
            return self._vertices[(type, value)]
        else:
            raise ValueError

    def get_similarity_by_type(self, song1: str, song2: str, type: str) -> float:
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

        value1 = self._vertices[song1].get_value_of_type(type)
        value2 = self._vertices[song2].get_value_of_type(type)
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
        # for vertex in self.get_song_vertices():
        for vertex in self.get_vertices():
            if isinstance(vertex, _SongVertex):
                song_similarity_dict[vertex.item] = self.average_similarity(
                    self.get_song_by_name(song), vertex.item)
        sorted_similarity = sorted(song_similarity_dict, key=song_similarity_dict.get)
        return sorted_similarity[:limit + 1]

    def value_vertex_by_distance(self, vertex: _ValueVertex, distance: int) -> Any:
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

    graph = Graph()

    for i in range(0, 101):
        # Copy this line for every piece of information that's going to be used.
        graph.add_vertex(('danceability', i / 100), 'value', i / 100)
        graph.add_vertex(('energy', i / 100), 'value', i / 100)
        graph.add_vertex(('valence', i / 100), 'value', i / 100)

    for i in range(1, 101):
        # Copy this line for every piece of information that's going to be used.
        graph.add_edge(('danceability', (i - 1) / 100), ('danceability', i / 100))
        graph.add_edge(('energy', (i - 1) / 100), ('energy', i / 100))
        graph.add_edge(('valence', (i - 1) / 100), ('valence', i / 100))

    # This needs to be clarified as utf-8, for some reason it doesn't read it correctly otherwise.
    with open(information_file, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            graph.add_vertex(row[0], 'song')
            graph.add_song(row[1], row[0])
            # Copy this line for every piece of information that's going to be used.
            graph.add_edge(row[0], ('danceability', round(float(row[9]), 2)))
            graph.add_edge(row[0], ('energy', round(float(row[10]), 2)))
            graph.add_edge(row[0], ('valence', round(float(row[17]), 2)))

    return graph


def load_visualization_graph(main_graph: Graph, songs: list[str], given_song: str) -> Graph:
    """
    Create a graph with all the songs in songs and all the value vertices in between
    """

    graph = Graph()
    given_song_vertex = main_graph.get_song_vertex_by_name(given_song)

    # Make vertices for the given song and it's values, as well as edges between those.
    given_song_values = {}
    # graph.add_vertex(main_graph.get_song_by_name(given_song), 'song')
    graph.add_vertex(given_song, 'song')
    for vertex in given_song_vertex.neighbours:
        vtype = vertex.item
        value = vertex.value
        graph.add_vertex((vtype, value), 'value', value)
        # graph.add_edge(main_graph.get_song_by_name(given_song), (vtype, value))
        graph.add_edge(given_song, (vtype, value))
        given_song_values[vtype] = value

    # Create vertices for the input song as well as the result songs, and all their values
    for song in songs:
        # TODO see if this should be song_name or song_id (it's names rn)
        # graph.add_vertex(main_graph.get_song_by_name(song), 'song')
        graph.add_vertex(main_graph.get_song_by_id(song), 'song')
        for value_vertex in main_graph.get_song_vertex_by_name(main_graph.get_song_by_id(song)).neighbours:
            vtype = value_vertex.item
            value = value_vertex.value
            graph.add_vertex((vtype, value), 'value', value)
            # graph.add_edge(main_graph.get_song_by_name(song), (vtype, value))
            graph.add_edge(main_graph.get_song_by_id(song), (vtype, value))

            # Not sure if this works
            graph.connect_value_edges(
                (vtype, given_song_values[vtype]),
                (vtype, value)
            )

    return graph


# visualizing the graph
def display_graph(g: Graph = None):
    """
    Display the graph in the Tkinter window.
    """
    global figure, canvas, toolbar

    if canvas is not None:
        figure.clear()
    else:
        figure = plt.figure(figsize=(15, 8))
        canvas = FigureCanvasTkAgg(figure, master=graph_frame)

    ax = figure.add_subplot()
    values = ['danceability', 'energy', 'valence']
    node_colors = []

    if g is None:
        vis = nx.Graph()
        vis.add_node("No data available")
    else:
        vis = nx.Graph()
        for edge in g.get_edges():
            node1 = None
            node2 = None
            if isinstance(edge[0], _ValueVertex) and isinstance(edge[1], _ValueVertex):
                node1 = f'{edge[0].item}, {edge[0].value}'
                node2 = f'{edge[1].item}, {edge[1].value}'
                vis.add_edge(node1, node2)
            elif isinstance(edge[0], _ValueVertex):
                node1 = f'{edge[0].item}, {edge[0].value}'
                vis.add_edge(node1, edge[1].item)
            elif isinstance(edge[1], _ValueVertex):
                node2 = f'{edge[1].item}, {edge[1].value}'
                vis.add_edge(edge[0].item, node2)
            else:
                vis.add_edge(edge[0].item, edge[1].item)

        for node in vis.nodes:
            if any(value in node for value in values):
                node_colors.append('green')
            else:
                node_colors.append('blue')

    pos = nx.random_layout(vis)
    nx.draw(vis, ax=ax, pos=pos, with_labels=True, node_size=500, font_size=10,
            node_color=node_colors, edge_color='lightgray', width=1, alpha=0.7)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    if toolbar is None:
        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    else:
        toolbar.update()


def submission_of_user():
    """
    Handle the submit action: generate graph data based on user input and display the graph.
    """
    song_name = song_entry.get()
    num_recommendations = int(limit_var.get())

    if graph.does_song_name_exist(song_name):
        graph_data = graph.recommend_songs(song_name, num_recommendations)
        recommendation_graph = load_visualization_graph(graph, graph_data, song_name)

        display_graph(recommendation_graph)

        song_listbox.delete(0, tk.END)

        for song in graph_data:
            if song in graph.song_ids:
                song_listbox.insert(tk.END, graph.get_song_by_id(song))
    else:
        tk.messagebox.showwarning(title='Error', message="Song not in data base")


if __name__ == '__main__':
    # create graph
    # TODO decide if we want one million songs, one hundred thousand, or some other number.
    graph = load_graph("tracks_features_one_hundred_thousand.csv")
    # create GUI
    figure = None
    canvas = None
    toolbar = None

    root = tk.Tk()
    root.title("Music Recommendations")
    root.state('zoomed')

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

    listbox_frame = tk.Frame(root)
    listbox_frame.pack(fill=tk.BOTH, expand=True)
    song_listbox = tk.Listbox(listbox_frame, width=50, height=10)
    song_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    submit_button = tk.Button(input_frame, text="Submit", command=submission_of_user)
    submit_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()
