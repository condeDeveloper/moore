# -*- coding: utf-8 -*-
"""Os numeros do README, presos aqui.

Se a busca mudar e um numero mudar, este arquivo quebra antes de o README
mentir. Nenhum valor daqui foi estimado: todos sairam do
`ferramentas/medidor.py`.

O grau 7, que custa minutos, mora no `test_pesados.py`.
"""
from moore.medidas import (admissiveis, classes, tabela_cotas, tabela_graus,
                           tabela_podas)


def test_tabela_de_cotas():
    esperado = {
        2: [5, 7, 9, 11],
        3: [10, 22, 46, 94],
        4: [17, 53, 161, 485],
        5: [26, 106, 426, 1706],
        6: [37, 187, 937, 4687],
        7: [50, 302, 1814, 10886],
    }
    for d, valores in tabela_cotas(diametros=(2, 3, 4, 5)):
        assert valores == esperado[d], d


def test_admissiveis_ate_um_milhao():
    assert admissiveis(1000000) == [1, 2, 3, 7, 57]


def test_tabela_de_graus_ate_6():
    linhas = {l[0]: l for l in tabela_graus(graus=(1, 2, 3, 4, 5, 6))}
    assert linhas[1][1:6] == (2, True, (1, 0), 0, 0)  # algebra passa, grafo nao existe
    assert linhas[2][1:6] == (5, True, (2, 2), 1, 0)
    assert linhas[3][1:6] == (10, True, (4, 5), 1, 3)
    assert linhas[4][1:6] == (17, False, None, 0, 29)
    assert linhas[5][1:6] == (26, False, None, 0, 526)
    assert linhas[6][1:6] == (37, False, None, 0, 62749)


def test_o_juiz_aprova_todas_as_solucoes_achadas_ate_6():
    for linha in tabela_graus(graus=(2, 3)):
        assert linha[6] is True
    for linha in tabela_graus(graus=(1, 4, 5, 6)):
        assert linha[6] is None


def test_tabela_de_podas():
    linhas = {l[0]: l[1:] for l in tabela_podas(graus=(3, 4, 5))}
    assert linhas[3] == (3, 3, 4)
    assert linhas[4] == (29, 76, 678)
    assert linhas[5] == (526, 377122, 540476052)


def test_a_poda_de_quadrado_vale_717_vezes_no_grau_5():
    com, so_tri, sem = 526, 377122, 540476052
    assert round(so_tri / com, 1) == 717.0
    assert round(sem / com, 1) == 1027521.0


def test_a_arvore_sem_poda_do_grau_6_passa_de_um_sextilhao():
    linha = dict((l[0], l[1:]) for l in tabela_podas(graus=(6,), teto=1000))
    com, so_tri, sem = linha[6]
    assert com == 62749
    assert so_tri == -1001  # negativo e a marca de 'passa de'
    assert sem == 1696899449916258453280


def test_petersen_e_unico_entre_as_solucoes_do_grau_3():
    assert classes(3) == 1
