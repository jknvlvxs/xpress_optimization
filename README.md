
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
