import random


def insercao(lista):
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > atual:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = atual
    return lista


def intercalar(esquerda, direita):
    saida = []
    i = 0
    j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            saida.append(esquerda[i])
            i += 1
        else:
            saida.append(direita[j])
            j += 1
    saida.extend(esquerda[i:])
    saida.extend(direita[j:])
    return saida


def intercalacao(lista):
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esquerda = intercalacao(lista[:meio])
    direita = intercalacao(lista[meio:])
    return intercalar(esquerda, direita)


def hibrida(lista, corte=20):
    if len(lista) < corte:
        return insercao(lista)
    if len(lista) <= 1:
        return lista

    pivo = random.choice(lista)
    menores = []
    iguais = []
    maiores = []

    for x in lista:
        if x < pivo:
            menores.append(x)
        elif x == pivo:
            iguais.append(x)
        else:
            maiores.append(x)

    return hibrida(menores, corte) + iguais + hibrida(maiores, corte)


def rapida(lista):
    if len(lista) <= 1:
        return lista

    pivo = random.choice(lista)
    menores = []
    iguais = []
    maiores = []

    for x in lista:
        if x < pivo:
            menores.append(x)
        elif x == pivo:
            iguais.append(x)
        else:
            maiores.append(x)

    return rapida(menores) + iguais + rapida(maiores)


def contagem(lista):
    if len(lista) == 0:
        return lista
    menor = min(lista)
    maior = max(lista)
    # um contador para cada valor da faixa: se a faixa for enorme, a memória estoura
    contador = [0] * (maior - menor + 1)
    for x in lista:
        contador[x - menor] += 1
    saida = []
    for i in range(len(contador)):
        saida.extend([i + menor] * contador[i])
    return saida


def base(lista):
    if len(lista) == 0:
        return lista
    # desloca tudo para começar em 0, assim funciona com negativos
    menor = min(lista)
    numeros = [x - menor for x in lista]
    maior = max(numeros)
    divisor = 1
    while maior // divisor > 0:
        baldes = [[] for _ in range(10)]
        for x in numeros:
            baldes[(x // divisor) % 10].append(x)
        numeros = []
        for balde in baldes:
            numeros.extend(balde)
        divisor *= 10
    return [x + menor for x in numeros]
