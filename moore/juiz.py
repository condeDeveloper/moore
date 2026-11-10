# -*- coding: utf-8 -*-
"""O juiz: decide por algebra, sem olhar um grafo.

A busca de `busca.py` constroi grafos aresta por aresta. Este arquivo nao
importa nada de la e nao recebe grafo nenhum em duas das tres funcoes: ele
responde quais graus PODEM ter grafo de Moore de diametro 2 olhando so para os
autovalores que esse grafo teria de ter.

A conta, em uma linha: um grafo de Moore de grau d e diametro 2 tem d*d+1
vertices, nenhum triangulo e exatamente um vizinho comum entre dois vertices
nao adjacentes. Isso o torna fortemente regular com parametros
(d*d+1, d, 0, 1), e os autovalores de um grafo fortemente regular sao d e as
raizes de x*x + x - (d-1) = 0, que sao (-1 +- raiz(4d-3)) / 2. As
multiplicidades saem de duas equacoes de traco:

    m+ + m-                 = d*d          (traco de A e zero, fora o d)
    r*m+ + s*m-             = -d

Multiplicidade e contagem de autovetores: tem de ser inteiro nao negativo. Se
raiz(4d-3) for irracional a unica saida e m+ = m-, que forca d = 2. Se for
inteiro s, a divisibilidade so fecha para s em {1, 3, 5, 15}, isto e,
d em {1, 3, 7, 57}.

Isto e um teorema de 1960 (Hoffman e Singleton). Aqui ele e um PROGRAMA, e o
programa e quem responde: a varredura de `graus_admissiveis` nao sabe o
resultado, ela testa d por d.
"""
from __future__ import annotations

from math import isqrt

from .nucleo import cintura, diametro, e_regular, vizinhos_comuns


def ordem_de_moore(d: int, k: int = 2) -> int:
    """A cota de Moore: quantos vertices cabem num grafo de grau d e diametro k.

    Uma arvore de busca a partir de um vertice: 1 + d + d*(d-1) + ... Nenhum
    grafo de grau d e diametro k passa disso, e os que empatam sao os de Moore.
    """
    if d < 1 or k < 1:
        raise ValueError("grau e diametro comecam em 1")
    if d == 1:
        return 2 if k >= 1 else 1
    if d == 2:
        return 2 * k + 1
    total = 1
    camada = d
    for _ in range(k):
        total += camada
        camada *= d - 1
    return total


def multiplicidades(d: int):
    """As duas multiplicidades de um grafo de Moore (d, 2), ou None.

    Devolve `(m_mais, m_menos)` quando as duas sao inteiras e nao negativas, e
    `None` quando a algebra ja proibe esse grau. Nao recebe grafo nenhum: so o
    numero d.
    """
    if d < 1:
        return None
    if d == 2:
        # raiz(5) e irracional: so fecha com m+ = m-, e so d = 2 permite.
        return (2, 2)
    s = isqrt(4 * d - 3)
    if s * s != 4 * d - 3:
        return None
    # m+ - m- = (2d - d*d) / s, e m+ + m- = d*d.
    numerador = 2 * d - d * d
    if numerador % s != 0:
        return None
    diferenca = numerador // s
    if (d * d + diferenca) % 2 != 0:
        return None
    m_mais = (d * d + diferenca) // 2
    m_menos = d * d - m_mais
    if m_mais < 0 or m_menos < 0:
        return None
    return (m_mais, m_menos)


def grau_admissivel(d: int) -> bool:
    return multiplicidades(d) is not None


def graus_admissiveis(ate: int) -> list[int]:
    """Varre d de 1 ate `ate` e devolve os que a algebra deixa passar."""
    return [d for d in range(1, ate + 1) if grau_admissivel(d)]


def e_grafo_de_moore(g, d: int, k: int = 2) -> bool:
    """Confere a definicao, do jeito mais burro possivel, direto no grafo.

    Esta e a segunda cabeca: nao usa nada do que a busca sabia enquanto
    construia. Mede grau, conta vertices, mede diametro e, no caso k = 2,
    confere na mao que todo par nao adjacente tem exatamente um vizinho comum
    e que nao existe triangulo.
    """
    n = len(g)
    if n != ordem_de_moore(d, k):
        return False
    if not e_regular(g, d):
        return False
    if diametro(g) != k:
        return False
    if k != 2:
        return True
    if d >= 3 and cintura(g) != 5:
        return False
    for u in range(n):
        for v in range(u + 1, n):
            adjacente = (g[u] >> v) & 1
            comuns = vizinhos_comuns(g, u, v)
            if adjacente and comuns != 0:
                return False
            if not adjacente and comuns != 1:
                return False
    return True


def petersen():
    """O grafo de Petersen pela definicao de Kneser: pares de um conjunto de 5.

    Dois vertices sao ligados quando os pares nao tem elemento em comum. Nao
    tem nada a ver com o jeito que a busca constroi, e e exatamente por isso
    que serve de juiz: se a busca achar outro grafo, os dois nao vao casar.
    """
    from itertools import combinations

    from .nucleo import grafo_de_arestas

    pares = list(combinations(range(5), 2))
    arestas = []
    for a in range(10):
        for b in range(a + 1, 10):
            if not set(pares[a]) & set(pares[b]):
                arestas.append((a, b))
    return grafo_de_arestas(10, arestas)


def hoffman_singleton():
    """O grafo de Hoffman-Singleton pela construcao de Robertson, de 1964.

    Cinco pentagonos P_h e cinco pentagramas Q_k, todos com os vertices
    numerados em Z_5; dentro de P_h liga-se i com i+1, dentro de Q_k liga-se j
    com j+2, e entre eles liga-se P_h[i] a Q_k[h*k + i mod 5].

    Sai um grafo de 50 vertices, 7-regular. Que ele tenha cintura 5 e diametro
    2 nao esta escrito em lugar nenhum deste arquivo: quem confere e o
    `e_grafo_de_moore`, e e a conferencia que vale.
    """
    from .nucleo import grafo_de_arestas

    def p(h, i):
        return h * 5 + i

    def q(k, j):
        return 25 + k * 5 + j

    arestas = []
    for h in range(5):
        for i in range(5):
            arestas.append((p(h, i), p(h, (i + 1) % 5)))
            arestas.append((q(h, i), q(h, (i + 2) % 5)))
    for h in range(5):
        for k in range(5):
            for i in range(5):
                arestas.append((p(h, i), q(k, (h * k + i) % 5)))
    return grafo_de_arestas(50, sorted(set(tuple(sorted(e)) for e in arestas)))
