# COVID19_Taxi_App

Análise de propagação epidemiológica baseada nos trajectos da tabela tracks e a visualização recorrendo às animações do matplotlib de tal propagação

## Objetivos

Este projeto tem os seguintes objetivos:

    - Representaçao do mapa de Portugal continental e dos trajetos de taxis
    - Calculos de propagaçao epidemiológica ao longo de 24 horas
    - Otimizaçao da simulaçao

## Sobre os criadores

| Nome            | Universidade  | País     |    Linkedin   |
| --------------- |:-------------:|:-------: | -------------:|
| Solange Sampaio | [FCUP][1]     | Portugal |  [Profile][2]  |
| José Sousa      | [FCUP][1]     | Portugal |  [Profile][3]  |

[1]: https://sigarra.up.pt/fcup/en/WEB_PAGE.INICIAL
[2]: https://www.linkedin.com/in/solange-sampaio-5a1b8915b
[3]: https://www.linkedin.com/in/jose-pedro-sousa-71328612a/

## Sobre a linguagem e modulos

Este projeto foi desenvolvido usando a linguagem de programaçao [Python 3.0](https://www.python.org/download/releases/3.0/)

Tambem foram usados varios modulos para a criaçao e visualização da simulaçao:

    - matplotlib
    - numpy
    - psycopg2
    - postgis
    - csv
    - math
    - random
    - pandas
    - time
    - queue
    - heapq
    - datetime

Alem da implementaçao e do uso dos modulos, usou-se uma base de dados [PostGreSQL](https://www.postgresql.org/) para obter os dados para o desenho do mapa de Portugal continental e para a representaçao dos trajetos dos taxis

## Sobre cada ficheiro

- propagation.py
    Calculos de propagaçao epidemiológica

- animation_concelho.py
    Calculo da imagem mostrada no final da execuçao do numeros de infetados por concelho num grafico de barras

- anim.csv
    Ficheiro que contem a informaçao sobre os taxis infetados ou nao infetados

- lines.py
    Representaçao no mapa com as estradas para as animaçoes com os taxis

- tracks_animation
    Representaçao da simulaçao com o mapa de Portugal Continental com os taxis e os seus trajetos ao longo de 24 horas
