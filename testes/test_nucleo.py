# -*- coding: utf-8 -*-
"""O nucleo medido contra grafos cujo resultado se sabe de cabeca."""
from moore.juiz import hoffman_singleton, petersen
from moore.nucleo import (INFINITO, arestas, cintura, conexo, diametro,
                          distancias, e_regular, grafo_de_arestas, graus,
                          sao_isomorfos, vizinhos_comuns)


def ciclo(n):
    return grafo_de_arestas(n, [(i, (i + 1) % n) for i in range(n)])


def completo(n):
    return grafo_de_arestas(n, [(u, v) for u in range(n) for v in range(u + 1, n)])


def caminho(n):
    return grafo_de_arestas(n, [(i, i + 1) for i in range(n - 1)])


def test_arestas_voltam_como_entraram():
    g = grafo_de_arestas(4, [(0, 1), (2, 3), (1, 2)])
    assert arestas(g) == [(0, 1), (1, 2), (2, 3)]


def test_laco_e_recusado():
    try:
        grafo_de_arestas(3, [(1, 1)])
    except ValueError:
        return
    raise AssertionError("laco passou")


def test_graus_do_completo():
    assert graus(completo(6)) == [5] * 6
    assert e_regular(completo(6), 5)
    assert not e_regular(completo(6), 4)


def test_distancias_no_caminho():
    g = caminho(5)
    assert distancias(g, 0) == [0, 1, 2, 3, 4]
    assert distancias(g, 2) == [2, 1, 0, 1, 2]


def test_desconexo_fica_em_infinito():
    g = grafo_de_arestas(4, [(0, 1), (2, 3)])
    assert distancias(g, 0)[2] == INFINITO
    assert not conexo(g)
    assert diametro(g) == INFINITO


def test_diametro_e_cintura_conhecidos():
    assert diametro(completo(7)) == 1
    assert cintura(completo(7)) == 3
    assert diametro(ciclo(9)) == 4
    assert cintura(ciclo(9)) == 9
    assert diametro(caminho(6)) == 5
    assert cintura(caminho(6)) == INFINITO


def test_petersen_pela_definicao_de_kneser():
    g = petersen()
    assert len(g) == 10
    assert e_regular(g, 3)
    assert diametro(g) == 2
    assert cintura(g) == 5
    assert len(arestas(g)) == 15


def test_hoffman_singleton_pela_construcao_de_robertson():
    g = hoffman_singleton()
    assert len(g) == 50
    assert e_regular(g, 7)
    assert diametro(g) == 2
    assert cintura(g) == 5
    assert len(arestas(g)) == 175


def test_vizinhos_comuns_em_grafo_de_moore():
    g = petersen()
    for u in range(10):
        for v in range(u + 1, 10):
            esperado = 0 if (g[u] >> v) & 1 else 1
            assert vizinhos_comuns(g, u, v) == esperado


def test_isomorfismo_reconhece_renumeracao():
    g = petersen()
    troca = {i: (i * 3 + 7) % 10 for i in range(10)}
    h = grafo_de_arestas(10, [(troca[u], troca[v]) for u, v in arestas(g)])
    assert sao_isomorfos(g, h)


def test_isomorfismo_separa_os_dois_cubicos_de_seis_vertices():
    # K_{3,3} e o prisma triangular: os dois sao cubicos com 6 vertices, e um
    # tem triangulo e o outro nao.
    k33 = grafo_de_arestas(6, [(u, v) for u in range(3) for v in range(3, 6)])
    prisma = grafo_de_arestas(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5),
                                  (5, 3), (0, 3), (1, 4), (2, 5)])
    assert e_regular(k33, 3) and e_regular(prisma, 3)
    assert not sao_isomorfos(k33, prisma)
    assert cintura(k33) == 4
    assert cintura(prisma) == 3
