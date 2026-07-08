# Global Solution 2026 — Monitoramento de Riscos Ambientais
**Diciplina:** Dynamic Programming
**Tema:** Economia Espacial 
**Abordagem:** Força Bruta (baseline) e Dijkstra (solução eficiente) para rotas de atendimento em emergências ambientais.

---

## Integrantes do Grupo

| RA | Nome |
|----|------|
| RM563029 | Arthur Canaverde da Cruz |
| RM566470 | Isabella Jardim Marques |
| RM564624 | Mayene Moura da Silva |
| RM564053 | Murilo Canéstri dos Reis |

---

## Descrição do Projeto

Sistema de **monitoramento e triagem de riscos ambientais** em municípios brasileiros, instanciado em dois cenários reais:

- **Cenário A — Enchentes no Rio Grande do Sul (2024):** rede viária de municípios afetados, com rota ótima de atendimento a partir de Porto Alegre.
- **Cenário B — Seca no MATOPIBA:** municípios da fronteira agrícola MA/TO/PI/BA com índice de risco derivado de NDVI e precipitação, triados por ordem de criticidade a partir de Palmas.

### Algoritmos implementados
- **Força Bruta** (backtracking exaustivo, N ≤ 12) — baseline e oráculo de validação
- **Dijkstra** (algoritmo guloso, fila de prioridade com `heapq`) — solução eficiente para instâncias reais

### Estruturas de dados utilizadas
| Estrutura | Uso |
|-----------|-----|
| `tuple` | Vértice imutável do grafo (id, nome, risco, custo, população) |
| `dict` | Lista de adjacência do grafo; predecessores e distâncias do Dijkstra |
| `list` | Adjacência de vértices; caminho reconstruído |
| `set` | Controle de visitados (BFS/DFS/Dijkstra) |
| `heapq` | Fila de prioridade do Dijkstra |
| `deque` | Fila do BFS |
| `BinarySearchTree` | BST por índice de risco — consultas eficientes de municípios críticos |
| `Grafo` | Rede de municípios como dicionário de listas de adjacência |

---

## Estrutura do Repositório

```
GS_Dynamic/
├── README.md                        # Este arquivo
├── requirements.txt                 # Dependências Python
├── data/
│   ├── raw/
│   │   ├── cenario_a_rs.json        # Dados sintéticos Cenário A (Enchentes RS)
│   │   └── cenario_b_matopiba.json  # Dados sintéticos Cenário B (MATOPIBA)
│   └── processed/
│       └── benchmark_resultados.json  # Resultados do benchmark (gerado automaticamente)
├── src/
│   ├── data_structures.py           # Node, BinarySearchTree, Grafo
│   ├── brute_force.py               # Força Bruta com backtracking
│   ├── greedy.py                    # Dijkstra + DijkstraComPrioridade (BST)
│   ├── performance_monitor.py       # Tempo, memória, contadores de operações
│   └── visualizations.py           # Geração de todas as figuras obrigatórias
├── tests/
│   └── test_algorithms.py          # Testes unitários (pytest)
├── report/
│   ├── fig1a_grafo_cenario_a.png   # Figuras (geradas por visualizations.py)
│   ├── fig1b_grafo_cenario_b.png
│   ├── fig2_bst_diagrama.png
│   ├── fig3_desempenho_comparativo.png
│   ├── fig4_gap_otimalidade.png
│   └── relatorio_final.pdf         # Relatório técnico (≤ 4 páginas)
└── notebooks/
    └── analise_resultados.ipynb    # Análise interativa e escala de decisão
```

---

## Instalação e Execução

### 1. Pré-requisitos:
- Python 3.10+

### 2. Instalar dependências:
```bash
pip install -r requirements.txt
```

### 3. Executar os módulos:

**Estruturas de dados (BST + Grafo):**
```bash
python src/data_structures.py
```

**Força Bruta:**
```bash
python src/brute_force.py
```

**Dijkstra (Guloso) + Plano de Atendimento:**
```bash
python src/greedy.py
```

**Benchmark de desempenho:**
```bash
python src/performance_monitor.py
```

**Gerar todas as figuras:**
```bash
python src/visualizations.py
```
> As figuras são salvas em `report/fig*.png`.

**Testes unitários:**
```bash
pytest tests/test_algorithms.py -v
```

---

## Cenários Brasileiros

### Cenário A — Enchentes no Rio Grande do Sul
Baseado nos eventos de 2024, que afetaram 478 municípios gaúchos. O grafo modela 12 municípios com maior impacto, conectados por rodovias (pesos = horas de deslocamento). O Dijkstra a partir de Porto Alegre encontra a rota ótima para cada município em crise, enquanto a BST prioriza os de maior índice de risco.

**Fonte:** Dados sintéticos baseados em malha viária DNIT + relatórios Defesa Civil RS.

### Cenário B — Seca no MATOPIBA
A região MATOPIBA (Maranhão, Tocantins, Piauí e Bahia) concentra a nova fronteira agrícola brasileira e é altamente vulnerável à seca. O índice de risco de cada município é derivado de NDVI (cobertura vegetal) e precipitação INMET. A BST organiza os municípios por criticidade; Dijkstra a partir de Palmas determina a rota ótima de atendimento.

**Fonte:** Dados sintéticos baseados em NDVI MODIS/NASA + INMET precipitação histórica.

---

## Resultados Principais

- **Dijkstra é ótimo** para grafos com pesos não-negativos (gap ≈ 0% vs. Força Bruta).
- **Força Bruta torna-se inviável a partir de N ≈ 12** (crescimento fatorial O(V!)).
- **Dijkstra mantém tempo sub-milissegundal** até N=100 — O((V+E) log V).
- **A BST permite consultas em O(log N)** para identificar municípios de alto risco, integrando-se nativamente ao Dijkstra.

---

## Conexão com ODS

| ODS | Relação |
|-----|---------|
| ODS 2 — Fome zero | Triagem de seca no MATOPIBA protege a produção agrícola |
| ODS 9 — Infraestrutura | Grafo de rotas viárias para logística de emergência |
| ODS 11 — Cidades sustentáveis | Defesa civil com resposta eficiente às enchentes no RS |
| ODS 13 — Ação climática | Monitoramento ambiental com dados de satélites (GOES-16, Sentinel) |

---

## Referências

- Cormen, T. et al. (2022). *Introduction to Algorithms*, 4th Ed. MIT Press.
- Sedgewick, R. & Wayne, K. (2011). *Algorithms*, 4th Ed. Addison-Wesley.
- Skiena, S. (2020). *The Algorithm Design Manual*, 3rd Ed. Springer.
- NASA Earthdata — MODIS NDVI: [earthdata.nasa.gov](https://earthdata.nasa.gov)
- INPE PRODES/DETER: [terrabrasilis.dpi.inpe.br](https://terrabrasilis.dpi.inpe.br)
- INMET: [bdmep.inmet.gov.br](https://bdmep.inmet.gov.br)
- DNIT — Malha Viária: [dnit.gov.br](https://www.dnit.gov.br)
