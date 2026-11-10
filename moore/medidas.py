# -*- coding: utf-8 -*-
"""As tabelas do README, calculadas aqui e em lugar nenhum mais.

Nenhum numero deste projeto foi digitado a mao: o `ferramentas/medidor.py`
imprime o que sai daqui, e o `testes/test_medidas.py` prende os mesmos valores.
Se a busca mudar e um numero mudar, o teste quebra antes do README mentir.

A varredura completa do grau 7 custa dezenas de milhoes de nos, entao ela roda
UMA VEZ por processo e fica guardada: as tabelas que precisam dela leem o mesmo
resultado.
"""
from __future__ import annotations

from .busca import Estourou, nos_sem_poda, varrer
from .juiz import e_grafo_de_moore, graus_admissiveis, multiplicidades, ordem_de_moore
from .nucleo import classes_de_isomorfismo

GRAUS = (1, 2, 3, 4, 5, 6, 7)

_cache: dict = {}


def varredura(d: int):
    """A varredura completa do grau `d`, calculada uma vez por processo."""
    if d not in _cache:
        _cache[d] = varrer(d)
    return _cache[d]


def tabela_graus(graus=GRAUS):
    """Uma linha por grau: cota, o que a algebra diz, e o que a busca achou.

    Devolve tuplas
    `(d, ordem, admissivel, multiplicidades, solucoes, nos, confere)`, onde
    `confere` e o veredito do juiz sobre a primeira solucao, se houver.
    """
    linhas = []
    for d in graus:
        r = varredura(d)
        m = multiplicidades(d)
        confere = e_grafo_de_moore(r.solucoes[0], d) if r.solucoes else None
        linhas.append((d, ordem_de_moore(d, 2), m is not None, m,
                       len(r.solucoes), r.nos, confere))
    return linhas


def tabela_podas(graus=(3, 4, 5), teto: int | None = None):
    """Quanto cada poda vale, contra a arvore inteira sem poda nenhuma.

    `(d, nos_com_as_duas, nos_so_triangulo, nos_sem_poda)`. Quando a busca sem a
    poda de quadrado passa do teto, o segundo numero sai negativo: e a marca de
    'passa de', e quem imprime trata.
    """
    linhas = []
    for d in graus:
        com = varrer(d).nos
        try:
            so_tri = varrer(d, poda_quadrado=False, teto=teto).nos
        except Estourou as e:
            so_tri = -int(e.args[0])
        linhas.append((d, com, so_tri, nos_sem_poda(d)))
    return linhas


def achar_contra_provar(d: int = 7):
    """O que custa achar UM grafo contra o que custa provar que nao ha outro.

    Devolve `(nos_ate_a_primeira, nos_totais, solucoes)`. A razao entre os dois
    e a pergunta que o livro nao responde: o teorema diz que o grafo e unico,
    nao diz que a unicidade custa milhares de vezes mais que a existencia.
    """
    primeira = varrer(d, parar_na_primeira=True)
    completa = varredura(d)
    return (primeira.nos, completa.nos, len(completa.solucoes))


def tabela_cotas(graus=(2, 3, 4, 5, 6, 7), diametros=(1, 2, 3, 4, 5)):
    """A cota de Moore crua, uma linha por grau e uma coluna por diametro."""
    return [(d, [ordem_de_moore(d, k) for k in diametros]) for d in graus]


def admissiveis(ate: int = 1000000):
    """Os graus que a condicao espectral deixa passar, varrendo d de 1 ate `ate`."""
    return graus_admissiveis(ate)


def classes(d: int):
    """Quantos grafos DIFERENTES ha entre as solucoes do grau `d`."""
    return len(classes_de_isomorfismo(varredura(d).solucoes))
