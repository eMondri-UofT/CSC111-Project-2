"""CSC111 Winter 2024 Project 2
    Title: "Music Reccomendations based on key factors"
    Authors: Mark Lu, Ethan Mondri, Ata Yenipazar, Omer Recep Kaya

    File contains user interface and main block
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
import graph_classes
import graph_loaders
import python_ta


# visualizing the graph
def display_graph(g: graph_classes.Graph = None) -> None:
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
            if isinstance(edge[0], graph_classes.ValueVertex) and isinstance(edge[1], graph_classes.ValueVertex):
                node1 = f'{edge[0].item}, {edge[0].value}'
                node2 = f'{edge[1].item}, {edge[1].value}'
                vis.add_edge(node1, node2)
            elif isinstance(edge[0], graph_classes.ValueVertex):
                node1 = f'{edge[0].item}, {edge[0].value}'
                vis.add_edge(node1, edge[1].item)
            elif isinstance(edge[1], graph_classes.ValueVertex):
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
            node_color=node_colors, edge_color='lightgray', width=1, alpha=0.5)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    if toolbar is None:
        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    else:
        toolbar.update()


def submission_of_user() -> None:
    """
    Handle the submit action: generate graph data based on user input and display the graph.
    """
    song_name = song_entry.get()
    num_recommendations = int(limit_var.get())

    if graph.does_song_name_exist(song_name):
        graph_data = graph.recommend_songs(song_name, num_recommendations)
        recommendation_graph = graph_loaders.load_visualization_graph(graph, graph_data, song_name)

        display_graph(recommendation_graph)

        song_listbox.delete(0, tk.END)

        for song in graph_data:
            if song in graph.song_ids:
                song_listbox.insert(tk.END, graph.get_song_by_id(song))
    else:
        tk.messagebox.showwarning(title='Error', message="Song not in data base")


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })

    # create graph
    graph = graph_loaders.load_graph("tracks_features_one_million_necessary_columns.csv")
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
