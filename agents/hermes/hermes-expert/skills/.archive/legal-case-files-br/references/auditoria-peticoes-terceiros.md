# Auditoria de petições recebidas de terceiros — protocolo da banca

Como auditar uma peça que outro advogado redigiu (ex.: exceção de pré-executividade do Dr. Hélio no caso Maricá, recebida em 09/09/2026) antes de protocolar, defender ou sugerir correções.

## Pipeline (ordem fixa)

1. **Extrair o texto completo** — `pdftotext`. Se escaneado (Creator/Producer = CamScanner, Office converter etc.), o texto vem com artefatos: espaços quebrados, zero no lugar de "o" ("ao0 final"), acentos partidos. Distinguir artefato de OCR vs erro real do advogado.
2. **Medir o formato antes de criticar** — `pdffonts` (fonte real: Times vs Arial), `pdfinfo` (A4, páginas, creator). Cada advogado tem seu padrão; a auditoria julga a peça pelo próprio estilo dela, não pelo de outro advogado do caso.
3. **Conferência numérica automatizada (o achado nº 1)** — para toda data afirmada na peça, calcular o intervalo real com datetime e comparar com o que a peça afirma por extenso. Caso real: a mesma saída societária (2007) aparecia como "19 anos", "10 anos" e "2 anos" em blocos diferentes — erro invisível a olho nu, detectado por script em 1 minuto.
4. **Cross-check com a estratégia canônica do caso** — valores (CDA, inscrição, valores de bloqueio), OAB do advogado, datas-marcos e teses já descartadas tecnicamente (ex.: forçar prescrição quando ela não se consumou). Peça que contradiz a tese forte do caso = achado de primeiro nível.
5. **Red team adversarial** — ler como a Procuradoria: onde rebater em 3 linhas? Valores divergentes não explicados (execução inicial × ordem de bloqueio atual)? Endereçamento a vara/órgão com nomenclatura inexistente? Qualificação da parte desatualizada?
6. **Relatório estruturado** — nota 0-10 + veredito de uma linha no topo ("tese forte, forma com falhas graves"); depois erros GRAVES (credibilidade/protocolo), falhas MÉDIAS (enfraquecem), pontos FORTES (manter); terminar com checklist acionável e impacto financeiro/prazo (ex.: janela até a próxima reiteração SISBAJUD — a urgência real).

## Verificações específicas de execução fiscal

- Instrumento correto: exceção de pré-executividade (ilegitimidade passiva, matéria de ofício, Súmula 393/STJ, Tema 108) — NÃO petição intercorrente. Nome do arquivo errado pode induzir protocolo com instrumento trocado.
- Teses a checar contra a memória do caso: prescrição da cobrança (art. 174 CTN) só se consumou? Prescrição intercorrente (art. 40 LEF) já? Decadência do sócio retirante (arts. 1.003 § único e 1.032 CC) desenvolvida?
- Documentos que precisam constar anexados: procuração, certidão do registro mercantil, QSA Receita, comprovantes de bloqueio (por banco, com valor individual).
- Prazo-câncer: reiterações automáticas de bloqueio (SISBAJUD "teimosinha", 30 dias) — calcular a próxima data e marcar como janela de urgência da tutela.

## Regras de entrega

- Auditoria é documento interno — NUNCA protocolar; rotular "documento de auditoria interna".
- Enviar ao advogado autor somente em PDF (nunca .md) e como checklist de correção, não como ordens.
- Formato do arquivo: `AUDITORIA_<TIPO>_<AUTOR>_V1_<YYYYMMDD>.md` na pasta `peticao/` do processo (mantém a convenção do acervo sem colidir com as versões da peça V1..Vn).
