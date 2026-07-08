"""
test_algorithms.py
==================
Testes unitários com pytest para:
    - BinarySearchTree (BST)
    - Força Bruta
    - Dijkstra

Execução: pytest tests/test_algorithms.py -v

Global Solution 2026 — FIAP | Disciplina: Estruturas de Dados e Algoritmos
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from data_structures import (
    BinarySearchTree, Grafo, criar_vertice,
    IDX_NOME, IDX_RISCO, IDX_ID
)
from brute_force import ForcaBruta, gerar_grafo_sintetico
from greedy import Dijkstra, DijkstraComPrioridade


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def municipios():
    """Lista de tuplas de municípios para testes."""
    return [
        criar_vertice(1, "Porto Alegre",    0.72, 1850.0, 1400000),
        criar_vertice(2, "Santa Maria",     0.61, 730.0,  275000),
        criar_vertice(3, "Cruz Alta",       0.52, 600.0,  60000),
        criar_vertice(4, "Canoas",          0.79, 520.0,  340000),
        criar_vertice(5, "Lajeado",         0.83, 540.0,  80000),
        criar_vertice(6, "Gramado",         0.39, 410.0,  37000),
        criar_vertice(7, "Caxias do Sul",   0.48, 980.0,  435000),
        criar_vertice(8, "São Leopoldo",    0.77, 490.0,  215000),
    ]

@pytest.fixture
def bst_populada(municipios):
    bst = BinarySearchTree()
    for m in municipios:
        bst.inserir(m)
    return bst

@pytest.fixture
def grafo_simples():
    """Grafo triangular para testes de caminho."""
    g = Grafo()
    for i in range(4):
        g.adicionar_vertice(criar_vertice(i, f"M{i}", 0.5, 500.0, 10000))
    g.adicionar_aresta(0, 1, 2.0)
    g.adicionar_aresta(1, 2, 3.0)
    g.adicionar_aresta(0, 2, 10.0)  # caminho direto mais caro
    g.adicionar_aresta(2, 3, 1.0)
    return g


# ============================================================
# TESTES — BinarySearchTree
# ============================================================

class TestBST:

    def test_inserir_e_tamanho(self, municipios):
        bst = BinarySearchTree()
        for m in municipios:
            bst.inserir(m)
        assert len(bst) == len(municipios)

    def test_in_order_crescente(self, bst_populada, municipios):
        resultado = bst_populada.percurso_in_order()
        riscos = [v[IDX_RISCO] for v in resultado]
        assert riscos == sorted(riscos), "Percurso in-order deve retornar em ordem crescente"

    def test_busca_por_intervalo(self, bst_populada):
        alto_risco = bst_populada.buscar(0.70, 1.0)
        for v in alto_risco:
            assert 0.70 <= v[IDX_RISCO] <= 1.0

    def test_busca_retorna_corretos(self, bst_populada):
        """Todos os municípios com risco >= 0.70 devem aparecer na busca."""
        alto_risco = bst_populada.buscar(0.70, 1.0)
        nomes = {v[IDX_NOME] for v in alto_risco}
        assert "Porto Alegre" in nomes    # risco 0.72
        assert "Canoas" in nomes          # risco 0.79
        assert "Lajeado" in nomes         # risco 0.83
        assert "São Leopoldo" in nomes    # risco 0.77
        assert "Gramado" not in nomes     # risco 0.39

    def test_altura_razoavel(self, bst_populada, municipios):
        """Altura de BST com N nós deve ser no máximo N-1."""
        assert bst_populada.altura() <= len(municipios) - 1

    def test_remover_existente(self, bst_populada):
        tamanho_antes = len(bst_populada)
        removido = bst_populada.remover(1)  # Porto Alegre id=1
        assert removido is True
        assert len(bst_populada) == tamanho_antes - 1
        ids = {v[IDX_ID] for v in bst_populada.percurso_in_order()}
        assert 1 not in ids

    def test_remover_inexistente(self, bst_populada):
        removido = bst_populada.remover(9999)
        assert removido is False

    def test_bst_vazia(self):
        bst = BinarySearchTree()
        assert len(bst) == 0
        assert bst.altura() == -1
        assert bst.percurso_in_order() == []
        assert bst.buscar(0, 1) == []

    def test_propriedade_bst_mantida(self, bst_populada):
        """Após remoção, a propriedade BST deve ser mantida."""
        bst_populada.remover(1)
        resultado = bst_populada.percurso_in_order()
        riscos = [v[IDX_RISCO] for v in resultado]
        assert riscos == sorted(riscos)


# ============================================================
# TESTES — Grafo
# ============================================================

class TestGrafo:

    def test_adicionar_vertices(self):
        g = Grafo()
        v = criar_vertice(1, "Teste", 0.5, 100.0, 1000)
        g.adicionar_vertice(v)
        assert g.num_vertices() == 1

    def test_adicionar_arestas_bidirecional(self, grafo_simples):
        assert any(v == 1 for v, _ in grafo_simples.vizinhos(0))
        assert any(v == 0 for v, _ in grafo_simples.vizinhos(1))

    def test_bfs_visita_todos(self, grafo_simples):
        visitados = grafo_simples.bfs(0)
        assert set(visitados) == {0, 1, 2, 3}

    def test_dfs_visita_todos(self, grafo_simples):
        visitados = grafo_simples.dfs(0)
        assert set(visitados) == {0, 1, 2, 3}


# ============================================================
# TESTES — Força Bruta
# ============================================================

class TestForcaBruta:

    def test_encontra_caminho_otimo(self, grafo_simples):
        """0→1→2→3 custa 6.0, caminho direto 0→2→3 custa 11.0."""
        fb = ForcaBruta(grafo_simples)
        caminho, custo = fb.buscar_todos_caminhos(0, 3)
        assert pytest.approx(custo, abs=0.01) == 6.0
        assert caminho[0] == 0 and caminho[-1] == 3

    def test_contador_caminhos(self, grafo_simples):
        fb = ForcaBruta(grafo_simples)
        fb.buscar_todos_caminhos(0, 3)
        assert fb.caminhos_avaliados >= 1
        assert fb.chamadas_recursivas >= fb.caminhos_avaliados

    def test_sem_caminho(self):
        """Grafo com dois componentes disconnectos."""
        g = Grafo()
        for i in range(4):
            g.adicionar_vertice(criar_vertice(i, f"M{i}", 0.5, 100.0, 1000))
        g.adicionar_aresta(0, 1, 1.0)
        g.adicionar_aresta(2, 3, 1.0)  # componente separado
        fb = ForcaBruta(g)
        _, custo = fb.buscar_todos_caminhos(0, 3)
        assert custo == float("inf")

    def test_grafo_sintetico(self):
        g = gerar_grafo_sintetico(6)
        assert g.num_vertices() == 6
        assert g.num_arestas() >= 5  # pelo menos a cadeia base


# ============================================================
# TESTES — Dijkstra
# ============================================================

class TestDijkstra:

    def test_caminho_correto(self, grafo_simples):
        """0→1→2→3 é o caminho ótimo (custo 6.0)."""
        dij = Dijkstra(grafo_simples)
        caminho, custo = dij.caminho_minimo(0, 3)
        assert pytest.approx(custo, abs=0.01) == 6.0
        assert caminho[0] == 0 and caminho[-1] == 3

    def test_distancia_origem_zero(self, grafo_simples):
        dij = Dijkstra(grafo_simples)
        dij.todos_caminhos(0)
        assert dij.dist[0] == 0.0

    def test_todos_alcancaveis(self, grafo_simples):
        dij = Dijkstra(grafo_simples)
        dij.todos_caminhos(0)
        for vid in grafo_simples.adjacencia:
            assert dij.dist[vid] < float("inf")

    def test_sem_caminho_retorna_inf(self):
        g = Grafo()
        for i in range(3):
            g.adicionar_vertice(criar_vertice(i, f"M{i}", 0.5, 100.0, 1000))
        g.adicionar_aresta(0, 1, 1.0)
        dij = Dijkstra(g)
        _, custo = dij.caminho_minimo(0, 2)
        assert custo == float("inf")

    def test_dijkstra_igual_forca_bruta(self, grafo_simples):
        """Dijkstra deve encontrar o mesmo custo ótimo que a Força Bruta."""
        fb = ForcaBruta(grafo_simples)
        _, custo_fb = fb.buscar_todos_caminhos(0, 3)
        dij = Dijkstra(grafo_simples)
        _, custo_dij = dij.caminho_minimo(0, 3)
        assert pytest.approx(custo_dij, abs=0.001) == custo_fb

    def test_dijkstra_sintetico_vs_fb(self):
        """Valida Dijkstra contra FB para vários tamanhos pequenos."""
        for n in [5, 7, 8]:
            g = gerar_grafo_sintetico(n)
            fb = ForcaBruta(g)
            dij = Dijkstra(g)
            _, custo_fb = fb.buscar_todos_caminhos(0, n - 1)
            _, custo_dij = dij.caminho_minimo(0, n - 1)
            if custo_fb < float("inf"):
                assert pytest.approx(custo_dij, abs=0.001) == custo_fb, \
                    f"N={n}: FB={custo_fb}, Dijkstra={custo_dij}"

    def test_contadores_operacoes(self, grafo_simples):
        dij = Dijkstra(grafo_simples)
        dij.caminho_minimo(0, 3)
        assert dij.arestas_relaxadas > 0
        assert dij.insercoes_heap > 0


# ============================================================
# TESTES — DijkstraComPrioridade (integração BST + Dijkstra)
# ============================================================

class TestDijkstraComPrioridade:

    def test_plano_retorna_alto_risco(self, grafo_simples, municipios):
        bst = BinarySearchTree()
        for m in municipios[:4]:  # apenas primeiros 4
            bst.inserir(m)
        # Adiciona os vértices do grafo_simples na BST (ids 0-3)
        bst2 = BinarySearchTree()
        for i in range(4):
            bst2.inserir(criar_vertice(i, f"M{i}",
                                       [0.72, 0.61, 0.83, 0.52][i],
                                       500.0, 10000))
        dcp = DijkstraComPrioridade(grafo_simples, bst2)
        plano = dcp.plano_atendimento(0, limiar_risco=0.60)
        for item in plano:
            assert item["indice_risco"] >= 0.60


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
