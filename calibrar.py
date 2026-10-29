# Experimentos usados para escolher os limites do escolhedor.py
import random
import time
from metodos import insercao, hibrida, contagem, base

random.seed(2026)


def tempo(metodo, lista, repeticoes):
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        metodo(lista[:])
    return (time.perf_counter() - inicio) / repeticoes * 1000000


def mostrar(titulo, metodos, casos, repeticoes):
    print(f"\n{titulo}")
    print("| caso | " + " | ".join(m.__name__ for m in metodos) + " |")
    print("|---|" + "---:|" * len(metodos))
    for nome, lista in casos:
        linha = f"| {nome} |"
        for metodo in metodos:
            linha += f" {tempo(metodo, lista, repeticoes):.1f} µs |"
        print(linha)


# 1. até que tamanho a inserção ganha?
casos = []
for n in [5, 10, 20, 50, 100]:
    casos.append((f"n={n}", [random.randint(0, 10**9) for _ in range(n)]))
mostrar("1. listas pequenas (LIMITE_PEQUENA)", [insercao, hibrida, base], casos, 2000)

# 2. quantas descidas a inserção aguenta?
casos = []
for porcento in [1, 5, 10, 20]:
    lista = sorted(random.randint(0, 10**9) for _ in range(5000))
    for _ in range(5000 * porcento // 100):
        i = random.randrange(4999)
        lista[i], lista[i + 1] = lista[i + 1], lista[i]
    casos.append((f"{porcento}% de trocas", lista))
mostrar("2. quase ordenada, n=5000 (LIMITE_DESCIDAS)", [insercao, hibrida, base], casos, 10)

# 3. até que faixa a contagem ganha?
casos = []
for vezes in [1, 2, 5, 10]:
    casos.append((f"faixa={vezes}n", [random.randint(0, 5000 * vezes) for _ in range(5000)]))
mostrar("3. faixa / tamanho, n=5000 (LIMITE_CONTAGEM)", [contagem, base, hibrida], casos, 10)

# 4. a partir de que tamanho a base ganha da híbrida?
casos = []
for n in [100, 500, 1000, 5000]:
    casos.append((f"n={n}, faixa=10^9", [random.randint(0, 10**9) for _ in range(n)]))
mostrar("4. base x híbrida (LIMITE_BASE_TAMANHO)", [base, hibrida], casos, 20)
