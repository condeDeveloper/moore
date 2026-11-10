# -*- coding: utf-8 -*-
"""Grafo simples nao dirigido, guardado como lista de mascaras de bits.

O grafo e uma tupla de inteiros: `g[v]` tem o bit `u` ligado quando existe a
aresta `u-v`. A tupla e imutavel de proposito, porque a busca de `busca.py`
guarda grafos em conjunto e compara um com o outro.

Aqui nao mora nada sobre grafos de Moore: so grau, distancia, diametro e
cintura, medidos do jeito mais obvio que existe. Quem decide se um grafo e de
Moore e o `juiz.py`, que nao importa uma linha deste arquivo.
"""
from __future__ import annotations

INFINITO = float("inf")


def grafo_de_arestas(n: int, arestas) -> tuple[int, ...]:
    """Monta o grafo de `n` vertices a partir de uma lista de pares."""
    g = [0] * n
    for u, v in arestas:
        if u == v:
            raise ValueError("laco nao e grafo simples: %d-%d" % (u, v))
        g[u] |= 1 << v
        g[v] |= 1 << u
    return tuple(g)


def arestas(g: tuple[int, ...]):
    """Devolve os pares `u < v` do grafo, em ordem."""
    saida = []
    for u in range(len(g)):
        resto = g[u] >> (u + 1)
        v = u + 1
        while resto:
            if resto & 1:
                saida.append((u, v))
            resto >>= 1
            v += 1
    return saida


def graus(g: tuple[int, ...]) -> list[int]:
    return [bin(viz).count("1") for viz in g]


def e_regular(g: tuple[int, ...], d: int) -> bool:
    return all(grau == d for grau in graus(g))


def distancias(g: tuple[int, ...], origem: int) -> list[float]:
    """Busca em largura a partir de `origem`. Vertice inalcancavel fica em `inf`."""
    n = len(g)
    dist: list[float] = [INFINITO] * n
    dist[origem] = 0
    fronteira = [origem]
    passo = 0
    vistos = 1 << origem
    while fronteira:
        passo += 1
        proxima = []
        for u in fronteira:
            novos = g[u] & ~vistos
            vistos |= novos
            while novos:
                b = novos & -novos
                v = b.bit_length() - 1
                dist[v] = passo
                proxima.append(v)
                novos ^= b
        fronteira = proxima
    return dist


def conexo(g: tuple[int, ...]) -> bool:
    if not g:
        return True
    return all(d != INFINITO for d in distancias(g, 0))


def diametro(g: tuple[int, ...]) -> float:
    """Maior distancia entre dois vertices. `inf` se o grafo for desconexo."""
    maior: float = 0
    for v in range(len(g)):
        d = max(distancias(g, v))
        if d == INFINITO:
            return INFINITO
        if d > maior:
            maior = d
    return maior


def cintura(g: tuple[int, ...]) -> float:
    """Menor ciclo do grafo, por busca em largura a partir de cada vertice.

    A busca em largura acha o menor ciclo que PASSA pela origem; o minimo sobre
    todas as origens e a cintura. Grafo sem ciclo devolve `inf`.
    """
    n = len(g)
    melhor: float = INFINITO
    for raiz in range(n):
        dist = [-1] * n
        pai = [-1] * n
        dist[raiz] = 0
        fila = [raiz]
        i = 0
        while i < len(fila):
            u = fila[i]
            i += 1
            if dist[u] * 2 >= melhor:
                break
            viz = g[u]
            while viz:
                b = viz & -viz
                v = b.bit_length() - 1
                viz ^= b
                if v == pai[u]:
                    continue
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    pai[v] = u
                    fila.append(v)
                else:
                    ciclo = dist[u] + dist[v] + 1
                    if ciclo < melhor:
                        melhor = ciclo
    return melhor


def vizinhos_comuns(g: tuple[int, ...], u: int, v: int) -> int:
    return bin(g[u] & g[v]).count("1")


def _assinaturas(g: tuple[int, ...]) -> list[tuple]:
    """Invariante por vertice que nao depende da numeracao: o vetor de distancias."""
    return [tuple(sorted(distancias(g, v))) for v in range(len(g))]


def sao_isomorfos(g: tuple[int, ...], h: tuple[int, ...]) -> bool:
    """Isomorfismo por casamento vertice a vertice, com poda.

    Nao e canonizacao: e uma busca que tenta construir UMA bijecao. Para os
    grafos deste projeto (no maximo 50 vertices, muito regulares) o teste por
    forca bruta sobre permutacoes seria 50!, entao o caminho e este.

    A poda: so casa vertices com a mesma assinatura de distancias, e so estende
    a bijecao quando as arestas ja decididas batem exatamente.
    """
    n = len(g)
    if n != len(h) or sorted(graus(g)) != sorted(graus(h)):
        return False
    ag, ah = _assinaturas(g), _assinaturas(h)
    if sorted(ag) != sorted(ah):
        return False

    destino = [-1] * n
    usado = [False] * n

    def tenta(v: int) -> bool:
        if v == n:
            return True
        for w in range(n):
            if usado[w] or ag[v] != ah[w]:
                continue
            ok = True
            for u in range(v):
                tem_g = (g[v] >> u) & 1
                tem_h = (h[w] >> destino[u]) & 1
                if tem_g != tem_h:
                    ok = False
                    break
            if not ok:
                continue
            destino[v] = w
            usado[w] = True
            if tenta(v + 1):
                return True
            usado[w] = False
            destino[v] = -1
        return False

    return tenta(0)


def classes_de_isomorfismo(grafos) -> list:
    """Agrupa uma lista de grafos; devolve um representante por classe."""
    representantes: list = []
    for g in grafos:
        if not any(sao_isomorfos(g, r) for r in representantes):
            representantes.append(g)
    return representantes
