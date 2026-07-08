"""
data_structures.py
==================
Implementação manual (sem bibliotecas externas) das estruturas de dados exigidas:
  - Node e BinarySearchTree (BST) por índice de risco
  - Grafo ponderado via dicionário de listas de adjacência

Global Solution 2026 — FIAP | Disciplina: Estruturas de Dados e Algoritmos
"""

from __future__ import annotations
from collections import deque
from typing import Optional, List, Tuple, Dict


# =============================================================================
# 1. NODO DO GRAFO — tupla imutável com atributos do município
# =============================================================================

def criar_vertice(id_municipio: int, nome: str, indice_risco: float,
                  custo_atendimento: float, populacao: int) -> tuple:
    """
    Cria um vértice como tupla imutável.
    Formato: (id_municipio, nome, indice_risco, custo_atendimento, populacao)
    Complexidade: O(1) — alocação constante.
    """
    return (id_municipio, nome, indice_risco, custo_atendimento, populacao)


# Índices de acesso às posições da tupla (clareza de código)
IDX_ID       = 0
IDX_NOME     = 1
IDX_RISCO    = 2
IDX_CUSTO    = 3
IDX_POP      = 4


# =============================================================================
# 2. ÁRVORE BINÁRIA DE BUSCA (BST) por índice de risco
# =============================================================================

class Node:
    """
    Nó da BST. Chave = indice_risco (float); valor = tupla do município.
    """
    def __init__(self, vertice: tuple):
        self.chave: float = vertice[IDX_RISCO]
        self.vertice: tuple = vertice
        self.esquerda: Optional[Node] = None
        self.direita: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node(risco={self.chave:.2f}, nome={self.vertice[IDX_NOME]})"


class BinarySearchTree:
    """
    A Árvore Binária de Busca implementada do zero.
    Propriedade BST: r_esquerda < r_pai < r_direita

    Operações existentes:
        inserir(vertice)        — O(h), h = altura
        buscar(r_min, r_max)    — O(h + k), k = resultados
        percurso_in_order()     — O(n)
        altura()                — O(n)
        remover(id_municipio)   — O(h)
    """

    def __init__(self):
        self.raiz: Optional[Node] = None
        self._tamanho: int = 0

    # ------------------------------------------------------------------ - 
    # inserir
    # ------------------------------------------------------------------ - 
    def inserir(self, vertice: tuple) -> None:
        """Insere município mantendo a propriedade BST."""
        novo = Node(vertice)
        if self.raiz is None:
            self.raiz = novo
        else:
            self._inserir_rec(self.raiz, novo)
        self._tamanho += 1

    def _inserir_rec(self, atual: Node, novo: Node) -> None:
        if novo.chave < atual.chave:
            if atual.esquerda is None:
                atual.esquerda = novo
            else:
                self._inserir_rec(atual.esquerda, novo)
        else:
            if atual.direita is None:
                atual.direita = novo
            else:
                self._inserir_rec(atual.direita, novo)

    # ------------------------------------------------------------------
    # buscar por intervalo [r_min, r_max]
    # ------------------------------------------------------------------
    def buscar(self, r_min: float, r_max: float) -> List[tuple]:
        """Retorna lista de municípios com índice_risco em [r_min, r_max]."""
        resultado: List[tuple] = []
        self._buscar_rec(self.raiz, r_min, r_max, resultado)
        return resultado

    def _buscar_rec(self, node: Optional[Node], r_min: float,
                    r_max: float, resultado: List[tuple]) -> None:
        if node is None:
            return
        if node.chave > r_min:
            self._buscar_rec(node.esquerda, r_min, r_max, resultado)
        if r_min <= node.chave <= r_max:
            resultado.append(node.vertice)
        if node.chave < r_max:
            self._buscar_rec(node.direita, r_min, r_max, resultado)

    # ------------------------------------------------------------------
    # percurso in-order (crescente de risco)
    # ------------------------------------------------------------------
    def percurso_in_order(self) -> List[tuple]:
        """Retorna municípios em ordem crescente de índice de risco."""
        resultado: List[tuple] = []
        self._in_order_rec(self.raiz, resultado)
        return resultado

    def _in_order_rec(self, node: Optional[Node], resultado: List[tuple]) -> None:
        if node is None:
            return
        self._in_order_rec(node.esquerda, resultado)
        resultado.append(node.vertice)
        self._in_order_rec(node.direita, resultado)

    # ------------------------------------------------------------------
    # altura
    # ------------------------------------------------------------------
    def altura(self) -> int:
        """Calcula a altura da árvore. O(n)."""
        return self._altura_rec(self.raiz)

    def _altura_rec(self, node: Optional[Node]) -> int:
        if node is None:
            return -1
        return 1 + max(self._altura_rec(node.esquerda),
                       self._altura_rec(node.direita))

    def esta_balanceada(self) -> bool:
        """Verifica se |altura_esq - altura_dir| <= 1 na raiz."""
        h_esq = self._altura_rec(self.raiz.esquerda) if self.raiz else -1
        h_dir = self._altura_rec(self.raiz.direita)  if self.raiz else -1
        return abs(h_esq - h_dir) <= 1

    # ------------------------------------------------------------------
    # remover por id_municipio
    # ------------------------------------------------------------------
    def remover(self, id_municipio: int) -> bool:
        """Remove o nó pelo id do município. Retorna True se encontrado."""
        self.raiz, removido = self._remover_rec(self.raiz, id_municipio)
        if removido:
            self._tamanho -= 1
        return removido

    def _remover_rec(self, node: Optional[Node],
                     id_municipio: int) -> Tuple[Optional[Node], bool]:
        if node is None:
            return None, False
        if node.vertice[IDX_ID] == id_municipio:
            # Caso 1: sem filhos
            if node.esquerda is None and node.direita is None:
                return None, True
            # Caso 2: um filho
            if node.esquerda is None:
                return node.direita, True
            if node.direita is None:
                return node.esquerda, True
            # Caso 3: dois filhos — substitui pelo sucessor in-order (mínimo da direita)
            sucessor = self._minimo(node.direita)
            node.chave = sucessor.chave
            node.vertice = sucessor.vertice
            node.direita, _ = self._remover_rec(
                node.direita, sucessor.vertice[IDX_ID])
            return node, True
        # Busca pelo nó
        if id_municipio < node.chave:
            node.esquerda, removido = self._remover_rec(node.esquerda, id_municipio)
        else:
            node.direita, removido = self._remover_rec(node.direita, id_municipio)
        return node, removido

    def _minimo(self, node: Node) -> Node:
        while node.esquerda is not None:
            node = node.esquerda
        return node

    def __len__(self) -> int:
        return self._tamanho

    def __repr__(self) -> str:
        return f"BinarySearchTree(tamanho={self._tamanho}, altura={self.altura()})"


# =============================================================================
# 3. GRAFO PONDERADO — dicionário de listas de adjacência
# =============================================================================

class Grafo:
    """
    Grafo não-direcionado ponderado implementado como dicionário de listas.

    Justificativa da escolha (lista de adjacência vs. matriz):
        - Espaço: O(V + E) vs O(V²) — nossos grafos são esparsos (poucos municípios
          conectados entre si), então a lista de adjacência é muito mais eficiente.
        - Tempo de iteração sobre vizinhos: O(grau(v)) vs O(V).
        - Para algoritmos como Dijkstra/Prim, percorremos apenas vizinhos reais,
          o que torna a lista de adjacência ideal.
    """

    def __init__(self):
        # {id_vertice: [(vizinho_id, peso), ...]}
        self.adjacencia: Dict[int, List[Tuple[int, float]]] = {}
        # {id_vertice: tupla_municipio}
        self.vertices: Dict[int, tuple] = {}

    def adicionar_vertice(self, vertice: tuple) -> None:
        """Adiciona município ao grafo. O(1) amortizado."""
        vid = vertice[IDX_ID]
        self.vertices[vid] = vertice
        if vid not in self.adjacencia:
            self.adjacencia[vid] = []

    def adicionar_aresta(self, u: int, v: int, peso: float) -> None:
        """Adiciona aresta bidirecional (u, v) com peso. O(1)."""
        if u not in self.adjacencia:
            self.adjacencia[u] = []
        if v not in self.adjacencia:
            self.adjacencia[v] = []
        self.adjacencia[u].append((v, peso))
        self.adjacencia[v].append((u, peso))

    def vizinhos(self, vid: int) -> List[Tuple[int, float]]:
        """Retorna lista de (vizinho_id, peso). O(1)."""
        return self.adjacencia.get(vid, [])

    def num_vertices(self) -> int:
        return len(self.vertices)

    def num_arestas(self) -> int:
        return sum(len(v) for v in self.adjacencia.values()) // 2

    # ------------------------------------------------------------------
    # BFS — percurso em largura
    # ------------------------------------------------------------------
    def bfs(self, origem: int) -> List[int]:
        """Retorna ordem de visita BFS a partir da origem. O(V + E)."""
        visitados: set = set()
        fila: deque = deque([origem])
        ordem: List[int] = []
        visitados.add(origem)
        while fila:
            atual = fila.popleft()
            ordem.append(atual)
            for vizinho, _ in self.adjacencia.get(atual, []):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return ordem

    # ------------------------------------------------------------------
    # DFS — percurso em profundidade
    # ------------------------------------------------------------------
    def dfs(self, origem: int) -> List[int]:
        """Retorna ordem de visita DFS. O(V + E)."""
        visitados: set = set()
        ordem: List[int] = []
        self._dfs_rec(origem, visitados, ordem)
        return ordem

    def _dfs_rec(self, atual: int, visitados: set, ordem: List[int]) -> None:
        visitados.add(atual)
        ordem.append(atual)
        for vizinho, _ in self.adjacencia.get(atual, []):
            if vizinho not in visitados:
                self._dfs_rec(vizinho, visitados, ordem)

    def __repr__(self) -> str:
        return (f"Grafo(vertices={self.num_vertices()}, "
                f"arestas={self.num_arestas()})")


# =============================================================================
# 4. FUNÇÕES UTILITÁRIAS — carregamento de JSON para estruturas
# =============================================================================

import json
import os
import sys


def carregar_grafo_json(caminho: str) -> Tuple[Grafo, BinarySearchTree]:
    """
    Lê um arquivo JSON (formato dos cenários A/B) e retorna:
        - Grafo de municípios
        - BST dos municípios por índice de risco
    """
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    grafo = Grafo()
    bst = BinarySearchTree()

    for m in dados["municipios"]:
        v = criar_vertice(m["id"], m["nome"], m["indice_risco"],
                          m["custo_atendimento"], m["populacao"])
        grafo.adicionar_vertice(v)
        bst.inserir(v)

    for a in dados["arestas"]:
        grafo.adicionar_aresta(a["origem"], a["destino"], a["peso"])

    return grafo, bst


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # Teste rápido
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho = os.path.join(BASE, "data", "raw", "cenario_a_rs.json")
    grafo, bst = carregar_grafo_json(caminho)

    print(grafo)
    print(bst)
    print("\nMunicípios em ordem crescente de risco:")
    for v in bst.percurso_in_order():
        print(f"  {v[IDX_NOME]:<20} risco={v[IDX_RISCO]:.2f}")

    print("\nMunicípios com risco > 0.70:")
    for v in bst.buscar(0.70, 1.0):
        print(f"  {v[IDX_NOME]:<20} risco={v[IDX_RISCO]:.2f}")

    print(f"\nAltura BST: {bst.altura()}")
    print(f"BST balanceada: {bst.esta_balanceada()}")
    print(f"\nBFS a partir de Porto Alegre: {grafo.bfs(4314902)}")
