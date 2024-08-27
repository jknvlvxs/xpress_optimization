from shapely.geometry import Point
from geopy.geocoders import Nominatim
import geopy.distance
import pickle
import random

geolocator = Nominatim(user_agent="Webscrapper")


# Função para buscar coordenadas
def coord(cidade):
    location = geolocator.geocode(f"{cidade['nome']}")
    return (location.latitude, location.longitude)


# Função para calcular a distância entre duas coordenadas
def distancia(coord1, coord2):
    if coord1 == coord2: return 9999
    return int(geopy.distance.geodesic(coord1, coord2).km)


# Função para carregar dados das cidades
def load_cidades(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    table_start = next(
        (i for i, line in enumerate(lines) if line.startswith("-")), None
    )

    if table_start is None:
        return []

    return [
        {
            "nome": f"{line[:40].strip()}, {line[40:43].strip()}, Brazil",
            "pop": int(line[43:].strip()),
        }
        for line in lines[table_start + 1 :]
    ]


# Função para mover uma cidade para uma nova posição
def mover_cidade(coord, direcao, distancia_km):
    novo_ponto = geopy.distance.distance(kilometers=distancia_km).destination(
        coord, direcao
    )
    return (novo_ponto.latitude, novo_ponto.longitude)


# Função para agrupar cidades em uma grade para reduzir comparações
def agrupar_cidades(cities, grid_size=200):
    grouped = {}
    for cidade, coords in cities.items():
        grid_key = (int(coords[0] // grid_size), int(coords[1] // grid_size))
        if grid_key not in grouped:
            grouped[grid_key] = []
        grouped[grid_key].append(cidade)
    return grouped


# Função principal para ajustar cidades próximas

def ajustar_cidades_proximas(cities, limite_km=200):
    for cidade1 in cities:
        for cidade2 in cities:
            if cidade1 != cidade2:
                dist = distancia(cities[cidade1], cities[cidade2])
                if dist < limite_km:
                    c1 = [c for c in cidades if cidade1 in c["nome"]].pop()
                    c2 = [c for c in cidades if cidade2 in c["nome"]].pop()
                    print("Ajustando cidades próximas:", cidade1, cidade2)

                    if c1["pop"] < c2["pop"]:
                        cities[cidade1] = mover_cidade(cities[cidade1], random.randint(200, 360), 90)
                    else:
                        cities[cidade2] = mover_cidade(cities[cidade2], random.randint(200, 360), 90)
    return cities



# Função para formatar o nome da cidade
def formatar_nome(nome):
    return nome.split(",")[0]


# Carregar as cidades do arquivo
cidades = load_cidades("dados/Dados_G05.txt")

# Obter as coordenadas das cidades
cities = {formatar_nome(cidade["nome"]): coord(cidade) for cidade in cidades}

# Ajustar as cidades que estão muito próximas
iteracoes = 0
while True:
    print(f"\nIteração {iteracoes}")
    cities = ajustar_cidades_proximas(cities)
    distancias = [[distancia(cities[cidade], cities[cidade2]) for cidade2 in cities] for cidade in cities]
    iteracoes += 1
    print(min(distancias))
    if(min(min(distancias)) > 200):
        break

# Salvar as coordenadas ajustadas em um arquivo
with open("mapas/dados/cities.pkl", "wb") as file:
    pickle.dump(cities, file)
