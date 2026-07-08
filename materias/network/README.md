# Network Architect Solutions

Esta pasta contém a entrega da disciplina de **Network Architect Solutions**, desenvolvida para o projeto **AETHER** na **Global Solution 2026**.

## Sobre a entrega

Nesta etapa, o foco foi planejar uma infraestrutura de rede para uma escola localizada em uma região remota do Brasil, considerando dificuldades reais de conectividade, distância urbana, floresta densa, baixa cobertura móvel e ausência de infraestrutura cabeada.

A solução proposta utiliza conexão via satélite com **Starlink**, combinada com uma rede local segmentada para atender os ambientes acadêmicos e administrativos da escola.

## Conteúdo

* Análise da região escolhida;
* Justificativa da dificuldade de conectividade;
* Escolha da solução via satélite;
* Planejamento de sub-redes;
* Separação entre rede acadêmica e administrativa;
* Definição de equipamentos de rede;
* Topologia lógica no Cisco Packet Tracer;
* Representação física dos ambientes da escola;
* Impacto social da conectividade.

## Região escolhida

A região analisada foi **São Gabriel da Cachoeira — Amazonas (AM)**, um município localizado em uma área de difícil acesso, com grande extensão territorial, comunidades afastadas e limitações de infraestrutura de telecomunicações.

## Solução proposta

A infraestrutura planejada utiliza:

* Antena Starlink como link WAN;
* Roteador Cisco 1941 como núcleo da rede;
* Switches Cisco Catalyst 2960;
* Rede Acadêmica;
* Rede Administrativa;
* DHCP configurado por sub-rede;
* Segmentação da rede com máscara `/26`.

## Documento

[Ver PDF da entrega](./network-aether.pdf)

> Caso o arquivo esteja com outro nome no repositório, atualize o link acima.

## Estrutura da pasta

```bash
network/
│
├── README.md
└── network-aether.pdf
```

## Voltar

[Voltar para o README principal](../../README.md)
