# Playbook de Negociação de Cartões

## Quando usar

Quando o usuário decidir não pagar um grupo de cartões e precisar de um guia completo de negociação com:
- Lista de cartões por emissor (agrupados)
- Canais de contato (telefones, portais, apps)
- Cronograma de negociação (fases de 30-60-90-180 dias)
- Simulação de acordos com descontos
- Cuidados e checklist

## Estrutura do documento

### 1. Visão Geral
Resumo executivo: quantos cartões mantidos vs negociação, valor total, reserva disponível.

### 2. Cartões para Negociação
Agrupar por **emissor** (não por marca):
- **Grupo 1 — Banco PAN**: Méliuz + Buscapé → mesmo emissor, negociar juntos
- **Grupo 2 — Bradescard**: Casas Bahia + C&A + Atacadão → portal único
- **Grupo 3 — Fintechs**: RecargaPay, Inter, PicPay, Digio (individuais)
- **Grupo 4 — Outros**: BrasilCard

Incluir valor total por grupo para priorização.

### 3. Canais de Negociação por Emissor
Para cada emissor, tabela com:
- Portal de renegociação (URL)
- App (caminho no menu)
- Telefone (capitais e 0800)
- WhatsApp
- SAC e Ouvidoria
- Horário de atendimento

### 4. Cronograma (4 fases)

| Fase | Quando | Ação |
|---|---|---|
| 1 — Deixar vencer | Mês 1 | Não pagar nada, silenciar notificações |
| 2 — Primeiras ofertas | 30-60 dias | Ofertas aparecem, NÃO aceitar |
| 3 — Negociação real | 90-120 dias | 🎯 Momento ideal, 70-95% desconto |
| 4 — Quitação | Mês 4-6 | Pagar acordos com reserva acumulada |

### 5. Estratégias por Emissor
Para cada grupo:
- **Abordagem**: negociar juntos ou separados?
- **Meta de desconto**: % realista baseado no histórico do emissor
- **Valor-alvo**: simulação com desconto aplicado

### 6. Simulação de Acordos
Tabela: Cartão → Dívida → Desconto est. → Valor acordo → % pago

> **⚠️ Exemplo histórico (31/07/2026) — números desatualizados.** Base de negociação era R$ 60.451 (naquela data); hoje ver `~/MEGA/Comprovantes/ENDIVIDAMENTO.md` seção 4 para os cartões e valores atuais em negociação. Mantido só para ilustrar o formato da simulação.

Exemplo real (31/07/2026):
```
RecargaPay:  R$ 14.254 × 85% = R$ 2.138 (15%)
PAN (3 cart): R$ 19.587 × 90% = R$ 1.959 (10%)
Bradescard:  R$  9.456 × 90% = R$   946 (10%)
...
TOTAL:       R$ 60.451       → R$ 7.703 (13%)
```

### 7. Cuidados
- ✅ Salvar print de todas as ofertas
- ✅ Negociar sempre por escrito (portal/app)
- ✅ Pagar acordos só com boleto/PIX identificado
- ❌ Não pagar 1ª oferta (esperar 60-90 dias)
- ❌ Não negociar por telefone sem gravar

## Pesquisa de canais de contato

Para cada emissor, buscar no Google:
- `"[nome do emissor]" negociação dívida telefone SAC`
- `"[nome do emissor]" renegociação portal`

Fontes confiáveis: site oficial do emissor, Reclame Aqui, Mobills, iDinheiro.

Priorizar:
1. Portal/app oficial (melhores ofertas)
2. Telefone de negociação dedicado
3. SAC genérico
4. Ouvidoria (último recurso)

## Entrega

Gerar Markdown + PDF (pandoc → wkhtmltopdf). Salvar na pasta mensal como:
`AAAA-MM-DD_PLAYBOOK-NEGOCIACAO-CARTOES.md` / `.pdf`
