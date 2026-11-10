# -*- coding: utf-8 -*-
"""O juiz sozinho: a cota, a condicao espectral e o verificador da definicao."""
from moore.juiz import (e_grafo_de_moore, grau_admissivel, graus_admissiveis,
                        hoffman_singleton, multiplicidades, ordem_de_moore,
                        petersen)
from moore.nucleo import grafo_de_arestas


def test_cota_de_moore_para_diametro_1_e_o_completo():
    for d in range(1, 8):
        assert ordem_de_moore(d, 1) == d + 1


def test_cota_de_moore_para_grau_2_e_o_ciclo_impar():
    for k in range(1, 7):
        assert ordem_de_moore(2, k) == 2 * k + 1


def test_cota_de_moore_de_diametro_2_e_d_ao_quadrado_mais_um():
    for d in range(3, 60):
        assert ordem_de_moore(d, 2) == d * d + 1
    assert ordem_de_moore(57, 2) == 3250


def test_cota_cresce_como_a_arvore_de_busca():
    # 1 + d + d(d-1) + d(d-1)^2 + ...
    for d in (3, 4, 7):
        for k in range(1, 6):
            esperado = 1 + sum(d * (d - 1) ** i for i in range(k))
            assert ordem_de_moore(d, k) == esperado


def test_grau_e_diametro_tem_de_comecar_em_um():
    for d, k in ((0, 2), (3, 0), (-1, 1)):
        try:
            ordem_de_moore(d, k)
        except ValueError:
            continue
        raise AssertionError("passou com d=%d k=%d" % (d, k))


def test_multiplicidades_conhecidas():
    assert multiplicidades(2) == (2, 2)
    assert multiplicidades(3) == (4, 5)
    assert multiplicidades(7) == (21, 28)
    assert multiplicidades(57) == (1520, 1729)


def test_multiplicidades_somam_d_ao_quadrado():
    for d in graus_admissiveis(1000):
        if d == 1:
            continue
        m_mais, m_menos = multiplicidades(d)
        assert m_mais + m_menos == d * d


def test_a_algebra_proibe_os_graus_que_a_busca_vai_recusar():
    for d in (4, 5, 6, 8, 9, 10, 11):
        assert not grau_admissivel(d)
        assert multiplicidades(d) is None


def test_so_cinco_graus_passam_ate_um_milhao():
    assert graus_admissiveis(1000000) == [1, 2, 3, 7, 57]
    assert graus_admissiveis(1000) == [1, 2, 3, 7, 57]
    assert graus_admissiveis(50) == [1, 2, 3, 7]
    assert graus_admissiveis(10) == [1, 2, 3, 7]


def test_juiz_aprova_os_dois_grafos_que_existem():
    assert e_grafo_de_moore(petersen(), 3)
    assert e_grafo_de_moore(hoffman_singleton(), 7)
    c5 = grafo_de_arestas(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
    assert e_grafo_de_moore(c5, 2)


def test_juiz_recusa_grau_errado_e_ordem_errada():
    g = petersen()
    assert not e_grafo_de_moore(g, 4)
    k4 = grafo_de_arestas(4, [(u, v) for u in range(4) for v in range(u + 1, 4)])
    assert not e_grafo_de_moore(k4, 3)
    assert e_grafo_de_moore(k4, 3, k=1)


def test_juiz_recusa_cubico_de_dez_vertices_que_nao_e_petersen():
    # Prisma pentagonal: cubico, 10 vertices, mas tem quadrado e diametro 3.
    arestas = [(i, (i + 1) % 5) for i in range(5)]
    arestas += [(5 + i, 5 + (i + 1) % 5) for i in range(5)]
    arestas += [(i, 5 + i) for i in range(5)]
    g = grafo_de_arestas(10, arestas)
    assert not e_grafo_de_moore(g, 3)
