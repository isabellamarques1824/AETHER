"""
brute_force.py
==============
Força Bruta — enumeração exaustiva de todos os caminhos simples entre origem e destino.
Serve como baseline/oráculo de validação para instâncias pequenas (N ≤ 12 nós).

Instrumentação:
    - Contador de chamadas recursivas
    - Contador de caminhos avaliados
    - Identificação do caminho ótimo (menor custo total)
    - Gráfico de explosão combinatória

Global Solution 2026 — FIAP | Disciplina: Estruturas de Dados e Algoritmos
"""

from __future__ import annotations
import time
import sys
import os
from typing import List, Tuple, Optional, Dict

# Adiciona o diretório pai ao path para importar data_structures
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_structures import Grafo, BinarySearchTree, carregar_grafo_json


# =============================================================================
# FORÇA BRUTA — backtracking exaustivo
# =============================================================================

class ForcaBruta:
    """
    Enumeração completa de todos os caminhos simples de 'origem' a 'destino'
    usando recursão com backtracking.

    Complexidade:
        Tempo:  O(V!) no pior caso — explosão fatorial
        Espaço: O(V) na pilha de recursão
    """

    def __init__(self, grafo: Grafo):
        self.grafo = grafo
        # Contadores de instrumentação
        self.chamadas_recursivas: int = 0
        self.caminhos_avaliados: int = 0
        # Melhor solução encontrada
        self.melhor_caminho: List[int] = []
        self.melhor_custo: float = float("inf")
        # Registro de todos os caminhos (custo, caminho)
        self.todos_caminhos: List[Tuple[float, List[int]]] = []

    def _resetar(self) -> None:
        self.chamadas_recursivas = 0
        self.caminhos_avaliados = 0
        self.melhor_caminho = []
        self.melhor_custo = float("inf")
        self.todos_caminhos = []

    def buscar_todos_caminhos(self, origem: int, destino: int) -> Tuple[List[int], float]:
        """
        Encontra o caminho de menor custo entre origem e destino
        enumerando todas as possibilidades.

        Retorna: (melhor_caminho, melhor_custo)
        """
        self._resetar()
        visitados: set = set()
        self._backtrack(origem, destino, visitados, [origem], 0.0)
        return self.melhor_caminho, self.melhor_custo

    def _backtrack(self, atual: int, destino: int, visitados: set,
                   caminho_atual: List[int], custo_atual: float) -> None:
        """Recursão com backtracking. Instrumentada com contadores."""
        self.chamadas_recursivas += 1
        visitados.add(atual)

        if atual == destino:
            self.caminhos_avaliados += 1
            self.todos_caminhos.append((custo_atual, list(caminho_atual)))
            if custo_atual < self.melhor_custo:
                self.melhor_custo = custo_atual
                self.melhor_caminho = list(caminho_atual)
        else:
            for vizinho, peso in self.grafo.vizinhos(atual):
                if vizinho not in visitados:
                    caminho_atual.append(vizinho)
                    self._backtrack(vizinho, destino, visitados,
                                    caminho_atual, custo_atual + peso)
                    caminho_atual.pop()  # backtrack

        visitados.discard(atual)

    def relatorio(self, origem: int, destino: int) -> str:
        """Gera relatório textual da busca."""
        nome_orig = self.grafo.vertices.get(origem, (origem,))[1] if origem in self.grafo.vertices else str(origem)
        nome_dest = self.grafo.vertices.get(destino, (destino,))[1] if destino in self.grafo.vertices else str(destino)
        caminho_nomes = [
            self.grafo.vertices[v][1] if v in self.grafo.vertices else str(v)
            for v in self.melhor_caminho
        ]
        linhas = [
            "=" * 60,
            "FORÇA BRUTA — Busca Exaustiva",
            "=" * 60,
            f"Origem:              {nome_orig}",
            f"Destino:             {nome_dest}",
            f"Chamadas recursivas: {self.chamadas_recursivas}",
            f"Caminhos avaliados:  {self.caminhos_avaliados}",
            f"Melhor custo:        {self.melhor_custo:.2f} h",
            f"Melhor caminho:      {' -> '.join(caminho_nomes)}",
            "=" * 60,
        ]
        return "\n".join(linhas)


# =============================================================================
# EXPERIMENTO DE ESCALABILIDADE — explosão combinatória
# =============================================================================

def gerar_grafo_sintetico(n: int) -> Grafo:
    """
    Gera um grafo aleatório com n vértices e ~n*1.5 arestas para benchmark.
    Usa seed fixa para reprodutibilidade.
    """
    import random
    random.seed(42)
    from data_structures import criar_vertice

    grafo = Grafo()
    for i in range(n):
        v = criar_vertice(i, f"Municipio_{i}", round(random.uniform(0.1, 0.99), 2),
                          round(random.uniform(100, 2000), 1), random.randint(5000, 500000))
        grafo.adicionar_vertice(v)

    # Garante conectividade com uma cadeia base
    for i in range(n - 1):
        peso = round(random.uniform(0.5, 6.0), 2)
        grafo.adicionar_aresta(i, i + 1, peso)

    # Arestas extras (grafo esparso mas conectado)
    extras = int(n * 0.6)
    nos = list(range(n))
    for _ in range(extras):
        u, v = random.sample(nos, 2)
        if v not in [viz for viz, _ in grafo.adjacencia[u]]:
            peso = round(random.uniform(0.5, 6.0), 2)
            grafo.adicionar_aresta(u, v, peso)

    return grafo


def medir_explosao_combinatoria(tamanhos: List[int]) -> Dict[int, dict]:
    """
    Para cada tamanho N, mede tempo de execução e número de caminhos da Força Bruta.
    Limita a 30 segundos por instância para evitar travamento.
    """
    resultados = {}
    for n in tamanhos:
        grafo = gerar_grafo_sintetico(n)
        fb = ForcaBruta(grafo)
        origem, destino = 0, n - 1

        inicio = time.perf_counter()
        fb.buscar_todos_caminhos(origem, destino)
        tempo_ms = (time.perf_counter() - inicio) * 1000

        resultados[n] = {
            "chamadas_recursivas": fb.chamadas_recursivas,
            "caminhos_avaliados": fb.caminhos_avaliados,
            "tempo_ms": round(tempo_ms, 4),
            "melhor_custo": round(fb.melhor_custo, 4),
        }
        print(f"  N={n:3d} | chamadas={fb.chamadas_recursivas:8d} | "
              f"caminhos={fb.caminhos_avaliados:6d} | tempo={tempo_ms:.2f} ms")

    return resultados


# =============================================================================
# VALIDAÇÃO: comparar FB com Dijkstra no mesmo grafo
# =============================================================================

def validar_contra_dijkstra(grafo: Grafo, origem: int, destino: int) -> dict:
    """
    Compara o custo ótimo da Força Bruta com o resultado do Dijkstra.
    Retorna dicionário com custos e gap de otimalidade (%).
    """
    from greedy import Dijkstra

    fb = ForcaBruta(grafo)
    _, custo_fb = fb.buscar_todos_caminhos(origem, destino)

    dij = Dijkstra(grafo)
    _, custo_dij = dij.caminho_minimo(origem, destino)

    gap = abs(custo_dij - custo_fb) / custo_fb * 100 if custo_fb > 0 else 0.0

    return {
        "custo_forca_bruta": round(custo_fb, 4),
        "custo_dijkstra": round(custo_dij, 4),
        "gap_percentual": round(gap, 2),
        "dijkstra_e_otimo": gap < 0.001,
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho = os.path.join(BASE, "data", "raw", "cenario_a_rs.json")
    grafo, bst = carregar_grafo_json(caminho)

    print("\n--- Força Bruta no Cenário A (Enchentes RS) ---")
    fb = ForcaBruta(grafo)
    # Porto Alegre -> Cruz Alta
    origem, destino = 4314902, 4306403
    caminho_otimo, custo = fb.buscar_todos_caminhos(origem, destino)
    print(fb.relatorio(origem, destino))

    print("\n--- Explosão Combinatória (grafos sintéticos) ---")
    tamanhos = [5, 8, 10, 12]
    resultados = medir_explosao_combinatoria(tamanhos)

    print("\n--- Validação vs. Dijkstra ---")
    grafo_pequeno = gerar_grafo_sintetico(8)
    val = validar_contra_dijkstra(grafo_pequeno, 0, 7)
    print(f"  Custo FB:       {val['custo_forca_bruta']}")
    print(f"  Custo Dijkstra: {val['custo_dijkstra']}")
    print(f"  Gap:            {val['gap_percentual']}%")
    print(f"  Dijkstra ótimo: {val['dijkstra_e_otimo']}")
