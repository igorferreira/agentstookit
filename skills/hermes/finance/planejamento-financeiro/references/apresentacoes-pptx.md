# Apresentações de análises financeiras (estatísticas + gráficos + PPTX)

Pipeline para pedidos como "cria análises estatísticas e uma apresentação explicando" sobre um arquivo canônico (GASTOS-*.md, fluxo de caixa, cartões). Fonte única: a tabela de registros do MD canônico — nunca recontar valores da memória da sessão.

## Pipeline

1. **Estatísticas primeiro, em script Python puro** (stdlib `collections` + `statistics` + `re`): parsear as linhas da tabela com regex ancorada no HEADER da tabela (ex.: `| Data | Local | ... Valor |`), nunca por posição fixa. Derivar por registro: ano/mês/dia-da-semana (via `datetime.date`), duração (horário entrada–saída, com +=24h se negativo), valor. Produzir: total geral/por ano/mês, por local, por dia de semana, por faixa de duração, dias com 2+ eventos (consolidáveis), top N mais caros, projeção anual.
2. **Anexar a seção de análises no PRÓPRIO MD canônico** (patch, não sobrescrever — o arquivo é append-friendly do vigia): tabelas por dimensão + bullets de leitura + dicas de redução ordenadas por impacto com economia estimada + tabela de metas (ritmo atual / fácil / agressivo).
3. **Gráficos PNG com matplotlib** (`matplotlib.use("Agg")` antes de tudo, `dpi=150`, figsize ~9×4.2) numa subpasta `charts_<tema>/` ao lado do MD — reutilizáveis pelo dashboard depois. Um PNG por dimensão: série mensal (destacar pico em vermelho + linha de média), dia da semana (barh), faixas de duração (2 painéis: nº e R$), comparação direta de custo/hora entre locais, cenários de economia.
4. **Deck 16:9 com python-pptx**: `prs.slide_width = Inches(13.333)`, `slide_height = Inches(7.5)`, layout BLANK; barra de título colorida por tema (shape cheio + texto branco); KPI cards como shapes arredondados; 1 ideia por slide com título-veredito ("BarraShopping custa 2× o Park", não "Locais"). Gráficos embutidos com `add_picture(..., width=Inches(9.1))` centrados.
5. **Salvar junto ao MD canônico**: `<tema>-apresentacao.pptx` no mesmo diretório (NÃO no `./out/` da convenção genérica de deck), nome sem acentos.
6. **Verificar antes de entregar**: reabrir o pptx (`Presentation(path)`, contar slides e imagens por shape_type==13) e inspecionar CADA PNG com visão antes de embutir — título com caractere quebrado só se pega olhando.
7. **Entrega no Telegram**: linha `MEDIA:/caminho/do/arquivo.pptx` na resposta (chega como arquivo nativo).

## Pitfalls

- **NUNCA montar texto de gráfico com encadeamento de `.replace()`** — escreva a string final direta no código. O hack `"...sa}bado...".replace("}", "á")` produziu "saábado" no título e só foi pego na verificação visual.
- **Gerar charts/deck via `terminal` com o python do venv Hermes, não via `execute_code`** — o intérprete do sandbox do execute_code não traz matplotlib nem python-pptx (instalados no venv e em /usr/bin/python3.12 --user); rodar no sandbox garante ModuleNotFoundError e 2 voltas perdidas.
- **Contas com meses parciais:** média mensal e projeção anual precisam declarar a base (ex.: "9 meses, jan–set") — projetar com base parcial sem avisar infla o número.
- **Regra de negócio do Igor em análises de redução:** dicas devem concentrar/otimizar comportamento, não mandar cortar lazer fixo intocável (Claro, IA, academia — ver seção Orçamento) nem deixar de sair; economia estimada por dica, do maior para o menor impacto.
