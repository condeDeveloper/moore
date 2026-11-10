# Grafos de Moore

Um grafo de grau `d` e diâmetro `k` não pode ter mais que `1 + d + d(d-1) + ...`
vértices: andando a partir de um vértice qualquer, na primeira camada cabem `d`
vizinhos, na segunda `d(d-1)`, e depois de `k` camadas acabou o diâmetro. Esse
teto é a **cota de Moore**, e os grafos que empatam com ela são os **grafos de
Moore**.

Este repositório varre o caso de diâmetro 2. Para cada grau, dois programas que
não se falam respondem a mesma pergunta:

- uma **busca** que constrói o grafo aresta por aresta, sem saber nada de
  álgebra;
- um **juiz** que decide por autovalores, sem ver um grafo.

Quando os dois concordam, o número vale. Eles concordam em todos os graus menos
um, e o desacordo está na tabela.

Python puro, sem dependência. 48 testes.

```bash
pip install -e ".[dev]"
python -m pytest
python -m moore graus 1000
python -m moore buscar 7
python ferramentas/medidor.py --tudo
```

## A cota de Moore

Quantos vértices cabem, por grau e por diâmetro:

| grau | k=2 | k=3 | k=4 | k=5 |
|---:|---:|---:|---:|---:|
| 2 | 5 | 7 | 9 | 11 |
| 3 | 10 | 22 | 46 | 94 |
| 4 | 17 | 53 | 161 | 485 |
| 5 | 26 | 106 | 426 | 1.706 |
| 6 | 37 | 187 | 937 | 4.687 |
| 7 | 50 | 302 | 1.814 | 10.886 |

## O juiz, que decide sem ver grafo

Um grafo de Moore de grau `d` e diâmetro 2 tem `d²+1` vértices, nenhum triângulo
e exatamente um vizinho comum entre dois vértices não adjacentes. Isso o torna
fortemente regular de parâmetros `(d²+1, d, 0, 1)`, e os autovalores de um grafo
fortemente regular saem de uma equação do segundo grau: `d` e as raízes de
`x² + x - (d-1) = 0`.

As multiplicidades desses autovalores saem de duas equações de traço. Elas contam
autovetores, então **têm de ser inteiras**. Essa é a peneira inteira, e ela não
olha nenhum grafo: recebe o número `d` e devolve sim ou não.

Varrendo `d` de 1 a 1.000.000:

| até | graus que passam |
|---:|---|
| 10 | 1, 2, 3, 7 |
| 100 | 1, 2, 3, 7, 57 |
| 1.000.000 | 1, 2, 3, 7, 57 |

| d | ordem | multiplicidades |
|---:|---:|---|
| 1 | 2 | 1 e 0 |
| 2 | 5 | 2 e 2 |
| 3 | 10 | 4 e 5 |
| 7 | 50 | 21 e 28 |
| 57 | 3.250 | 1.520 e 1.729 |

Um milhão de graus, cinco sobreviventes.

## A busca, que decide sem ver álgebra

A forma de um grafo de Moore (d,2) é quase toda a resposta: uma raiz, `d`
vizinhos, e `d` blocos de `d-1` vértices na camada 2. Dois vértices do mesmo
bloco não podem se ligar (fariam triângulo com o pai), então cada vértice da
camada 2 precisa de **exatamente um** vizinho em cada bloco que não é o seu, e
entre dois blocos há um emparelhamento perfeito. Sobra escolher as permutações, e
é isso que a busca varre.

Duas podas, que são a mesma coisa dita de dois jeitos: sem triângulo e sem
quadrado, isto é, cintura 5. **A busca nunca mede diâmetro.** Quem passa pelas
duas podas até o fim tem diâmetro 2 de graça: com cintura 5 e grau `d`, a
vizinhança a distância 2 de qualquer vértice tem `1 + d + d(d-1)` vértices todos
distintos, que é o grafo inteiro. O juiz mede o diâmetro depois, por fora, e
confirma.

| d | ordem | álgebra | soluções | nós | juiz |
|---:|---:|---|---:|---:|---|
| 1 | 2 | passa | 0 | 0 | — |
| 2 | 5 | passa | 1 | 0 | confere |
| 3 | 10 | passa | 1 | 3 | confere |
| 4 | 17 | proíbe | 0 | 29 | — |
| 5 | 26 | proíbe | 0 | 526 | — |
| 6 | 37 | proíbe | 0 | 62.749 | — |
| 7 | 50 | passa | 720 | 106.541.412 | confere |

Os dois grafos achados foram conferidos contra construções de outra gente e de
outro século: o do grau 3 contra o grafo de Kneser dos pares de `{1..5}`, e o do
grau 7 contra a construção de Robertson de 1964, cinco pentágonos e cinco
pentagramas colados por `h·k + i mod 5`. Os dois casam.

## Quanto cada poda vale

| d | com as duas | só triângulo | árvore sem poda |
|---:|---:|---:|---:|
| 3 | 3 | 3 | 4 |
| 4 | 29 | 76 | 678 |
| 5 | 526 | 377.122 | 540.476.052 |
| 6 | 62.749 | passa de 300.000 | 1.696.899.449.916.258.453.280 |

A última coluna é o número de **nós** que a mesma árvore teria sem poda nenhuma,
visitada na mesma ordem: soma dos produtos parciais de ramificação. Não é o
número de folhas. Comparar nó com folha infla a conta e já me enganou duas vezes
em outro repositório.

## Quatro achados

**1. A álgebra deixa passar cinco graus em um milhão, e três deles têm grafo.**
De `d = 1` a `d = 1.000.000`, só 1, 2, 3, 7 e 57 sobrevivem à exigência de
multiplicidade inteira. A busca confirma o 2 e o 3, confirma o 7 depois de 106
milhões de nós, **derruba o 1** e não alcança o 57, que precisaria de 3.250
vértices e segue em aberto desde 1960.

**2. O grau 1 é o único em que o juiz e a busca discordam, e a busca está certa.**
A álgebra passa porque a condição de que ela parte — "todo par não adjacente tem
exatamente um vizinho comum" — é **vazia** em dois vértices: não existe par não
adjacente. Um grafo 1-regular conexo é o K2, de diâmetro 1, e para ter diâmetro 2
faltaria um terceiro vértice, que estragaria o grau. A peneira espectral não vê
isso porque ela nunca olha o grafo. É o caso em que a segunda cabeça pagou o
preço de existir.

**3. Achar o Hoffman-Singleton custa 0,03% do que custa provar que ele é único.**
A busca encontra o primeiro grafo de 50 vértices em **32.567 nós**. Esgotar o
espaço para garantir que não há outro custa **106.541.412** — **3.271 vezes
mais**. As 720 soluções que sobram da varredura foram testadas uma a uma e são
**todas o mesmo grafo**, em 720 numerações diferentes: o resíduo de simetria que
a normalização de blocos não consumiu.

**4. A poda de quadrado é a que trabalha, e sozinha vale 717 vezes.** No grau 5 a
busca com as duas podas fecha em 526 nós; só com a de triângulo, em 377.122. A
árvore sem poda nenhuma tem 540.476.052 nós, ou seja, as duas juntas cortam
**1.027.521 para 1**. No grau 6 a diferença deixa de ser de grau: com as duas
podas a busca fecha em 62.749 nós, e só com a de triângulo ela passa de 300.000
sem terminar.

## O que as medidas me corrigiram

- **Escrevi 716,9 onde o programa deu 717,0.** Dividi 377.122 por 526 de cabeça
  para preencher o teste e errei no primeiro decimal. O teste quebrou na mesma
  hora, que é exatamente para isso que ele existe. Nenhuma razão deste README foi
  digitada: todas passaram pelo Python antes de entrar no arquivo.
- **Eu esperava que a busca precisasse medir diâmetro.** Não precisa. Cintura 5
  mais grau `d` mais `d²+1` vértices já é diâmetro 2, e a conta cabe em uma
  linha. A busca ficou mais simples depois que eu entendi isso, e o diâmetro
  passou a ser conferência do juiz, não condição da busca.
- **Eu esperava que o grau 1 fosse um caso trivial de acordo.** É o único caso de
  desacordo do projeto. A primeira versão da busca devolvia o K2 como solução
  para diâmetro 2, e o verificador da definição reprovou na mesma rodada —
  `e_grafo_de_moore` mede o diâmetro e viu 1 onde o programa prometia 2. Virou o
  achado número 2.
- **Eu esperava que provar a não existência fosse mais caro que achar.** É, mas
  não onde eu achava: nos graus 4, 5 e 6, onde não existe nada, a busca fecha em
  29, 526 e 62.749 nós. O caro é o grau 7, onde o grafo **existe**: 106 milhões
  de nós para mostrar que ele é um só.
- **O denominador honesto me fez refazer a última coluna.** Minha primeira versão
  contava folhas (o produto de todas as ramificações) e dava um número muito
  maior, comparando coisas diferentes. O número que está na tabela é a soma dos
  produtos parciais: nós contra nós.

## Arquivos

```
moore/nucleo.py    grafo, distância, diâmetro, cintura, isomorfismo
moore/juiz.py      a condição espectral e o verificador da definição
moore/busca.py     o backtracking que constrói os grafos
moore/medidas.py   as tabelas deste README
ferramentas/medidor.py
testes/            48 testes, os pesados separados
```

`juiz.py` não importa `busca.py` e `busca.py` não importa `juiz.py`.
