import matplotlib.pyplot as plt
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point
import pickle


def cities_color(cities, edges):
    # Se cidade é Macaé, deve ser amarela
    # Se cidade tiver aresta com Macaé, deve ser vermelha
    # Se cidade não tiver aresta com Macaé, deve ser azul
    colors = []

    for city in cities:
        if city == "Macaé":
            colors.append("yellow")
        elif any(
            edge["CIDADE A"] == "Macaé" and edge["CIDADE B"] == city for edge in edges
        ):
            colors.append("red")
        else:
            colors.append("blue")

    return colors


def edge_color(subproduct):
    if subproduct == "Petróleo":
        return "yellow"
    elif subproduct == "Gasolina":
        return "red"
    elif subproduct == "Diesel":
        return "cyan"
    elif subproduct == "Naftas":
        return "orange"
    elif subproduct == "GLP":
        return "purple"
    else:
        return "black"


# Load cities object from 'cities.pkl'
with open("mapas/dados/cities.pkl", "rb") as f:
    cities = pickle.load(f)

# Load edges object from 'edges.pkl'
with open("mapas/dados/arestas/edges_1.pkl", "rb") as f:
    edges = pickle.load(f)

# Criando um GeoDataFrame para as cidades
city_points = gpd.GeoDataFrame(
    {"city": cities.keys()},
    geometry=[Point(lon, lat) for lat, lon in cities.values()],
    crs="EPSG:4326",
)

# Carregar o shapefile do Brasil
shapefile_path = "mapas/dados/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"  # Altere para o caminho do seu shapefile
brasil = gpd.read_file(shapefile_path)
brasil = brasil[brasil["NAME"] == "Brazil"]

# Criar o grafo
G = nx.DiGraph()

# Adicionar nós
for city, (lat, lon) in cities.items():
    G.add_node(city, pos=(lon, lat))

# Adicionar arestas
for edge in edges:
    G.add_edge(
        edge["CIDADE A"],
        edge["CIDADE B"],
        weight=edge["VALOR"],
        color=edge_color(edge["ITEM"]),
    )


colors = [edge[2]['color'] for edge in [edges for edges in G.edges(data=True)]]

# Plotar o mapa do Brasil
fig, ax = plt.subplots(figsize=(10, 10))
brasil.plot(ax=ax, color="lightgray")

# Plotar os nós das cidades
city_points.plot(ax=ax, color=cities_color(cities.keys(), edges), markersize=100)

# Obter as posições dos nós para o grafo
pos = nx.get_node_attributes(G, "pos")

# Desenhar o grafo sobre o mapa
nx.draw(
    G,
    pos,
    ax=ax,
    with_labels=True,
    edge_color=colors,
    node_size=1,
    font_size=7,
    font_color="black",
    alpha=0.8,
    arrows=True,
)

plt.show()
