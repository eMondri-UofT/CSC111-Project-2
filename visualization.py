"""CSC111 Winter 2024 Project 2
    Title: "Music Reccomendations based on key factors"
            - Graph Visualization
    Author: Mark Lu, Ethan Mondri, _, _
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import main as mn


def display_graph(g=None):
    """
    Display the graph in the Tkinter window.
    """
    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots()

    if g is None:
        g = nx.Graph()
        g.add_node("No data available")

    nx.draw(g, ax=ax, with_labels=True, node_size=700,
            node_color='skyblue')

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def on_submit():
    """
    Handle the submit action: generate graph data based on user input and display the graph.
    """
    song_name = song_entry.get()
    num_recommendations = int(limit_var.get())
    graph_data = mn.generate_graph_based_on_input(song_name, num_recommendations)
    display_graph(graph_data)


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

submit_button = tk.Button(input_frame, text="Submit", command=on_submit)
submit_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
