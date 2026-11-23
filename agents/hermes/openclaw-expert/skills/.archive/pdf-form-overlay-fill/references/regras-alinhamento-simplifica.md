# Regras de alinhamento — Requerimento Simplifica Maricá (03/09/2026)

Três correções explícitas do Igor nesta sessão, que valem para QUALQUER formulário de overlay:

## REGRA Nº1 — Centralizar na banda vazia ABAIXO do rótulo
Igor rejeitou 3x o mesmo erro: texto colocado na MESMA altura / colado em cima do título do campo ("ainda está muito colado em cima ou junto do título do campo").
- Cada rótulo (etiqueta) ocupa a PRÓPRIA linha no topo da célula.
- O valor vai na **faixa em branco (banda vazia) entre a linha do rótulo e a linha-guia de baixo**.
- Baseline central da banda: `baseline = (y0 + y1) / 2 + size * 0.28`.
- As células de um formulário são baixas (rótulo quase toca a linha) — por isso texto com fonte 10-11 não pode ser posto na altura do rótulo: transborda verticalmente e invade a etiqueta.

## REGRA Nº2 — Campos da mesma linha: MESMO baseline e MESMO fontsize
Igor: "DETRAN-RJ desalinhado/vazando". Causa: reduzi a fonte de um único campo (ÓRGÃO "DETRAN-RJ" em 9 em vez de 10).
- Todos os campos de UMA MESMA linha (ex.: RG / ÓRGÃO / DATA / CPF) DEVM ficar no MESMO baseline e com o MESMO fontsize.
- Verificação: extrair spans com `page.get_text('dict')` e conferir que os y0/y1 das células da mesma linha batem (ex.: todos y0=191.25, y1=202.42).
- Se o texto não couber, reduza a fonte de TODOS os campos da linha igualmente — nunca de um só.

## REGRA Nº3 — Centralizar horizontalmente sob o center_x do rótulo
- Alinhar sob o CENTRO do rótulo da coluna, não à esquerda, nem deixar o texto vazar a divisória à direita da coluna.
- Use as divisórias verticais do formulário (`get_drawings` linhas verticais) para saber onde cada coluna começa/termina.
- Medir a largura do texto com `fitz.Font(fontfile=FONT).text_length(text, fontsize=size)` — `fitz.get_text_length(fontname=...)` FALHA (usa nome interno da fonte, não caminho).

## Duas versões OBRIGATÓRIAS do PDF preenchido
O Igor pediu explicitamente: gerar **2 versões**:
1. **SEM assinatura + SEM data** → para assinar à mão ao imprimir (padrão p/ órgão público).
2. **COM assinatura + data** → quando houver assinatura digital disponível.
- Assinatura inserida com `page.insert_image(rect, filename=sig.png, keep_proportion=True)` centralizada no campo ASSINATURA, proporção preservada.

## Assinatura digital limpa — fonte preferida
- A assinatura limpa do Igor está no **DocuSign** (Perfil → Assinaturas, `account.docusign.com/me/signatures`) como imagem renderizada (fonte manuscrita). É a oficial/legível.
- Clicksign NÃO guarda imagem de assinatura no perfil (só dados de acesso). DocuSign sim (aba Assinatura).
- NÃO usar cartão de assinaturas de pessoa jurídica (é rabisco de representante, sai "legal não" / denso).