from shapely.geometry import Point
from geopy.geocoders import Nominatim
import geopy.distance
import pickle

geolocator = Nominatim(user_agent="Webscrapper")


def coord(cid):
    coord = geolocator.geocode(f"{cid}")
    return (coord.latitude, coord.longitude)


def load_cidades(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    table_start = next(
        (i for i, line in enumerate(lines) if line.startswith("-")), None
    )

    if table_start is None:
        return []

    return [
        f"{line[:40].strip()}, {line[40:43].strip()}, Brazil"
        for line in lines[table_start + 1 :]
    ]


cidades = load_cidades("dados/Dados_G05.txt")

cities = {}

for cidade in cidades:
    cities[cidade.split(",")[0]] = coord(cidade)

with open("mapas/dados/cities.pkl", "wb") as file:
    pickle.dump(cities, file)
