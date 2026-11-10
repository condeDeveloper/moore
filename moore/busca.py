# -*- coding: utf-8 -*-
"""A busca: constroi grafos de Moore de diametro 2 aresta por aresta.

Nao consulta o `juiz.py` em momento nenhum. O que ela sabe e a forma que um
grafo de Moore (d, 2) e obrigado a ter, e essa forma e quase toda a resposta:

    raiz 0, com d vizinhos 1..d;
    cada vizinho i leva outros d-1 vertices, o bloco B_i, de modo que a camada
    2 tem d*(d-1) vertices e o total fecha em d*d + 1;
    um vertice de B_i nao se liga a outro de B_i (seria triangulo com i);
    entao cada vertice da camada 2 precisa de exatamente um vizinho em cada
    bloco que nao e o seu, e entre dois blocos ha um emparelhamento perfeito.

Sobra escolher, para cada par de blocos, qual permutacao casa um com o outro.
E essa escolha que a busca varre.

Duas podas, e as duas sao a mesma coisa dita de dois jeitos: o grafo nao pode
ter triangulo nem quadrado, isto e, cintura 5. Ao ligar u a v:

    triangulo  -> u e v ja tem vizinho comum;
    quadrado   -> algum vizinho de u ja e vizinho de algum vizinho de v.

Quem passa pelas duas ate o fim e grafo de Moore de graca: com cintura 5 e grau
d, a vizinhanca a distancia 2 de qualquer vertice tem 1 + d + d*(d-1) vertices
todos distintos, que e o numero de vertices do grafo. Diametro 2 sem medir.

Normalizacao: o t-esimo vertice de B_1 e ligado ao t-esimo de cada outro bloco.
Isso nao perde solucao nenhuma, porque renumerar os vertices dentro de um bloco
da outro desenho do mesmo grafo; so gasta essa liberdade de uma vez.
"""
from __future__ import annotations

from .nucleo import grafo_de_arestas


class Resultado:
    """O que a varredura de um grau devolve.

    `nos` e o numero de vezes que a busca escolheu um parceiro, inclusive as
    escolhas que a poda derrubou no instante seguinte: e a medida de quanto
    custou a resposta, e e o unico numero daqui que nao da para prever no papel.
    """

    def __init__(self, d: int):
        self.d = d
        self.ordem = d * d + 1
        self.nos = 0
        self.podas_triangulo = 0
        self.podas_quadrado = 0
        self.solucoes: list = []

    def __repr__(self) -> str:
        return "Resultado(d=%d, ordem=%d, solucoes=%d, nos=%d)" % (
            self.d, self.ordem, len(self.solucoes), self.nos)


def _cintura_cinco(g) -> bool:
    """Sem quadrado e sem triangulo, conferido direto nas arestas."""
    n = len(g)
    for u in range(n):
        for v in range(u + 1, n):
            comuns = bin(g[u] & g[v]).count("1")
            if (g[u] >> v) & 1:
                if comuns:
                    return False
            elif comuns > 1:
                return False
    return True


def _blocos(d: int):
    """Os indices de cada bloco da camada 2. B[i] para i de 1 a d."""
    blocos = {}
    proximo = d + 1
    for i in range(1, d + 1):
        blocos[i] = list(range(proximo, proximo + d - 1))
        proximo += d - 1
    return blocos


def nos_sem_poda(d: int) -> int:
    """Quantos nos a MESMA arvore teria sem poda nenhuma.

    O denominador honesto de uma busca podada nao e o numero de folhas do
    espaco (isso compara no com folha e infla a conta): e o numero de NOS que a
    arvore inteira teria, soma dos produtos parciais de ramificacao, visitados
    na mesma ordem.

    Na tarefa do t-esimo vertice de um bloco contra um bloco posterior sobram
    d-1-t parceiros livres, entao os fatores sao conhecidos sem rodar nada.
    """
    if d < 3:
        return 0
    fatores = []
    for i in range(2, d + 1):
        for t in range(d - 1):
            for _ in range(i + 1, d + 1):
                fatores.append(d - 1 - t)
    total = 0
    produto = 1
    for f in fatores:
        produto *= f
        total += produto
    return total


class Estourou(Exception):
    """A busca passou do teto de nos combinado. A medida vira 'passa de N'."""


def varrer(d: int, parar_na_primeira: bool = False,
           poda_quadrado: bool = True, teto: int | None = None) -> Resultado:
    """Varre todos os grafos de Moore (d, 2) sob a normalizacao de blocos.

    `poda_quadrado=False` desliga a segunda poda e deixa so a de triangulo. A
    busca continua correta (o grafo e conferido no fim), e serve para medir
    quanto a poda de quadrado vale.
    """
    r = Resultado(d)
    if d < 1:
        raise ValueError("grau comeca em 1")
    if d == 1:
        # Nao existe, e a algebra do `juiz.py` nao percebe. Um grafo 1-regular
        # conexo e o K2: dois vertices, diametro 1. Para ter diametro 2 faltaria
        # um terceiro vertice, e ai o grau nao seria 1. A derivacao espectral
        # passa porque ela fala de "todo par nao adjacente tem um vizinho
        # comum", e com dois vertices nao existe par nao adjacente nenhum: a
        # condicao e vazia e a conta nao tem sobre o que se apoiar.
        return r
    if d == 2:
        r.solucoes.append(grafo_de_arestas(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]))
        return r

    n = d * d + 1
    blocos = _blocos(d)
    bloco_de = {}
    for i, membros in blocos.items():
        for u in membros:
            bloco_de[u] = i

    adj = [0] * n
    def liga(u, v):
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    for i in range(1, d + 1):
        liga(0, i)
        for u in blocos[i]:
            liga(i, u)

    # Normalizacao: B_1[t] casa com B_j[t] em todos os blocos.
    for t in range(d - 1):
        for j in range(2, d + 1):
            liga(blocos[1][t], blocos[j][t])

    # As tarefas que sobraram: para cada vertice da camada 2 fora de B_1, um
    # parceiro em cada bloco posterior ao seu. Vertice por vertice, e nao par de
    # blocos por par de blocos, porque assim a poda cai mais cedo.
    tarefas = []
    for i in range(2, d + 1):
        for u in blocos[i]:
            for j in range(i + 1, d + 1):
                tarefas.append((u, j))

    def cabe(u: int, v: int) -> bool:
        if adj[u] & adj[v]:
            r.podas_triangulo += 1
            return False
        if not poda_quadrado:
            return True
        vizinhos = adj[u]
        while vizinhos:
            b = vizinhos & -vizinhos
            x = b.bit_length() - 1
            vizinhos ^= b
            if adj[x] & adj[v]:
                r.podas_quadrado += 1
                return False
        return True

    mascara_bloco = {}
    for i, membros in blocos.items():
        m = 0
        for u in membros:
            m |= 1 << u
        mascara_bloco[i] = m

    achou_tudo = [False]

    def passo(k: int):
        if achou_tudo[0]:
            return
        if k == len(tarefas):
            arestas = []
            for u in range(n):
                viz = adj[u] >> (u + 1)
                v = u + 1
                while viz:
                    if viz & 1:
                        arestas.append((u, v))
                    viz >>= 1
                    v += 1
            g = grafo_de_arestas(n, arestas)
            if poda_quadrado or _cintura_cinco(g):
                r.solucoes.append(g)
            if parar_na_primeira and r.solucoes:
                achou_tudo[0] = True
            return
        u, j = tarefas[k]
        for v in blocos[j]:
            if adj[u] & (1 << v):
                continue
            # v ja pode ter parceiro no bloco de u
            if adj[v] & mascara_bloco[bloco_de[u]]:
                continue
            r.nos += 1
            if teto is not None and r.nos > teto:
                raise Estourou(r.nos)
            if not cabe(u, v):
                continue
            liga(u, v)
            passo(k + 1)
            adj[u] &= ~(1 << v)
            adj[v] &= ~(1 << u)
            if achou_tudo[0]:
                return

    passo(0)
    return r
