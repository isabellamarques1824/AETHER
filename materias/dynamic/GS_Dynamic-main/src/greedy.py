"""
greedy.py
=========
Algoritmo Guloso — Dijkstra (caminho mínimo de fonte única).

Justificativa da escolha:
    Dijkstra é ideal para os cenários A (Enchentes RS) e B (MATOPIBA) porque
    o objetivo é encontrar a rota de menor custo/tempo de deslocamento partindo
    de um hub central (Porto Alegre ou Palmas) até cada município afetado.
    Prim/Kruskal resolveriam um problema diferente (MST de cobertura total),
    enquanto Dijkstra responde à pergunta operacional concreta: "qual é o
    caminho mais rápido do hub até o município X em crise?".

Prova informal de corretude (greedy choice):
    A cada passo, Dijkstra extrai o vértice não-visitado com menor distância
    acumulada. Como os pesos são não-negativos, nunca haverá um caminho mais
    curto passando por vértices ainda não processados — pois qualquer extensão
    só aumentaria o custo. Essa propriedade garante que, ao visitar um vértice,
    seu caminho já é ótimo.

Complexidade:
    Tempo:  O((V + E) log V) com heap binário
    Espaço: O(V) para dist[], prev[] e heap

Global Solution 2026 — FIAP | Disciplina: Estruturas de Dados e Algoritmos
"""

from __future__ import annotations
import heapq
import sys
import os
from typing import List, Tuple, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_structures import Grafo, BinarySearchTree, carregar_grafo_json, IDX_NOME, IDX_RISCO


# =============================================================================
# DIJKSTRA
# =============================================================================

class Dijkstra:
    """
    Implementação de Dijkstra com heapq.

    Após executar caminho_minimo(origem, destino) ou todos_caminhos(origem),
    os atributos dist e prev ficam disponíveis para a análise.
    """

    def __init__(self, grafo: Grafo):
        self.grafo = grafo
        self.dist: Dict[int, float] = {}
        self.prev: Dict[int, Optional[int]] = {}
        # Contadores para monitoramento de desempenho
        self.arestas_relaxadas: int = 0
        self.insercoes_heap: int = 0

    def _resetar(self) -> None:
        self.dist = {}
        self.prev = {}
        self.arestas_relaxadas = 0
        self.insercoes_heap = 0

    def todos_caminhos(self, origem: int) -> Dict[int, float]:
        """
        Calcula o menor custo da origem a TODOS os vértices alcançáveis.
        Retorna dicionário {id_vertice: custo_minimo}.
        """
        self._resetar()

        # Inicialização
        for vid in self.grafo.adjacencia:
            self.dist[vid] = float("inf")
            self.prev[vid] = None
        self.dist[origem] = 0.0

        # heap: (custo_acumulado, id_vertice)
        heap: List[Tuple[float, int]] = [(0.0, origem)]
        self.insercoes_heap += 1
        visitados: set = set()

        while heap:
            custo_atual, u = heapq.heappop(heap)

            if u in visitados:
                continue
            visitados.add(u)

            # Relaxamento das arestas
            for v, peso in self.grafo.vizinhos(u):
                self.arestas_relaxadas += 1
                novo_custo = custo_atual + peso
                if novo_custo < self.dist.get(v, float("inf")):
                    self.dist[v] = novo_custo
                    self.prev[v] = u
                    heapq.heappush(heap, (novo_custo, v))
                    self.insercoes_heap += 1

        return {v: c for v, c in self.dist.items() if c < float("inf")}

    def caminho_minimo(self, origem: int, destino: int) -> Tuple[List[int], float]:
        """
        Retorna (caminho, custo) do menor caminho de origem a destino.
        Executa todos_caminhos() internamente.
        """
        self.todos_caminhos(origem)
        caminho = self._reconstruir_caminho(destino)
        return caminho, self.dist.get(destino, float("inf"))

    def _reconstruir_caminho(self, destino: int) -> List[int]:
        """Reconstrói o caminho a partir do dicionário prev[]."""
        caminho: List[int] = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = self.prev.get(atual)
        caminho.reverse()
        # Se o primeiro elemento não é a origem válida, caminho não existe
        if len(caminho) == 1 and self.dist.get(destino, float("inf")) == float("inf"):
            return []
        return caminho

    def relatorio(self, origem: int, destino: int) -> str:
        """Relatório textual da execução de Dijkstra."""
        caminho, custo = self.caminho_minimo(origem, destino)
        caminho_nomes = [
            self.grafo.vertices[v][IDX_NOME] if v in self.grafo.vertices else str(v)
            for v in caminho
        ]
        linhas = [
            "=" * 60,
            "DIJKSTRA — Algoritmo Guloso (Caminho Mínimo)",
            "=" * 60,
            f"Origem:              {self.grafo.vertices.get(origem, (origem,))[1] if origem in self.grafo.vertices else origem}",
            f"Destino:             {self.grafo.vertices.get(destino, (destino,))[1] if destino in self.grafo.vertices else destino}",
            f"Custo total:         {custo:.2f} h",
            f"Arestas relaxadas:   {self.arestas_relaxadas}",
            f"Inserções no heap:   {self.insercoes_heap}",
            f"Caminho:             {' -> '.join(caminho_nomes)}",
            "=" * 60,
            "",
            "Razão da escolha gulosa a cada passo:",
            "  Em cada iteração, o vértice com MENOR custo acumulado é",
            "  processado primeiro. Como pesos >= 0, esse custo nunca será",
            "  melhorado posteriormente — garantia de otimalidade local e global.",
        ]
        return "\n".join(linhas)


# =============================================================================
# DIJKSTRA COM BST — prioriza municípios de alto risco
# =============================================================================

class DijkstraComPrioridade:
    """
    Extensão do Dijkstra que usa a BST para identificar municípios de alto
    risco e retorna os caminhos para eles em ordem de criticidade.

    Fluxo:
        1. BST.buscar(limiar, 1.0) → lista de municípios críticos
        2. Dijkstra(origem) → distâncias para todos os vértices
        3. Retorna ranking: município crítico + custo de chegar lá
    """

    def __init__(self, grafo: Grafo, bst: BinarySearchTree):
        self.grafo = grafo
        self.bst = bst
        self.dijkstra = Dijkstra(grafo)

    def plano_atendimento(self, origem: int,
                          limiar_risco: float = 0.70) -> List[dict]:
        """
        Retorna lista de dicionários ordenada por (risco DESC, custo ASC)
        para municípios com índice_risco >= limiar_risco.
        """
        # 1. Executa Dijkstra a partir do hub
        custos = self.dijkstra.todos_caminhos(origem)

        # 2. Consulta BST para municípios de alto risco
        criticos = self.bst.buscar(limiar_risco, 1.0)

        # 3. Monta plano de atendimento
        plano = []
        for v in criticos:
            vid = v[0]
            if vid == origem:
                continue
            custo = custos.get(vid, float("inf"))
            caminho = self.dijkstra._reconstruir_caminho(vid)
            caminho_nomes = [
                self.grafo.vertices[n][IDX_NOME] if n in self.grafo.vertices else str(n)
                for n in caminho
            ]
            plano.append({
                "id": vid,
                "nome": v[IDX_NOME],
                "indice_risco": v[IDX_RISCO],
                "custo_horas": round(custo, 2),
                "caminho": caminho_nomes,
            })

        # Ordena: primeiro maior risco, depois menor custo
        plano.sort(key=lambda x: (-x["indice_risco"], x["custo_horas"]))
        return plano

    def imprimir_plano(self, origem: int, limiar_risco: float = 0.70) -> None:
        plano = self.plano_atendimento(origem, limiar_risco)
        nome_hub = self.grafo.vertices.get(origem, (origem,))[1] if origem in self.grafo.vertices else str(origem)
        print(f"\nPlano de Atendimento — Hub: {nome_hub} | Limiar de risco: {limiar_risco}")
        print("-" * 70)
        print(f"{'Município':<22} {'Risco':>6} {'Custo(h)':>9}  Rota")
        print("-" * 70)
        for item in plano:
            rota = " -> ".join(item["caminho"])
            print(f"{item['nome']:<22} {item['indice_risco']:>6.2f} {item['custo_horas']:>9.2f}  {rota}")
        print("-" * 70)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("\n=== CENÁRIO A — Enchentes RS ===")
    caminho_a = os.path.join(BASE, "data", "raw", "cenario_a_rs.json")
    grafo_a, bst_a = carregar_grafo_json(caminho_a)

    dij_a = DijkstraComPrioridade(grafo_a, bst_a)
    dij_a.imprimir_plano(origem=4314902, limiar_risco=0.70)

    print("\n=== CENÁRIO B — Seca MATOPIBA ===")
    caminho_b = os.path.join(BASE, "data", "raw", "cenario_b_matopiba.json")
    grafo_b, bst_b = carregar_grafo_json(caminho_b)

    dij_b = DijkstraComPrioridade(grafo_b, bst_b)
    dij_b.imprimir_plano(origem=1721000, limiar_risco=0.75)

    print("\n=== Relatório detalhado: Porto Alegre -> Cruz Alta ===")
    dij = Dijkstra(grafo_a)
    print(dij.relatorio(4314902, 4306403))
