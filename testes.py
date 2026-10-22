import unittest
from metodos import insercao, intercalacao, hibrida

METODOS = [insercao, intercalacao, hibrida]

VAZIA = []
UM_ELEMENTO = [7]
IGUAIS = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
ORDENADA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
INVERTIDA = [30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16,
             15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
NEGATIVOS = [3, -1, -50, 0, 22, -7, 8, -3, 15, -100, 42, -2, 9,
             1, -8, 5, -30, 17, 0, -1, 6, -4, 11, 2, -9]


class TestOrdenacao(unittest.TestCase):

    def verificar(self, lista):
        for metodo in METODOS:
            with self.subTest(metodo=metodo.__name__):
                self.assertEqual(metodo(lista[:]), sorted(lista))

    def test_lista_vazia(self):
        self.verificar(VAZIA)

    def test_um_elemento(self):
        self.verificar(UM_ELEMENTO)

    def test_todos_iguais(self):
        self.verificar(IGUAIS)

    def test_ja_ordenada(self):
        self.verificar(ORDENADA)

    def test_invertida(self):
        self.verificar(INVERTIDA)

    def test_valores_negativos(self):
        self.verificar(NEGATIVOS)

    def test_hibrida_sem_insercao(self):
        for lista in [VAZIA, UM_ELEMENTO, IGUAIS, ORDENADA, INVERTIDA, NEGATIVOS]:
            with self.subTest(lista=lista):
                self.assertEqual(hibrida(lista[:], 1), sorted(lista))


if __name__ == "__main__":
    unittest.main()
