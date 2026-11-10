# -*- coding: utf-8 -*-
"""Os testes que custam minutos: o grau 7 inteiro.

A varredura completa do grau 7 passa de cem milhoes de nos. Ela roda UMA VEZ
neste arquivo, guardada em `_completa`, e todos os testes daqui leem o mesmo
resultado. Rodar de novo por teste multiplicaria o tempo da bateria por cinco
sem conferir nada a mais.
"""
import pytest

from moore.busca import Estourou, varrer
from moore.juiz import e_grafo_de_moore, hoffman_singleton
from moore.nucleo import cintura, diametro, e_regular, sao_isomorfos

_completa = None


def completa():
    global _completa
    if _completa is None:
        _completa = varrer(7)
    return _completa


def test_grau_7_esgota_o_espaco():
    r = completa()
    assert r.ordem == 50
    assert r.nos == 106541412
    assert len(r.solucoes) == 720


def test_as_720_solucoes_sao_o_mesmo_grafo():
    r = completa()
    primeira = r.solucoes[0]
    assert all(sao_isomorfos(primeira, g) for g in r.solucoes)


def test_o_grafo_achado_e_o_de_robertson():
    assert sao_isomorfos(completa().solucoes[0], hoffman_singleton())


def test_o_juiz_aprova_o_que_a_busca_achou():
    g = completa().solucoes[0]
    assert e_regular(g, 7)
    assert diametro(g) == 2
    assert cintura(g) == 5
    assert e_grafo_de_moore(g, 7)


def test_achar_e_muito_mais_barato_que_provar():
    primeira = varrer(7, parar_na_primeira=True)
    assert primeira.nos == 32567
    razao = completa().nos / primeira.nos
    assert 3200 < razao < 3300


def test_as_podas_do_grau_7():
    r = completa()
    assert r.podas_triangulo == 27125930
    assert r.podas_quadrado == 47301477


def test_grau_6_sem_a_poda_de_quadrado_nao_fecha_em_300_mil_nos():
    with pytest.raises(Estourou):
        varrer(6, poda_quadrado=False, teto=300000)
    assert varrer(6).nos == 62749
