# Relatório: Escolhedor de Ordenadores

Medições feitas com `python3 medir.py` (Python 3.14, Linux). Listas de N = 5000 elementos, exceto a minúscula (10 elementos). Cada tempo é a média de 10 execuções (10 000 na minúscula), sempre ordenando uma cópia da mesma lista.

## 1. Tabela: quatro cenários × seis métodos

| cenário | inserção | intercalação | rápida | híbrida | contagem | base | **ordenar** | escolheu | custo do escolher |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| aleatório chaves grandes | 300.42 ms | 5.71 ms | 3.32 ms | 2.58 ms | estoura | **2.26 ms** | 2.55 ms | base | 321.19 µs |
| faixa estreita | 293.90 ms | 5.51 ms | 940.54 µs | 952.28 µs | **196.82 µs** | 690.31 µs | 514.82 µs | contagem | 318.44 µs |
| quase ordenado | **325.28 µs** | 3.88 ms | 3.10 ms | 1.88 ms | estoura | 2.12 ms | 593.61 µs | insercao | 264.46 µs |
| minúscula | **1.48 µs** | 4.89 µs | 3.14 µs | 1.52 µs | 6.88 µs | 2.74 µs | 1.53 µs | insercao | 0.09 µs |

Como foram gerados os cenários:

- **aleatório chaves grandes**: 5000 inteiros aleatórios entre 0 e 10⁹.
- **faixa estreita**: 5000 inteiros aleatórios entre 0 e 100.
- **quase ordenado**: 5000 inteiros entre 0 e 10⁹ já ordenados, com 50 trocas de vizinhos (1%).
- **minúscula**: `[42, 7, 93, 15, 61, 3, 78, 29, 50, 11]`.

"estoura" = não rodamos a contagem porque a faixa é de 10⁹, o que exigiria um vetor de um bilhão de contadores (~8 GB). Testamos sem querer durante o trabalho e o programa travou tentando alocar o vetor.

### Somando os quatro cenários

| método fixo | tempo total |
|---|---:|
| inserção | 594.65 ms |
| intercalação | 15.10 ms |
| rápida | 7.36 ms |
| híbrida | 5.41 ms |
| base | 5.07 ms |
| contagem | não termina (estoura) |
| **ordenar** | **3.66 ms** |

O `ordenar` não é o mais rápido em nenhum cenário isolado (ele sempre paga o custo do `escolher` em cima do melhor método), mas **nenhum método fixo chega perto dele no conjunto**: o melhor fixo (base) gasta 39% a mais, e a contagem e a inserção são desastrosas em pelo menos um cenário.

## 2. Quem venceu cada cenário, e por quê

- **Aleatório com chaves grandes → base.** Com faixa de 10⁹ a base faz 10 passadas (uma por dígito), e cada passada só faz uma conta e um `append`. A híbrida faz cerca de log₂(5000) ≈ 12 níveis de partição, cada um com comparações e criação de listas novas, e por isso fica um pouco atrás. A inserção é O(n²) (300 ms!) e a contagem nem dá para rodar.
- **Faixa estreita → contagem.** Com só 101 valores possíveis, a contagem faz uma passada para contar e depois 101 `extend`. É O(n + faixa), praticamente linear. Ela fica 3,5× à frente da base e 5× à frente da híbrida.
- **Quase ordenado → inserção.** A inserção custa O(n + inversões). Cada troca de vizinhos cria só uma inversão, então ela praticamente só percorre a lista uma vez. Os outros métodos não aproveitam que a lista já está quase pronta e pagam o O(n log n) inteiro.
- **Minúscula → inserção (empatada com a híbrida).** Com 10 elementos não compensa recursão nem criar listas auxiliares. A híbrida empata porque, com menos de 20 elementos, ela mesma chama a inserção. A contagem e a base perdem porque têm custo fixo (criar o vetor de contadores e os 10 baldes) que não se paga numa lista tão pequena.

## 3. Regras do `escolher` e de onde vieram

```python
if n <= 10:                           return insercao
# uma única passada calcula menor, maior e descidas (v[i] < v[i-1])
if descidas <= 10% de n:              return insercao
if faixa <= 2 * n:                    return contagem
if n >= 1000 and faixa <= 10**9:      return base
return hibrida
```

Os números vieram do `calibrar.py` (rode `python3 calibrar.py` para ver as tabelas completas):

| regra | evidência (calibrar.py) |
|---|---|
| `n <= 10` → inserção | n=5: inserção 0.3 µs = híbrida 0.3 µs; n=10: 1.5 µs = 1.5 µs; n=20 a híbrida já ganha (4.6 vs 6.0 µs). Até 10 a inserção não perde e evita até o custo da passada do `escolher`. |
| `descidas <= 10%` → inserção | com 1%, 5%, 10% e até 20% de trocas a inserção ficou entre 327 e 374 µs, contra ~1900 µs da híbrida. Usamos 10% para ter folga. |
| `faixa <= 2n` → contagem | faixa = n: contagem 710 µs vs base 1143 µs; faixa = 2n: 1114 vs 1179 (quase empate); faixa = 5n: a base já ganha (1338 vs 2231). |
| `n >= 1000` e `faixa <= 10⁹` → base | n=100: base 54 vs híbrida 31 µs; n=1000: 446 vs 428 (empate); n=5000: 2137 vs 2575. A base só compensa em lista grande. O limite de 10⁹ é porque acima disso ela precisaria de mais passadas e não medimos. |
| senão → híbrida | é o melhor método de comparação em todas as tabelas: sempre O(n log n), sem precisar de faixa pequena. |

A ordem importa: o teste de quase ordenado vem antes da contagem porque a inserção numa lista quase ordenada é ainda mais barata. A contagem só é escolhida quando a faixa é no máximo 2n, ou seja, o vetor de contadores nunca é maior que o dobro da própria lista. Assim **a memória nunca estoura**: é isso que o enunciado pedia para prever.

## 4. Quanto custa o `escolher`, e se compensa

O `escolher` percorre a lista **uma vez só**, calculando menor, maior e descidas no mesmo `for` (não usamos `min()` e `max()` separados para não passar três vezes). Para listas de até 10 elementos ele nem olha os dados.

| cenário | custo do escolher | ordenar | parte do tempo gasta escolhendo |
|---|---:|---:|---:|
| aleatório chaves grandes | 321 µs | 2.55 ms | 13% |
| faixa estreita | 318 µs | 515 µs | 62% |
| quase ordenado | 264 µs | 594 µs | 45% |
| minúscula | 0.09 µs | 1.53 µs | 6% |

É caro: cerca de 60 ns por elemento, porque é um laço em Python puro, e às vezes custa mais do que o próprio método escolhido (a contagem leva 197 µs e escolher leva 318 µs).

**Mesmo assim compensa**, porque o erro de escolher o método errado é muito maior que o custo de escolher:

- na faixa estreita, pagar 318 µs evita a híbrida (952 µs): o ordenar sai 1,8× mais rápido que ela;
- no quase ordenado, pagar 264 µs evita a híbrida (1.88 ms): sai 3,2× mais rápido;
- no aleatório, perde 13% para a base fixa. É o preço do seguro;
- no total dos quatro cenários o ordenar gasta 3.66 ms contra 5.07 ms do melhor método fixo.

Se o `escolher` percorresse a lista duas vezes (por exemplo, uma passada para faixa e outra para descidas), o custo subiria para ~600 µs e, na faixa estreita, o ordenar passaria de 515 µs para ~800 µs, quase sem vantagem sobre a híbrida fixa (952 µs). Por isso a passada é única.

## 5. Um cenário em que ele erra

**Duas metades ordenadas, com a segunda menor que a primeira**, por exemplo `[1001, 1002, ..., 2000, 1, 2, ..., 1000]` (no `medir.py`: 2500 + 2500 elementos com chaves até 2·10⁹).

| cenário | inserção | intercalação | rápida | híbrida | contagem | base | ordenar | escolheu |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| duas metades | 343.25 ms | 3.98 ms | 3.58 ms | **2.28 ms** | estoura | 2.84 ms | 365.76 ms | insercao |

A lista tem **uma única descida** (na emenda das metades), então o `escolher` acha que está quase ordenada e escolhe a inserção. Só que cada elemento da segunda metade precisa andar 2500 posições para trás: são 2500 × 2500 ≈ 6 milhões de deslocamentos, o pior caso O(n²) da inserção. O ordenar fica **160× mais lento** que a híbrida.

O problema é que "descidas" mede bagunça **local** (vizinhos fora de ordem), mas o custo da inserção depende das **inversões**, que medem a bagunça **global**. Contar inversões de verdade custaria O(n log n), o mesmo que ordenar. Uma correção barata seria também olhar quanto cada descida "desce" (`v[i-1] - v[i]`) comparado com a faixa: uma descida enorme indica um bloco fora do lugar. Não implementamos para manter o escolher simples.

Outra limitação: a contagem e a base só funcionam com **inteiros**. O escolher assume que a lista é de inteiros (como em todos os cenários do trabalho); com `float` ou texto ele quebraria.

## Testes

`python3 testes.py` roda todos os seis métodos e o `ordenar` com: lista vazia, um elemento, todos iguais, já ordenada, invertida e valores negativos. Também testa se o `escolher` devolve o método esperado em casos simples e se ele nunca escolhe a contagem quando a faixa é grande.
