from geopy.geocoders import Nominatim
import geopy.distance
import os

path = os.path.dirname(os.path.abspath(__file__))

def coord(cid):
    coord = geolocator.geocode(f"{cid}")
    return (coord.latitude, coord.longitude)


def distancia(coord1, coord2):
    return int(geopy.distance.geodesic(coord1, coord2).km)


if __name__ == "__main__":
    geolocator = Nominatim(user_agent="Webscrapper")
    table = False

    target = coord("Macaé, RJ, Brazil")
    cidades = []
    distancias_macae = []

    with open(f"{path}/Dados_G05.txt", "r") as file:
        for line in file:
            linha = line.strip()

            if linha.startswith("-"):
                table = True
                continue

            if table:
                cidade = linha[:40].strip()
                estado = linha[40:43].strip()
                cidades.append(coord(f"{cidade}, {estado}, Brazil"))

    for cidade in cidades:
        distancias_macae.append(distancia(cidade, target))

    print(distancias_macae)
    print("\n\n")

    matriz_distancias = [
        [distancia(cidade, cidade2) or 5 for cidade2 in cidades] for cidade in cidades
    ]

    print(matriz_distancias)
