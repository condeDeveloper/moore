# -*- coding: utf-8 -*-
"""Linha de comando: `python -m moore <comando>`.

    graus [ate]     os graus que a condicao espectral deixa passar
    buscar <d>      varre o grau d e conta solucoes, classes e nos
    cota <d> <k>    a cota de Moore para grau d e diametro k
    tabela          a tabela de graus, do jeito que vai para o README
"""
from __future__ import annotations

import sys

from .juiz import e_grafo_de_moore, graus_admissiveis, multiplicidades, ordem_de_moore
from .medidas import tabela_graus
from .nucleo import cintura, classes_de_isomorfismo, diametro
from .busca import varrer


def _graus(args) -> int:
    ate = int(args[0]) if args else 1000
    bons = graus_admissiveis(ate)
    print("graus com multiplicidade inteira, de 1 a %d: %s"
          % (ate, ", ".join(str(d) for d in bons)))
    for d in bons:
        print("  d=%-4d ordem=%-6d multiplicidades=%s"
              % (d, ordem_de_moore(d, 2), multiplicidades(d)))
    return 0


def _buscar(args) -> int:
    if not args:
        print("falta o grau", file=sys.stderr)
        return 2
    d = int(args[0])
    r = varrer(d)
    print("grau %d, ordem %d" % (d, r.ordem))
    print("  nos visitados      %d" % r.nos)
    print("  podas de triangulo %d" % r.podas_triangulo)
    print("  podas de quadrado  %d" % r.podas_quadrado)
    print("  solucoes           %d" % len(r.solucoes))
    if r.solucoes:
        g = r.solucoes[0]
        print("  classes            %d" % len(classes_de_isomorfismo(r.solucoes)))
        print("  diametro %s, cintura %s, juiz diz %s"
              % (diametro(g), cintura(g), e_grafo_de_moore(g, d)))
    return 0


def _cota(args) -> int:
    if len(args) < 2:
        print("faltam grau e diametro", file=sys.stderr)
        return 2
    d, k = int(args[0]), int(args[1])
    print("cota de Moore para grau %d e diametro %d: %d vertices"
          % (d, k, ordem_de_moore(d, k)))
    return 0


def _tabela(args) -> int:
    print("  d  ordem  algebra  solucoes  nos")
    for d, ordem, ok, _m, sol, nos, _c in tabela_graus():
        print("  %-2d %-6d %-8s %-9d %d"
              % (d, ordem, "passa" if ok else "proibe", sol, nos))
    return 0


COMANDOS = {"graus": _graus, "buscar": _buscar, "cota": _cota, "tabela": _tabela}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in COMANDOS:
        print(__doc__)
        return 0 if not argv else 2
    return COMANDOS[argv[0]](argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
