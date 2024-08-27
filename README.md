
# Gerar distâncias

## Instalar pacotes necessários
> pip install geopy

## Gerar arquivo de distâncias
> python dados/mat_dist.py > dados/distancias.txt

## Rodando cenários com Xpress-MP
Para rodar é necessário instalar o [Xpress](https://www.fico.com/fico-xpress-optimization/docs/latest/installguide/dhtml/chapinst1.html)

### Compilar cenário
> mosel comp cenario_x/model.mos

### Rodar o cenário
> model exec cenario_x/model.bim > cenario_x/output.txt

# Gerar mapas

## Instalas pacotes necessários
> pip install networkx geopandas

## Baixar Natural Earth Data
Baixar o mapa de países em [Natural Earth Data](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/), extrair a pasta `ne_110m_admin_0_countries` no diretório `/mapas`

## Gerar pickle de coordenadas entre nós
> python mapas/coords.py

Irá gerar o arquivo `mapas/dados/cities.pkl` que será usado para desenhar os nós no mapa