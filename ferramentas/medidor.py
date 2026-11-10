# -*- coding: utf-8 -*-
"""Imprime as tabelas que vao para o README. Nenhum numero sai daqui a mao.

    python ferramentas/medidor.py          tudo menos o grau 7 completo
    python ferramentas/medidor.py --tudo   inclui a varredura do grau 7

A varredura completa do grau 7 passa de cem milhoes de nos e leva minutos, por
isso fica atras de um sinalizador. O resto roda em segundos.
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moore.busca import Estourou, nos_sem_poda, varrer  # noqa: E402
from moore.juiz import graus_admissiveis, multiplicidades, ordem_de_moore  # noqa: E402
from moore.medidas import tabela_graus, varredura  # noqa: E402
from moore.nucleo import cintura, diametro, sao_isomorfos  # noqa: E402

TETO_SEM_QUADRADO = 300000


def titulo(texto: str) -> None:
    print()
    print(texto)
    print("-" * len(texto))


def cotas() -> None:
    titulo("A cota de Moore: quantos vertices cabem")
    print("  grau |" + "".join("  k=%-8d" % k for k in range(1, 6)))
    for d in range(2, 8):
        print("  %-4d |" % d + "".join("  %-8d  " % ordem_de_moore(d, k)
                                       for k in range(1, 6)))


def algebra() -> None:
    titulo("O que a condicao espectral deixa passar")
    for ate in (10, 100, 1000, 100000, 1000000):
        bons = graus_admissiveis(ate)
        print("  d ate %-9d %s" % (ate, ", ".join(str(d) for d in bons)))
    print()
    for d in graus_admissiveis(1000000):
        m = multiplicidades(d)
        print("  d=%-3d ordem %-6d multiplicidades %d e %d"
              % (d, ordem_de_moore(d, 2), m[0], m[1]))


def graus(ate_7: bool) -> None:
    titulo("Grau por grau: algebra contra busca")
    print("  d  ordem  algebra  solucoes  nos          juiz")
    limite = 8 if ate_7 else 7
    for d, ordem, ok, _m, sol, nos, confere in tabela_graus(range(1, limite)):
        print("  %-2d %-6d %-8s %-9d %-12d %s"
              % (d, ordem, "passa" if ok else "proibe", sol, nos,
                 "-" if confere is None else ("confere" if confere else "FALHOU")))


def podas() -> None:
    titulo("Quanto cada poda vale")
    print("  d  com as duas  so triangulo  arvore sem poda")
    for d in (3, 4, 5):
        com = varrer(d).nos
        so_tri = varrer(d, poda_quadrado=False).nos
        print("  %-2d %-12d %-13d %d" % (d, com, so_tri, nos_sem_poda(d)))
    inicio = time.time()
    try:
        r = varrer(6, poda_quadrado=False, teto=TETO_SEM_QUADRADO)
        marca = str(r.nos)
    except Estourou:
        marca = "passa de %d" % TETO_SEM_QUADRADO
    print("  %-2d %-12d %-13s %d  (%.1fs no teto)"
          % (6, varrer(6).nos, marca, nos_sem_poda(6), time.time() - inicio))


def grau7() -> None:
    titulo("Grau 7: achar contra provar")
    inicio = time.time()
    primeira = varrer(7, parar_na_primeira=True)
    t1 = time.time() - inicio
    print("  achar a primeira   %12d nos  (%.1fs)" % (primeira.nos, t1))
    inicio = time.time()
    completa = varredura(7)
    t2 = time.time() - inicio
    print("  esgotar o espaco   %12d nos  (%.1fs)" % (completa.nos, t2))
    print("  razao              %12.1f vezes" % (completa.nos / primeira.nos))
    print("  solucoes           %12d" % len(completa.solucoes))
    g = completa.solucoes[0]
    print("  diametro %s, cintura %s" % (diametro(g), cintura(g)))
    inicio = time.time()
    iguais = sum(1 for h in completa.solucoes if sao_isomorfos(g, h))
    print("  isomorfas a primeira %10d de %d  (%.1fs)"
          % (iguais, len(completa.solucoes), time.time() - inicio))
    print("  podas: triangulo %d, quadrado %d"
          % (completa.podas_triangulo, completa.podas_quadrado))


def main() -> int:
    tudo = "--tudo" in sys.argv
    cotas()
    algebra()
    graus(tudo)
    podas()
    if tudo:
        grau7()
    else:
        print()
        print("(o grau 7 completo so com --tudo)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
