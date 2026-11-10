# -*- coding: utf-8 -*-
"""A busca contra o juiz: dois caminhos que nao se falam.

O ponto destes testes nao e que a busca roda. E que o grafo que ela constroi
aresta por aresta e o MESMO que sai de uma construcao de 1964 feita com
pentagonos e aritmetica modulo 5. Se um dos dois estivesse errado, o
isomorfismo falharia.
"""
from moore.busca import nos_sem_poda, varrer
from moore.juiz import (e_grafo_de_moore, grau_admissivel, hoffman_singleton,
                        ordem_de_moore, petersen)
from moore.nucleo import cintura, diametro, e_regular, sao_isomorfos


def test_grau_1_a_algebra_passa_e_o_grafo_nao_existe():
    # O unico grau em que o juiz e a busca discordam, e a busca esta certa:
    # 1-regular conexo e o K2, de diametro 1.
    assert grau_admissivel(1)
    assert varrer(1).solucoes == []


def test_grau_2_e_o_ciclo_de_cinco():
    r = varrer(2)
    assert len(r.solucoes) == 1
    assert e_grafo_de_moore(r.solucoes[0], 2)


def test_grau_zero_e_recusado():
    try:
        varrer(0)
    except ValueError:
        return
    raise AssertionError("grau 0 passou")


def test_grau_3_acha_o_petersen_e_mais_nada():
    r = varrer(3)
    assert len(r.solucoes) == 1
    assert r.nos == 3
    g = r.solucoes[0]
    assert len(g) == 10
    assert e_regular(g, 3)
    assert sao_isomorfos(g, petersen())


def test_a_busca_nunca_mede_diametro_e_mesmo_assim_sai_diametro_2():
    g = varrer(3).solucoes[0]
    assert diametro(g) == 2
    assert cintura(g) == 5
    assert e_grafo_de_moore(g, 3)


def test_graus_4_5_e_6_fecham_vazios():
    esperado = {4: 29, 5: 526, 6: 62749}
    for d, nos in esperado.items():
        r = varrer(d)
        assert r.solucoes == []
        assert r.nos == nos
        assert not grau_admissivel(d)
        assert r.ordem == ordem_de_moore(d, 2)


def test_grau_7_acha_o_hoffman_singleton():
    r = varrer(7, parar_na_primeira=True)
    assert len(r.solucoes) == 1
    assert r.nos == 32567
    assert sao_isomorfos(r.solucoes[0], hoffman_singleton())


def test_a_poda_de_quadrado_muda_o_tamanho_da_busca_sem_mudar_a_resposta():
    for d in (3, 4, 5):
        com = varrer(d)
        sem = varrer(d, poda_quadrado=False)
        assert len(com.solucoes) == len(sem.solucoes)
        assert sem.nos >= com.nos
    assert varrer(5).nos == 526
    assert varrer(5, poda_quadrado=False).nos == 377122


def test_arvore_sem_poda_nenhuma_e_o_denominador_honesto():
    # Nao e o numero de folhas do espaco: e o numero de NOS que a mesma arvore
    # teria, soma dos produtos parciais de ramificacao.
    assert nos_sem_poda(3) == 4
    assert nos_sem_poda(4) == 678
    assert nos_sem_poda(5) == 540476052
    assert nos_sem_poda(2) == 0
    for d in (3, 4, 5, 6):
        assert nos_sem_poda(d) >= varrer(d).nos


def test_teto_interrompe_sem_mentir():
    from moore.busca import Estourou
    try:
        varrer(6, poda_quadrado=False, teto=1000)
    except Estourou as e:
        assert e.args[0] == 1001
        return
    raise AssertionError("o teto nao pegou")
