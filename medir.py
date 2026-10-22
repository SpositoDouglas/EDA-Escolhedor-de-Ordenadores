import time
from metodos import insercao, intercalacao, hibrida

REPETICOES = 10000

METODOS = {
    "inserção": insercao,
    "intercalação": intercalacao,
    "híbrida": hibrida,
}

CENARIOS = {
    "minúscula": [42, 7, 93, 15, 61, 3, 78, 29, 50, 11],
}


def medir(metodo, lista):
    total = 0
    for _ in range(REPETICOES):
        copia = lista[:]
        inicio = time.perf_counter()
        resultado = metodo(copia)
        total += time.perf_counter() - inicio
        if resultado != sorted(lista):
            print("ERRO:", metodo.__name__, "nao ordenou")
    return total / REPETICOES


def main():
    cabecalho = "| cenário | " + " | ".join(METODOS) + " |"
    print(cabecalho)
    print("|---|" + "---:|" * len(METODOS))

    for nome_cenario, lista in CENARIOS.items():
        linha = f"| {nome_cenario} |"
        for metodo in METODOS.values():
            tempo = medir(metodo, lista)
            linha += f" {tempo * 1000000:.2f} µs |"
        print(linha)


main()
