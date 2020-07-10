# COVID19_Taxi_App

Análise de propagação epidemiológica baseada nos trajectos da tabela tracks e a visualização recorrendo às animações do matplotlib de tal propagação.

## Objetivos

Este projeto tem os seguintes objetivos:

    - Representação do mapa de Portugal continental e dos trajetos de taxis
    - Simulação da propagação epidemiológica ao longo de 24 horas
    - Otimização da simulação

## Sobre os criadores

| Nome            | Universidade  | País     |    Linkedin   |
| --------------- |:-------------:|:-------: | -------------:|
| Solange Sampaio | [FCUP][1]     | Portugal |  [Profile][2] |
| José Sousa      | [FCUP][1]     | Portugal |  [Profile][3] |

[1]: https://sigarra.up.pt/fcup/en/WEB_PAGE.INICIAL
[2]: https://www.linkedin.com/in/solange-sampaio-5a1b8915b
[3]: https://www.linkedin.com/in/jose-pedro-sousa-71328612a/

## Sobre a linguagem e módulos

Este projeto foi desenvolvido usando a linguagem de programação [Python 3.0](https://www.python.org/download/releases/3.0/)

Tambem foram usados vários módulos para a criação e visualização da simulação:

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

Além da implementação e do uso dos módulos, usou-se uma base de dados [PostGreSQL](https://www.postgresql.org/) para obter os dados para a representação do mapa de Portugal continental e para a representação dos trajetos dos taxis.

## Sobre cada ficheiro

- propagation.py
    Calculos de propagação epidemiológica

- animation_concelho.py
    Cálculo do gráfico com o número total de infetados por concelho, no distrito do Porto e Lisboa

- anim.csv
    Ficheiro que contem a informaçao sobre os taxis infetados ou nao infetados

- lines.py
    Representação dos trajetos dos taxis no mapa com as estradas do distrito do Porto e de Lisboa

- tracks_animation
    Representação da simulação com o mapa de Portugal Continental com os taxis e os seus trajetos ao longo de 24 horas
