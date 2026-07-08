# AETHER

**Sistema autônomo adaptativo para ambientes extremos**

O **AETHER** é um projeto acadêmico desenvolvido para a **Global Solution 2026**, com o objetivo de propor uma solução tecnológica capaz de auxiliar comunidades, bases operacionais e instituições localizadas em ambientes extremos ou vulneráveis.

A ideia central do projeto é simples: **ambientes extremos precisam de sistemas que saibam se adaptar**.

Pensando nisso, o AETHER foi idealizado como uma plataforma inteligente capaz de monitorar condições críticas, priorizar recursos essenciais e ativar modos de operação específicos em situações como seca, enchentes, falhas de comunicação, isolamento geográfico e emergências ambientais.

---

## Sobre o projeto

O AETHER é um sistema conceitual e em fase inicial de prototipação, criado para demonstrar como tecnologias como sensores, análise de dados, banco de dados, redes e organização ágil podem ser integradas em uma solução voltada para resiliência em cenários extremos.

O projeto foi pensado especialmente para locais como:

* Escolas remotas;
* Comunidades isoladas;
* Postos de saúde em regiões vulneráveis;
* Áreas afetadas por enchentes;
* Regiões com seca severa;
* Ambientes com baixa infraestrutura de comunicação;
* Bases operacionais em locais de difícil acesso.

Além da aplicação terrestre, o conceito do AETHER também foi expandido para cenários futuros, como bases lunares, bases marcianas e missões espaciais, onde a adaptação automática e a gestão inteligente de recursos seriam ainda mais críticas.

---

## Problema

Comunidades em regiões isoladas ou afetadas por desastres ambientais enfrentam dificuldades como:

* Falta de acesso constante à água;
* Instabilidade de energia e comunicação;
* Baixa capacidade de resposta em emergências;
* Dificuldade de monitoramento ambiental;
* Falta de dados organizados para tomada de decisão;
* Dependência de ações manuais em situações críticas.

Esses problemas podem comprometer a segurança, a saúde, a educação e a sobrevivência das pessoas nesses ambientes.

---

## Solução proposta

O AETHER propõe um sistema adaptativo capaz de identificar o tipo de situação enfrentada e ativar modos específicos de funcionamento.

A solução é organizada em quatro modos principais:

### AquaSave

Modo voltado para situações de escassez de água.

O objetivo é monitorar o uso, identificar risco de falta de abastecimento e priorizar o consumo de água para atividades essenciais.

### ResourceLock

Modo de preservação de recursos.

Quando o sistema identifica risco de escassez, ele reduz ou limita o uso de recursos não essenciais, priorizando energia, água, conectividade e equipamentos críticos.

### SignalLock

Modo de proteção e priorização da comunicação.

Esse modo é ativado quando há instabilidade de rede ou risco de perda de conexão. O sistema prioriza mensagens importantes, alertas e dados essenciais.

### Emergency Mode

Modo de emergência.

Ativado em situações críticas, como enchentes, colapso de recursos, falhas graves de comunicação ou risco direto à comunidade. Nesse modo, o AETHER prioriza alertas, rotas de apoio, comunicação emergencial e ações de resposta rápida.

---

## Objetivos

* Criar uma solução tecnológica voltada para ambientes extremos;
* Demonstrar como dados podem apoiar decisões em situações críticas;
* Organizar informações ambientais e operacionais em um banco de dados;
* Propor uma arquitetura adaptável para diferentes cenários;
* Simular modos inteligentes de funcionamento;
* Criar uma base conceitual para futuras implementações práticas;
* Integrar conhecimentos de diferentes disciplinas da Global Solution.

---

## Funcionalidades previstas

* Monitoramento de condições ambientais;
* Registro de dados críticos;
* Classificação de níveis de risco;
* Ativação automática de modos operacionais;
* Controle e priorização de recursos;
* Geração de alertas;
* Histórico de eventos;
* Apoio à tomada de decisão;
* Visualização de dados em dashboards;
* Organização de informações para análise futura.

---

## Protótipo

O projeto ainda está em fase inicial e funciona como uma proposta conceitual/prototipada.

Foram criados materiais visuais para representar como o AETHER poderia funcionar em diferentes cenários, incluindo:

* Escola remota;
* Comunidade afetada por enchente;
* Local com comunicação instável;
* Base lunar;
* Base marciana;
* Missão espacial;
* Central de controle;
* Robô assistente do sistema;
* Modos operacionais do AETHER.

### Imagens do protótipo


```md
![Protótipo do AETHER](./assets/aether-prototipo.png)
![Modos do sistema](./assets/aether-modos.png)
![Aplicações terrestres](./assets/aether-terra.png)
![Aplicações espaciais](./assets/aether-espaco.png)
```

---

## Tecnologias e áreas envolvidas

O AETHER foi desenvolvido como um projeto multidisciplinar, envolvendo diferentes áreas da Engenharia de Software.

### Agile & Squads

Organização do projeto, definição de papéis, backlog, planejamento das entregas e divisão das tarefas da equipe.

### Database Design

Modelagem dos dados necessários para armazenar informações sobre ambientes, sensores, alertas, recursos, eventos e modos de operação.

### Data Science

Análise dos dados coletados para apoiar previsões, identificação de padrões e tomada de decisão em situações críticas.

### Network Architect Solutions

Planejamento da infraestrutura de rede e comunicação para cenários com conexão instável ou limitada.

### Dynamic Programming / Desenvolvimento

Construção da lógica do sistema, organização das funcionalidades e estruturação inicial da solução.

### Java

Implementação inicial do protótipo, estruturação das classes, aplicação dos conceitos de Programação Orientada a Objetos e testes das funcionalidades principais do sistema.

---

## Estrutura sugerida do repositório

```bash
AETHER/
│
├── README.md
│
├── imagens/
│   ├── aether-prototipo.png
│   ├── modos-aether.png
│   ├── aplicacoes-terra.png
│   └── aplicacoes-espaco.png
│
└── materias/
    ├── agile/
    │   └── README.md
    │
    ├── database/
    │   └── README.md
    │
    ├── data-science/
    │   └── README.md
    │
    ├── network/
    │   └── README.md
    │
    ├── dynamic/
    │   └── README.md
    │
    └── java/
        └── README.md
```

---

## Organização por matérias

A documentação do projeto foi separada por matéria para facilitar a navegação e deixar claro o que foi desenvolvido em cada área da Global Solution.

| Matéria      | Conteúdo                                                                              |
| ------------ | ------------------------------------------------------------------------------------- |
| Agile        | Organização do projeto, divisão da equipe, backlog, planejamento e metodologia        |
| Database     | Modelagem do banco de dados, entidades, relacionamentos e estrutura das informações   |
| Data Science | Análise de dados, indicadores, hipóteses e uso das informações para tomada de decisão |
| Network      | Arquitetura de rede, comunicação, conectividade e cenários com sinal instável         |
| Dynamic      | Lógica do sistema, regras de funcionamento e comportamento dos modos adaptativos      |
| Java         | Implementação inicial, estrutura do código, classes e testes do protótipo             |
| Imagens      | Protótipos visuais, representações do sistema, cenários e identidade visual do AETHER |

---

## Possíveis aplicações

O AETHER pode ser adaptado para diferentes contextos:

### Ambientes terrestres

* Escolas em regiões isoladas;
* Comunidades ribeirinhas;
* Áreas atingidas por enchentes;
* Regiões de seca extrema;
* Postos de saúde remotos;
* Centros de apoio emergencial.

### Ambientes espaciais

* Bases lunares;
* Bases marcianas;
* Estações de pesquisa;
* Missões espaciais;
* Ambientes com recursos extremamente limitados.

---

## Diferenciais do projeto

* Sistema baseado em modos adaptativos;
* Foco em resiliência e sobrevivência operacional;
* Aplicação em cenários reais e futuros;
* Integração entre dados, rede, recursos e emergência;
* Proposta escalável para diferentes tipos de ambiente;
* Visualização clara por meio de protótipos e materiais gráficos.

---

## Status do projeto

> Projeto acadêmico em desenvolvimento.

Atualmente, o AETHER está em fase de concepção, documentação e prototipação visual. A implementação prática ainda está em desenvolvimento e representa uma primeira etapa para validar a ideia, a arquitetura e os possíveis fluxos do sistema.

---

## Próximos passos

* Melhorar a documentação técnica;
* Organizar os arquivos por disciplina;
* Adicionar imagens do protótipo;
* Criar telas simuladas do sistema;
* Desenvolver uma versão inicial funcional;
* Implementar dashboards;
* Simular dados ambientais;
* Testar a ativação dos modos do AETHER;
* Melhorar a apresentação do pitch.

---

## Equipe

Projeto desenvolvido por estudantes de Engenharia de Software da FIAP para a Global Solution 2026.

```md
Arthur Canaverde da Cruz
Isabella Jardim Marques
Mayene Moura da Silva
Murilo Canéstri dos Reis
```

---

## Licença

Este projeto foi desenvolvido para fins acadêmicos.

---
