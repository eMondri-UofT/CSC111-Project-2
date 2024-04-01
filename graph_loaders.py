"""CSC111 Winter 2024 Project 2
    File containing two functions to create a graph.
"""
from __future__ import annotations
import csv
import doctest
import python_ta
import graph_classes


def load_graph(information_file: str) -> graph_classes.Graph:
    """
    Return a graph containing the information in information_file.

    Preconditions:
        - information_file is the path to a CSV file with the dataset in the specified format.
    """

    graph = graph_classes.Graph()

    for i in range(0, 101):
        graph.add_vertex(('danceability', i / 100), 'value', i / 100)
        graph.add_vertex(('energy', i / 100), 'value', i / 100)
        graph.add_vertex(('valence', i / 100), 'value', i / 100)

    for i in range(1, 101):
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
            # Note that this is using a stripped version of the file.
            # Using the base dataset, these columns are 10, 11, and 18
            graph.add_edge(row[0], ('danceability', round(float(row[2]), 2)))
            graph.add_edge(row[0], ('energy', round(float(row[3]), 2)))
            graph.add_edge(row[0], ('valence', round(float(row[4]), 2)))

    return graph


def load_visualization_graph(main_graph: graph_classes.Graph,
                             songs: list[str], given_song: str) -> graph_classes.Graph:
    """
    Create a graph with all the songs in songs and all the value vertices in between
    """

    graph = graph_classes.Graph()
    given_song_vertex = main_graph.get_song_vertex_by_name(given_song)

    # Make vertices for the given song and it's values, as well as edges between those.
    given_song_values = {}
    # graph.add_vertex(main_graph.get_song_by_name(given_song), 'song')
    graph.add_vertex(given_song, 'song')
    for vertex in given_song_vertex.neighbours:
        vtype = vertex.item
        value = vertex.value
        graph.add_vertex((vtype, value), 'value', value)
        graph.add_edge(given_song, (vtype, value))
        given_song_values[vtype] = value

    # Create vertices for the input song as well as the result songs, and all their values
    for song in songs:
        graph.add_vertex(main_graph.get_song_by_id(song), 'song')
        for value_vertex in main_graph.get_song_vertex_by_name(main_graph.get_song_by_id(song)).neighbours:
            vtype = value_vertex.item
            value = value_vertex.value
            graph.add_vertex((vtype, value), 'value', value)
            graph.add_edge(main_graph.get_song_by_id(song), (vtype, value))

            graph.connect_value_edges(
                (vtype, given_song_values[vtype]),
                (vtype, value)
            )

    return graph


if __name__ == '__main__':
    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['annotations', 'csv', 'graph_classes'],  # the names (strs) of imported modules
        'allowed-io': ['load_graph'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
