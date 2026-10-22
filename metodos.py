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
