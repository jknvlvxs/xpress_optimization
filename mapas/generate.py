import matplotlib.pyplot as plt
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point
import pickle


def cities_color(cities):
    colors = []
    for city in cities:
        if city == "Macaé":
            colors.append("#FFFF00")
        elif city == "Salvador":
            colors.append("#0000FF")
        elif city == "Belo Horizonte":
            colors.append("#00FF00")
        else:
            colors.append("#FFFF00")
    print(colors)
    return colors


# Load cities object from 'cities.pkl'
with open("mapas/dados/cities.pkl", "rb") as f:
    cities = pickle.load(f)

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
G = nx.Graph()

# Adicionar nós
for city, (lat, lon) in cities.items():
    G.add_node(city, pos=(lon, lat))

# Adicionar arestas
# G.add_edge("Porto Alegre", "Salvador")
# G.add_edge("Belo Horizonte", "Salvador")

# Plotar o mapa do Brasil
fig, ax = plt.subplots(figsize=(10, 10))
brasil.plot(ax=ax, color="lightgray")

# Plotar os nós das cidades
city_points.plot(ax=ax, color=cities_color(cities.keys()), markersize=100)

# Obter as posições dos nós para o grafo
pos = nx.get_node_attributes(G, "pos")

# Desenhar o grafo sobre o mapa
nx.draw(
    G,
    pos,
    ax=ax,
    with_labels=True,
    edge_color="blue",
    node_size=1,
    font_size=7,
    font_color="black",
    alpha=0.8,
)

plt.show()
