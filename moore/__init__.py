# -*- coding: utf-8 -*-
"""Grafos de Moore de diametro 2, construidos e julgados por dois caminhos.

O pacote tem quatro pedacos que nao se misturam:

    nucleo   grafo, grau, distancia, diametro, cintura, isomorfismo
    juiz     a condicao espectral e o verificador da definicao
    busca    o backtracking que constroi os grafos aresta por aresta
    medidas  as tabelas que vao para o README

O `juiz` nao importa a `busca` e a `busca` nao importa o `juiz`: e de proposito,
e e o que faz os numeros valerem alguma coisa.
"""
from .busca import Estourou, Resultado, nos_sem_poda, varrer
from .juiz import (e_grafo_de_moore, grau_admissivel, graus_admissiveis,
                   multiplicidades, ordem_de_moore)
from .nucleo import (arestas, cintura, classes_de_isomorfismo, conexo,
                     diametro, distancias, e_regular, grafo_de_arestas, graus,
                     sao_isomorfos, vizinhos_comuns)

__all__ = [
    "Estourou", "Resultado", "arestas", "cintura", "classes_de_isomorfismo",
    "conexo", "diametro", "distancias", "e_grafo_de_moore", "e_regular",
    "grafo_de_arestas", "grau_admissivel", "graus", "graus_admissiveis",
    "multiplicidades", "nos_sem_poda", "ordem_de_moore", "sao_isomorfos",
    "varrer", "vizinhos_comuns",
]

__version__ = "1.0.0"
