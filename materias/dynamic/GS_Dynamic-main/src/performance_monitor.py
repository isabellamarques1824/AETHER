"""
performance_monitor.py
======================
Monitoramento de desempenho para Força Bruta e Dijkstra.

Métricas coletadas por algoritmo e tamanho N:
    - Tempo de execução (ms) via time.perf_counter()
    - Memória alocada (MB) via tracemalloc
    - Número de operações elementares:
        * Força Bruta: chamadas recursivas
        * Dijkstra:    arestas relaxadas + inserções no heap

Instâncias testadas: N = 5, 8, 10, 12, 20, 50, 100

Global Solution 2026 — FIAP | Disciplina: Estruturas de Dados e Algoritmos
"""

from __future__ import annotations
import time
import tracemalloc
import sys
import os
import json
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_structures import Grafo, carregar_grafo_json
from brute_force import ForcaBruta, gerar_grafo_sintetico
from greedy import Dijkstra


# =============================================================================
# FUNÇÕES DE MEDIÇÃO
# =============================================================================

def medir_forca_bruta(n: int) -> dict:
    """Executa FB em grafo sintético de N vértices e retorna métricas."""
    grafo = gerar_grafo_sintetico(n)
    fb = ForcaBruta(grafo)
    origem, destino = 0, n - 1

    tracemalloc.start()
    inicio = time.perf_counter()

    fb.buscar_todos_caminhos(origem, destino)

    tempo_ms = (time.perf_counter() - inicio) * 1000
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algoritmo": "Força Bruta",
        "N": n,
        "tempo_ms": round(tempo_ms, 4),
        "memoria_mb": round(pico / 1024 / 1024, 4),
        "operacoes": fb.chamadas_recursivas,
        "caminhos_avaliados": fb.caminhos_avaliados,
        "custo_otimo": round(fb.melhor_custo, 4),
    }


def medir_dijkstra(n: int) -> dict:
    """Executa Dijkstra em grafo sintético de N vértices e retorna métricas."""
    grafo = gerar_grafo_sintetico(n)
    dij = Dijkstra(grafo)
    origem, destino = 0, n - 1

    tracemalloc.start()
    inicio = time.perf_counter()

    _, custo = dij.caminho_minimo(origem, destino)

    tempo_ms = (time.perf_counter() - inicio) * 1000
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algoritmo": "Dijkstra",
        "N": n,
        "tempo_ms": round(tempo_ms, 4),
        "memoria_mb": round(pico / 1024 / 1024, 4),
        "operacoes": dij.arestas_relaxadas + dij.insercoes_heap,
        "arestas_relaxadas": dij.arestas_relaxadas,
        "insercoes_heap": dij.insercoes_heap,
        "custo_otimo": round(custo, 4),
    }


# =============================================================================
# BENCHMARK COMPLETO
# =============================================================================

def executar_benchmark(tamanhos_fb: List[int] = None,
                       tamanhos_dij: List[int] = None) -> Dict[str, List[dict]]:
    """
    Executa benchmark completo.
    FB é limitado a N ≤ 12 pois cresce fatorialmente.
    Dijkstra é testado até N=100.
    """
    if tamanhos_fb is None:
        tamanhos_fb = [5, 8, 10, 12]
    if tamanhos_dij is None:
        tamanhos_dij = [5, 8, 10, 12, 20, 50, 100]

    resultados_fb: List[dict] = []
    resultados_dij: List[dict] = []

    print("\n" + "=" * 60)
    print("BENCHMARK — Força Bruta")
    print("=" * 60)
    for n in tamanhos_fb:
        print(f"  Testando N={n}...", end=" ", flush=True)
        r = medir_forca_bruta(n)
        resultados_fb.append(r)
        print(f"tempo={r['tempo_ms']:.2f}ms | "
              f"chamadas={r['operacoes']} | "
              f"caminhos={r['caminhos_avaliados']}")

    print("\n" + "=" * 60)
    print("BENCHMARK — Dijkstra")
    print("=" * 60)
    for n in tamanhos_dij:
        print(f"  Testando N={n}...", end=" ", flush=True)
        r = medir_dijkstra(n)
        resultados_dij.append(r)
        print(f"tempo={r['tempo_ms']:.2f}ms | "
              f"operações={r['operacoes']} | "
              f"memória={r['memoria_mb']:.4f}MB")

    return {"forca_bruta": resultados_fb, "dijkstra": resultados_dij}


def calcular_gap_otimalidade(tamanhos: List[int] = None) -> List[dict]:
    """
    Calcula o gap de otimalidade entre FB (ótimo) e Dijkstra para N ≤ 12.
    Dijkstra é ótimo para grafos com pesos não-negativos, então gap ≈ 0%.
    """
    if tamanhos is None:
        tamanhos = [5, 8, 10, 12]

    gaps = []
    for n in tamanhos:
        grafo = gerar_grafo_sintetico(n)
        fb = ForcaBruta(grafo)
        dij = Dijkstra(grafo)
        origem, destino = 0, n - 1

        _, custo_fb = fb.buscar_todos_caminhos(origem, destino)
        _, custo_dij = dij.caminho_minimo(origem, destino)

        gap = abs(custo_dij - custo_fb) / custo_fb * 100 if custo_fb > 0 else 0.0
        gaps.append({
            "N": n,
            "custo_fb": round(custo_fb, 4),
            "custo_dijkstra": round(custo_dij, 4),
            "gap_percentual": round(gap, 4),
        })
        print(f"  N={n:3d} | FB={custo_fb:.4f} | Dijkstra={custo_dij:.4f} | gap={gap:.4f}%")

    return gaps


def salvar_resultados(resultados: dict, caminho_saida: str) -> None:
    """Salva os resultados do benchmark em JSON."""
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"\nOs resultados são salvos em: {caminho_saida}")


def imprimir_tabela(resultados: Dict[str, List[dict]]) -> None:
    """Imprime tabela comparativa no terminal."""
    print("\n" + "=" * 80)
    print(f"{'Algoritmo':<14} {'N':>4} {'Tempo (ms)':>12} {'Memória (MB)':>13} {'Operações':>12}")
    print("-" * 80)
    for r in resultados.get("forca_bruta", []):
        print(f"{'Força Bruta':<14} {r['N']:>4} {r['tempo_ms']:>12.4f} "
              f"{r['memoria_mb']:>13.4f} {r['operacoes']:>12}")
    for r in resultados.get("dijkstra", []):
        print(f"{'Dijkstra':<14} {r['N']:>4} {r['tempo_ms']:>12.4f} "
              f"{r['memoria_mb']:>13.4f} {r['operacoes']:>12}")
    print("=" * 80)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    resultados = executar_benchmark()

    print("\n--- Gap de Otimalidade (FB vs Dijkstra) ---")
    gaps = calcular_gap_otimalidade()

    imprimir_tabela(resultados)

    # Salva em JSON para uso nas visualizações
    saida = os.path.join(BASE, "data", "processed", "benchmark_resultados.json")
    resultados["gaps"] = gaps
    salvar_resultados(resultados, saida)
