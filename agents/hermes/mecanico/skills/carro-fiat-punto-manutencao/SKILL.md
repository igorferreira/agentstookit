---
name: carro-fiat-punto-manutencao
description: "Use when handling maintenance, fuel consumption tracking, mechanical diagnostics, or legal documentation for Usuário's Fiat Punto ELX 2010 (plate [PLACA-REDACTADA]) under ~/MEGA/Documentos/Carros/FiatPuntoELX2010."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [carro, fiat, punto, mecanica, manutencao, combustivel, brasil]
    related_skills: []
---

# Carro: Fiat Punto ELX 2010 — Manutenção e Consumo

## Overview

Skill do agente `mecanico` (apelido **Rubens**) para controlar manutenção preventiva, diagnóstico mecânico e consumo de combustível do Fiat Punto ELX 1.4 8V de Usuário (placa [PLACA-REDACTADA], RENAVAM [RENAVAM-REDACTADO], ano fab./modelo 2009/2010, motor Fire Evo 1.4 8V flex).

Pasta base autorizada:

`/home/usuario/MEGA/Documentos/Carros/FiatPuntoELX2010`

Perfil recomendado: `mecanico`

## When to Use

Use quando Usuário mencionar:

- troca de óleo, filtro (óleo/ar/combustível/cabine), correia dentada, correia acessórios, velas, pastilhas/discos de freio, pneus, bateria, fluido de freio, arrefecimento;
- revisão programada ou "levar o carro na oficina";
- abastecimento, litros, quilometragem rodada, "quanto tá gastando de combustível";
- barulho, luz no painel, dificuldade de ligar, ou qualquer sintoma mecânico no Punto;
- IPVA, licenciamento, CRLV, SPVAT/DPVAT, vistoria do carro.

Não use para outros veículos sem antes confirmar com Usuário (esta skill é específica do Punto [PLACA-REDACTADA]).

## Estrutura de arquivos

```text
/home/usuario/MEGA/Documentos/Carros/FiatPuntoELX2010/
├── dados-veiculo.md                    # dados fixos do CRLV — não editar sem novo documento oficial
├── plano-revisoes-manutencao.md        # tabela de intervalos de manutenção (referência)
├── manutencoes-obrigatorias-legais.md  # IPVA, licenciamento, SPVAT, vistoria (RJ)
├── historico-manutencoes.md            # log real do que foi feito, sempre append
├── controle-consumo-combustivel.md     # log de abastecimentos + km/l calculado
└── abastecimentos/                     # fotos originais dos cupons/comprovantes de abastecimento
```

## Registro de manutenção (append-only)

Ao registrar um serviço em `historico-manutencoes.md`, sempre no formato de tabela Markdown, adicionando uma linha nova (nunca reescrever linhas antigas):

`| Data | KM | Serviço | Peça/Oficina | Valor (R$) | Próxima troca prevista (KM) |`

Depois de registrar, recalcule e avise se algum item crítico está próximo ou vencido (ver tabela de intervalos abaixo).

## Intervalos de manutenção — Fiat Punto 1.4 8V Fire/Fire Evo

Fonte: manuais do proprietário, planos de revisão Fiat e consenso de oficinas/fóruns especializados (PuntoClube, Sua Oficina Online). Sempre priorize o adesivo de revisão no vão do motor ou o manual físico do carro se divergir daqui.

| Item | Intervalo | Observação |
|---|---|---|
| **Correia dentada + tensor** | **60.000 km** (ou ~5 anos) | **CRÍTICO**: se arrebentar, motor pode ser destruído (colisão pistão/válvula). Trocar tensor e correia de acessórios junto. Verificação intermediária recomendada aos 15.000 km do último troca. |
| Óleo do motor + filtro de óleo | 10.000 km ou 1 ano (sintético/semissintético); a cada 5.000–7.500 km se mineral | Verificar tipo de óleo usado na última troca antes de decidir o intervalo. |
| Filtro de ar | ~10.000 km | Junto com troca de óleo é prático. |
| Filtro de combustível | ~10.000 km | |
| Revisão programada completa | A cada 10.000 km (modelos 2014+) ou 7.500 km/1 ano (padrão anterior a 2014, caso do Punto 2010) | Inclui checagem de freios, direção, suspensão, elétrica. |
| Velas de ignição | 20.000–30.000 km (flex desgasta mais rápido que gasolina pura) | |
| Fluido de freio | A cada 2 anos, independente da km | Fluido é higroscópico (absorve água) mesmo parado. |
| Pastilhas de freio dianteiras | 20.000–40.000 km (varia muito com uso urbano) | Verificar por desgaste/ruído, não só por km. |
| Fluido de arrefecimento | ~2 anos ou 30.000–40.000 km | |
| Correia de acessórios (alternador/AC) | Junto com a correia dentada, ou antes se ressecada/trincada | |
| Pneus — rodízio/alinhamento/balanceamento | ~10.000 km | |
| Bateria | 2–4 anos | Vida útil menor com uso urbano de paradas curtas. |

## Cálculo de consumo de combustível

Fórmulas:

- **Consumo (km/l)** = KM rodados ÷ litros abastecidos
- **Custo por km** = valor total pago ÷ KM rodados
- **Autonomia estimada do tanque** = capacidade do tanque (L) × km/l calculado

Sempre que Usuário informar um abastecimento (litros + valor, e KM do odômetro no momento), registre uma linha nova em `controle-consumo-combustivel.md`:

`| Data | KM odômetro | Litros | Combustível | Valor (R$) | KM rodados desde último | Consumo (km/l) | R$/km | Comprovante |`

## Abastecimento por foto (OCR)

Usuário normalmente vai enviar o abastecimento como **foto do cupom/comprovante do posto**, não como texto. Fluxo obrigatório ao receber uma foto de abastecimento:

1. **Ler a imagem** (visão nativa do modelo / ferramenta de OCR disponível) e extrair o que o cupom mostrar: data/hora, litros, valor total, preço por litro, tipo de combustível (álcool ou gasolina — cupom de posto costuma indicar), nome do posto/bandeira.
2. **Cupom de posto normalmente NÃO mostra o KM do odômetro.** Se a foto (ou a mensagem que a acompanha) não trouxer a quilometragem atual, **pergunte a Usuário a KM do odômetro no momento do abastecimento** antes de calcular o consumo — não estime nem deixe em branco sem avisar.
3. **Salvar o arquivo original** da foto em `abastecimentos/`, nomeado como:
   `AAAA-MM-DD_ABASTECIMENTO-KM<odometro>-R<valor>.ext` (ex.: `2026-07-25_ABASTECIMENTO-KM149200-R18000.jpg`; usar o valor sem vírgula/ponto, ex. R$ 180,00 → `R18000`).
4. **Calcular** km rodados (KM atual − KM do abastecimento anterior registrado), consumo (km/l) e R$/km.
5. **Registrar a linha** em `controle-consumo-combustivel.md`, incluindo na coluna `Comprovante` o link relativo para o arquivo salvo em `abastecimentos/`.
6. **Comparar** o km/l calculado com a faixa de referência do Punto (tabela abaixo) e avisar Usuário se o consumo estiver fora do esperado.
7. Não inventar nenhum dado que não veio do cupom nem de Usuário — se algo do cupom estiver ilegível na foto, marcar como "não identificado" e perguntar se for um dado essencial (litros, valor, KM).
8. Antes de responder, confirmar (via `ls`/leitura do arquivo) que a foto foi salva e a linha foi adicionada corretamente.

### Médias de referência (Punto 1.4 8V Fire Flex, Inmetro + relatos de proprietários)

| Combustível | Cidade | Estrada |
|---|---|---|
| Etanol | ~6,5 a 7,5 km/l | ~8,5 a 10 km/l |
| Gasolina | ~9,5 a 11 km/l | ~12 a 14 km/l |

Regra prática de bico: com etanol até ~70% do preço da gasolina no posto, etanol compensa; acima disso, gasolina compensa (pela relação de consumo ~30% pior do etanol). Use isso para orientar Usuário sobre qual combustível abastecer, se ele perguntar.

Consumo muito abaixo da faixa acima pode indicar: pneus murchos, filtro de ar sujo, velas gastas, bicos sujos, uso excessivo de ar-condicionado em trânsito parado, ou problema de injeção — sugerir diagnóstico se for recorrente.

## Documentação legal obrigatória (RJ)

Ver `manutencoes-obrigatorias-legais.md` para detalhes e valores. Resumo: IPVA (DARJ, cota única ou 3x), licenciamento anual + CRLV-e (GRT), SPVAT (reativado desde jan/2025, pago via Caixa), vistoria/laudo de gases quando aplicável. Sem esses em dia, o CRLV não é emitido e o carro fica irregular para circular.

## Diagnóstico — abordagem

Ao ouvir um sintoma, siga a lógica de mecânico experiente:
1. Pergunte contexto mínimo se faltar: km atual, há quanto tempo começou, se piora com o motor frio/quente, se tem luz acesa no painel.
2. Dê 2-3 hipóteses mais prováveis, da mais comum para a mais rara.
3. Diga se é seguro continuar rodando até resolver, ou se deve parar e levar na oficina imediatamente (ex.: luz de óleo acesa, barulho metálico forte, cheiro de queimado = não rodar).
4. Se for algo simples e verificável em casa (nível de óleo, calibragem de pneu, fusível), oriente o passo a passo.
