from metodos import insercao, hibrida, contagem, base

# limites tirados das medições do RELATORIO.md
LIMITE_PEQUENA = 10
LIMITE_DESCIDAS = 0.1      # até 10% de descidas ainda conta como quase ordenada
LIMITE_CONTAGEM = 2        # faixa de até 2 vezes o tamanho da lista
LIMITE_BASE_TAMANHO = 1000  # base só compensa em lista grande
LIMITE_BASE_FAIXA = 10**9   # até 10 dígitos


def escolher(lista):
    n = len(lista)
    if n <= LIMITE_PEQUENA:
        return insercao

    # uma passada só: menor, maior e quantas vezes o vizinho é menor que o anterior
    menor = lista[0]
    maior = lista[0]
    descidas = 0
    for i in range(1, n):
        x = lista[i]
        if x < menor:
            menor = x
        elif x > maior:
            maior = x
        if x < lista[i - 1]:
            descidas += 1

    if descidas <= n * LIMITE_DESCIDAS:
        return insercao
    faixa = maior - menor + 1
    # a contagem cria um vetor do tamanho da faixa, então só usa se a faixa for pequena
    if faixa <= n * LIMITE_CONTAGEM:
        return contagem
    if n >= LIMITE_BASE_TAMANHO and faixa <= LIMITE_BASE_FAIXA:
        return base
    return hibrida


def ordenar(lista):
    metodo = escolher(lista)
    return metodo(lista)
