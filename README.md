# Escolhedor de Ordenadores

Trabalho de Estrutura de Dados Avançadas: um `ordenar(v)` que olha a lista, escolhe sozinho o método de ordenação e executa.

Só precisa de Python 3 (testado com 3.14). Nenhuma biblioteca extra.

## Arquivos

| arquivo | o que tem |
|---|---|
| `metodos.py` | os seis métodos: inserção, intercalação, rápida (pivô aleatório), híbrida, contagem e base |
| `escolhedor.py` | `escolher(v)` e `ordenar(v)` |
| `testes.py` | testes com lista vazia, um elemento, todos iguais, já ordenada, invertida e negativos |
| `medir.py` | gera a tabela dos quatro cenários contra os seis métodos (e o cenário em que o escolher erra) |
| `calibrar.py` | experimentos que deram origem aos limites usados no `escolher` |
| `RELATORIO.md` | resultados e discussão |

## Como refazer as medições

```bash
python3 testes.py     # roda os testes
python3 medir.py      # tabela dos cenários (~10 s)
python3 calibrar.py   # tabelas usadas para definir as regras (~2 s)
```

O `medir.py` e o `calibrar.py` usam semente fixa (`random.seed(2026)`), então as listas são sempre as mesmas. Os tempos mudam de máquina para máquina, mas quem ganha cada cenário deve continuar o mesmo.

Para mudar o tamanho das listas, altere `N` no começo do `medir.py`.
