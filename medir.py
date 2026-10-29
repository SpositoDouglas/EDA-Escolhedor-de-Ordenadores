import random
import time
from metodos import insercao, intercalacao, rapida, hibrida, contagem, base
from escolhedor import escolher, ordenar

random.seed(2026)
N = 5000

METODOS = {
    "inserção": insercao,
    "intercalação": intercalacao,
    "rápida": rapida,
    "híbrida": hibrida,
    "contagem": contagem,
    "base": base,
    "ordenar": ordenar,
}


def quase_ordenada():
    lista = sorted(random.randint(0, 10**9) for _ in range(N))
    for _ in range(N // 100):
        i = random.randrange(N - 1)
        lista[i], lista[i + 1] = lista[i + 1], lista[i]
    return lista


def duas_metades():
    # cada metade ordenada, mas a segunda é toda menor que a primeira
    metade = sorted(random.randint(0, 10**9) for _ in range(N // 2))
    return [x + 10**9 for x in metade] + metade


# nome: (lista, repetições)
CENARIOS = {
    "aleatório chaves grandes": ([random.randint(0, 10**9) for _ in range(N)], 10),
    "faixa estreita": ([random.randint(0, 100) for _ in range(N)], 10),
    "quase ordenado": (quase_ordenada(), 10),
    "minúscula": ([42, 7, 93, 15, 61, 3, 78, 29, 50, 11], 10000),
}

ERRO = {"duas metades (erro)": (duas_metades(), 3)}


def medir(metodo, lista, repeticoes):
    total = 0
    for _ in range(repeticoes):
        copia = lista[:]
        inicio = time.perf_counter()
        resultado = metodo(copia)
        total += time.perf_counter() - inicio
        if resultado != sorted(lista):
            print("ERRO:", metodo.__name__, "nao ordenou")
    return total / repeticoes


def formatar(segundos):
    if segundos >= 0.001:
        return f"{segundos * 1000:.2f} ms"
    return f"{segundos * 1000000:.2f} µs"


def imprimir_tabela(cenarios):
    print("| cenário | " + " | ".join(METODOS) + " | escolheu | custo do escolher |")
    print("|---|" + "---:|" * len(METODOS) + "---|---:|")

    for nome_cenario, (lista, repeticoes) in cenarios.items():
        linha = f"| {nome_cenario} |"
        for metodo in METODOS.values():
            # contagem com chaves grandes criaria um vetor de 10^9 posições
            if metodo is contagem and max(lista) - min(lista) > 10 * len(lista):
                linha += " estoura |"
                continue
            # inserção em lista aleatória grande demora muito, mas mede igual
            tempo = medir(metodo, lista, repeticoes)
            linha += f" {formatar(tempo)} |"
        escolhido = escolher(lista).__name__
        custo = custo_escolher(lista, repeticoes * 10)
        linha += f" {escolhido} | {formatar(custo)} |"
        print(linha)


def custo_escolher(lista, repeticoes):
    total = 0
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        escolher(lista)
        total += time.perf_counter() - inicio
    return total / repeticoes


print(f"N = {N} (exceto a minúscula, que tem 10)\n")
imprimir_tabela(CENARIOS)
print("\nCenário em que o escolher erra:\n")
imprimir_tabela(ERRO)
