from geopy.geocoders import Nominatim
import geopy.distance
import os

path = os.path.dirname(os.path.abspath(__file__))

def coord(cid):
    coord = geolocator.geocode(f"{cid}")
    return (coord.latitude, coord.longitude)

def distancia(coord1, coord2):
    return int(geopy.distance.geodesic(coord1, coord2).km)


def load_cidades(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    table_start = next((i for i, line in enumerate(lines) if line.startswith("-")), None)

    if table_start is None: return []

    return [f"{line[:40].strip()}, {line[40:43].strip()}, Brazil" for line in lines[table_start + 1 :]]


if __name__ == "__main__":
    geolocator = Nominatim(user_agent="Webscrapper")

    target = coord("Macaé, RJ, Brazil")

    cidades = load_cidades(f"{path}/Dados_G05.txt")
    coordenadas = [coord(cidade) for cidade in cidades]

    distancias_macae = [distancia(cidade, target) for cidade in coordenadas]
    matriz_distancias = [[distancia(cidade, cidade2) or 5 for cidade2 in coordenadas] for cidade in coordenadas]

    print(f"{distancias_macae}\n\n{matriz_distancias}")
