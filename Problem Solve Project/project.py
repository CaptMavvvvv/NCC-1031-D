import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import folium
from tkinter import filedialog

locations = {
    "CentralWorld": (13.7466, 100.5395, "Bangkok"),
    "Central Ladprao": (13.8123, 100.5615, "Bangkok"),
    "Central Bangna": (13.6685, 100.6212, "Bangkok"),
    "Central Pinklao": (13.7801, 100.4855, "Bangkok"),
    "Central Rama 9": (13.7547, 100.5662, "Bangkok"),
    "Central EastVille": (13.8168, 100.6122, "Bangkok"),
    "Central Ramindra": (13.8569, 100.6209, "Bangkok"),
    "Central Rama 3": (13.6826, 100.5283, "Bangkok"),
    "Central Chaengwattana": (13.8967, 100.5362, "Bangkok"),
    "Central Rattanathibet": (13.8669, 100.4956, "Nonthaburi"),
    "Central Westgate": (13.8770, 100.4113, "Nonthaburi"),
    "Central Village": (13.6397, 100.7438, "Samut Prakan"),
    "Central Salaya": (13.7874, 100.2762, "Bangkok"),
    "Central Mahachai": (13.5728, 100.2892, "Samut Sakhon"),
    "Esplanade Ratchada": (13.7666, 100.5698, "Bangkok"),
    "Mega Bangna": (13.6452, 100.6807, "Bangkok"),
    "Central Rama 2": (13.6631, 100.4396, "Bangkok"),
}

G = nx.Graph()

for mall, (lat, lon, province) in locations.items():
    G.add_node(mall, pos=(lon, lat), province=province)

edges = [
    ("CentralWorld", "Central Ladprao", 12),
    ("CentralWorld", "Central Rama 9", 4),
    ("Central Ladprao", "Central Bangna", 15),
    ("Central Ladprao", "Central Chaengwattana", 10),
    ("Central Bangna", "Mega Bangna", 7),
    ("Central Bangna", "Central Rama 2", 12),
    ("Central Pinklao", "Central Rama 9", 7),
    ("Central Rama 9", "Esplanade Ratchada", 3),
    ("Central Rama 9", "Central EastVille", 6),
    ("Central Rama 3", "Central Rama 2", 9),
    ("Central Chaengwattana", "Central Rattanathibet", 6),
    ("Central Rattanathibet", "Central Westgate", 10),
    ("Central Salaya", "Central Pinklao", 15),
    ("Central Salaya", "Central Mahachai", 20),
    ("Central Village", "Mega Bangna", 8),
    ("Central Westgate", "Central Chaengwattana", 9),
    ("Central Ramindra", "Central Ladprao", 8),
    ("Central Ramindra", "Central EastVille", 7),
    ("Central Mahachai", "Central Rama 2", 18),
    ("Central Village", "Central Bangna", 10),
    ("Central Salaya", "Central Rama 3", 17),
    ("Esplanade Ratchada", "CentralWorld", 5),
    ("Mega Bangna", "Central EastVille", 14),
]

for u, v, car_distance in edges:
    bike_distance = car_distance * 0.8
    G.add_edge(u, v, car=car_distance, bike=bike_distance)

def find_fastest_route(start, destination, mode, day_type):
    weight_type = "car" if mode == "Car" else "bike"
    try:
        if mode == "Motorcycle":
            G_temp = G.copy()
            for u, v, data in G_temp.edges(data=True):
                data["bike"] = data["bike"] / 1.5 
        else:
            G_temp = G

        path = nx.shortest_path(G_temp, source=start, target=destination, weight=weight_type)
        distance = nx.shortest_path_length(G_temp, source=start, target=destination, weight=weight_type)

        if day_type == "Weekday":
            distance /= 1.3
        elif day_type == "Weekend":
            distance *= 2 

        return path, distance
    except nx.NetworkXNoPath:
        return None, None

def generate_map(path):
    start_coords = locations[path[0]][0:2]
    route_map = folium.Map(location=start_coords, zoom_start=12)

    for mall in path:
        lat, lon = locations[mall][0], locations[mall][1]
        folium.Marker([lat, lon], popup=mall).add_to(route_map)

    route_coords = [(locations[mall][0], locations[mall][1]) for mall in path]
    folium.PolyLine(route_coords, color="blue", weight=5).add_to(route_map)

    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if file_path:
        route_map.save(file_path)
        messagebox.showinfo("Map Saved", f"Map has been saved to {file_path}")

def find_shortest_path():
    start = start_var.get()
    destination = destination_var.get()
    vehicle = vehicle_var.get()
    day_type = day_var.get()

    if start == destination:
        messagebox.showwarning("Warning", "Please select a different destination.")
        return

    path, distance = find_fastest_route(start, destination, vehicle, day_type)

    if path is None:
        messagebox.showerror("Error", "No available route.")
        return

    result = f"Fastest Path: {start} → {destination} ({vehicle}, {day_type})\n"
    result += f" ➝ {' ➝ '.join(path)}\n"
    result += f"Time: {distance:.1f} units\n\n"

    result_text.set(result)
    draw_graph(highlight_path=path)

    if messagebox.askyesno("Generate Map", "Do you want to generate a map for this route?"):
        generate_map(path)

root = tk.Tk()
root.title("Mall Route Finder")
root.geometry("900x750")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill="both", expand=True)

input_frame = tk.LabelFrame(main_frame, text="Route Finder Inputs", font=("Arial", 14), padx=10, pady=10)
input_frame.pack(fill="x", pady=10)

tk.Label(input_frame, text="🏙️ Start Location", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
start_var = tk.StringVar(value="CentralWorld")
start_menu = ttk.Combobox(input_frame, textvariable=start_var, values=list(locations.keys()), state="readonly", width=30)
start_menu.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="🏁 Destination", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
destination_var = tk.StringVar(value="Central Ladprao")
destination_menu = ttk.Combobox(input_frame, textvariable=destination_var, values=list(locations.keys()), state="readonly", width=30)
destination_menu.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="🚗 Vehicle Type", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
vehicle_var = tk.StringVar(value="Car")
vehicle_menu = ttk.Combobox(input_frame, textvariable=vehicle_var, values=["Car", "Motorcycle"], state="readonly", width=30)
vehicle_menu.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="📅 Day Type", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
day_var = tk.StringVar(value="Weekday")
day_menu = ttk.Combobox(input_frame, textvariable=day_var, values=["Weekday", "Weekend"], state="readonly", width=30)
day_menu.grid(row=3, column=1, padx=5, pady=5)

find_route_button = tk.Button(input_frame, text="🔍 Find Route", font=("Arial", 12), command=find_shortest_path)
find_route_button.grid(row=4, column=0, columnspan=2, pady=10)

result_frame = tk.LabelFrame(main_frame, text="Route Information", font=("Arial", 14), padx=10, pady=10)
result_frame.pack(fill="x", pady=10)

result_text = tk.StringVar(value="Select a location and vehicle, then click 'Find Route'.")
result_label = tk.Label(result_frame, textvariable=result_text, wraplength=800, font=("Arial", 12), fg="blue", justify="left")
result_label.pack(pady=5)

graph_frame = tk.LabelFrame(main_frame, text="Mall Network Visualization", font=("Arial", 14), padx=10, pady=10)
graph_frame.pack(fill="both", expand=True, pady=10)

fig, ax = plt.subplots(figsize=(10, 7)) 
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

def draw_graph(highlight_path=None):
    ax.clear()
    pos = nx.get_node_attributes(G, 'pos')

    province_colors = {
        "Bangkok": "orange",
        "Nonthaburi": "lightblue",
        "Samut Prakan": "green",
        "Samut Sakhon": "red"
    }
    
    node_colors = [province_colors[G.nodes[node]["province"]] for node in G.nodes]

    nx.draw(G, pos, ax=ax, node_size=200, node_color=node_colors, with_labels=True, font_size=8, font_weight="bold")

    if highlight_path:
        path_edges = list(zip(highlight_path, path_edges, edge_color="blue", width=3))

    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Bangkok', markerfacecolor='orange', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Nonthaburi', markerfacecolor='lightblue', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Samut Prakan', markerfacecolor='green', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Samut Sakhon', markerfacecolor='red', markersize=10),
    ]
    ax.legend(handles=legend_elements, loc='upper left', title="Provinces", fontsize=10)

    ax.set_title("Mall Network with Lat/Lon Positions and Provinces", fontsize=14)
    canvas.draw()

root.mainloop()