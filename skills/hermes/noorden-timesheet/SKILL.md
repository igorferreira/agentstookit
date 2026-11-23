---
name: noorden-timesheet
description: Preenche a planilha de horas da Noorden com dados do sistema da HDI
version: 2.0.0
category: productivity
---

# Preenchimento de Timesheet Noorden

Fluxo mensal: as horas lançadas no sistema da HDI são transferidas para a planilha da Noorden e enviadas por e-mail.

## Roteamento de intenção (antes de qualquer operação em arquivo)

As palavras-chave abaixo indicam que esta skill pode ser relevante; não autorizam, por si só, editar uma planilha ou enviar e-mail. Use o contexto para separar localizar o agente de executar o fluxo mensal. Se Igor pedir onde está o agente existente, informe o perfil `hr-tech-senior` (alias `rh`) e esta skill em `~/.hermes/skills/noorden-timesheet/SKILL.md`; não altere a planilha nem envie e-mail. Se a intenção ou o mês não estiver claro, pergunte antes de modificar arquivos. Dados já preenchidos, ou apenas ler uma planilha, não autorizam alterações. E-mail só após aprovação explícita do conteúdo final e do anexo.

## Trigger

- Quando Igor disser "timesheet", "planilha de horas", "Noorden", "horas HDI"
- Quando chegar e-mail da Ariane Oliveira (Projetos Noorden) cobrando a planilha
- Quando Igor enviar as horas lançadas no sistema da HDI

## Contexto

- **Empresa:** Noorden Services
- **Cliente:** HDI (São Paulo)
- **Projeto:** Arquitetura IA
- **Calendário de feriados:** São Paulo/SP (não RJ)
- **Responsável Noorden:** Ariane Oliveira (arianeoliveira@noorden.com.br)
- **E-mail Projetos:** projetos@noorden.com.br
- **E-mail do Igor (cópia):** igorferreirabr@gmail.com
- **Pasta das planilhas:** `/home/igorferreira/MEGA/Documentos/trabalho_projetos_ti/timesheets/` (⚠️ NÃO `09_Timesheets` — a pasta real é essa, dentro de trabalho_projetos_ti)
- **Template base:** último arquivo preenchido do mês anterior (NUNCA o template em branco)
- **Padrão de nomenclatura:** `Controle horas Noorden - <MÊS> <ANO> - igor dos santos ferreira.xlsx`
- **Gerador automático de meses:** `trabalho_projetos_ti/timesheets/gerar_timesheet_noorden_2026.py` — cria Ago–Dez/2026 pré-preenchidos com 8h de "Desenvolvimento", respeitando feriados SP

## ⚡ Gerar meses inteiros (Ago–Dez/2026)

Quando Igor pedir "crie as planilhas do ano" (ou pré-preencher), rodar o script que replica o padrão exato de julho:

```bash
python3.12 /home/igorferreira/MEGA/Documentos/trabalho_projetos_ti/timesheets/gerar_timesheet_noorden_2026.py
```

O script:
1. Copia o arquivo de **Julho/2026** (template de 31 dias) como base → preserva merged cells, estilos e fórmulas.
2. Para cada mês (Ago–Dez): atualiza `B4` (1º dia do mês), reescreve dias/semana, aplica feriados SP, ajusta `SUM(H7:H<n>)` conforme dias do mês.
3. **Feriados SP 2026 aplicados:** 07/09 Independência, 12/10 Aparecida, 02/11 Finados, 15/11 Proclamação, 20/11 Consciência Negra, 25/12 Natal.

Feriados formatados exatamente como julho: `Feriado -  <nome>` (dois espaços após o hífen), colunas D–G e H **vazias** (None), e colunas I–N com `00:00:00` + fórmulas `=J-I`/`=M-L`.

## Regras de Ouro

Estas regras vêm da comparação com a planilha preenchida manualmente pelo Igor. **NUNCA viole estas regras:**

1. ⚠️ **Fins de semana e feriados:** colunas D, E, F, G, H ficam **VAZIAS** (None). NUNCA escrever "00:00:00".
2. ⚠️ **Atividade:** `Desenvolvimento ` com **espaço no final**.
3. ⚠️ **Feriado:** coluna C = `Feriado -  <nome do feriado>` (ex: `Feriado -  Revolução Constitucionalista de 1932`). Notar os DOIS espaços após o hífen.
4. ⚠️ **Cabeçalho (B1-B4):** B1=`igor dos santos ferreira`, B2=`HDI`, B3=`Arquitetura IA`, B4=date do 1º dia do mês.
5. ⚠️ **Template:** SEMPRE usar o arquivo preenchido do mês anterior. NUNCA o template em branco.

## Procedimento

### 1. Receber as horas do sistema HDI

Igor vai passar as horas em formato livre. Pode ser:
- Lista de dias com horas (ex: "dia 1 - 8 horas")
- Screenshot/print do sistema
- Texto corrido

### 2. Identificar o mês de referência

Confirmar com Igor qual mês está sendo preenchido.

### 3. Verificar feriados SP no mês

- SP: 09/07 (Revolução Constitucionalista), 20/11 (Consciência Negra)
- Nacionais: 01/01, 21/04, 01/05, 07/09, 12/10, 02/11, 15/11, 25/12
- Móveis: Sexta-feira Santa, Corpus Christi

### 4. Criar a planilha — MÉTODO CORRETO

**Copiar o arquivo do mês anterior e editar.** Isto garante que merged cells, fórmulas e estrutura estejam 100% corretas.

```python
import shutil
src = f"Controle horas Noorden - <MÊS ANTERIOR> <ANO> - igor dos santos ferreira.xlsx"
dst = f"Controle horas Noorden - <MÊS> <ANO> - igor dos santos ferreira.xlsx"
shutil.copy2(src, dst)
```

Depois editar o arquivo copiado:

1. **Atualizar cabeçalho:**
   - B1 = `igor dos santos ferreira`
   - B2 = `HDI`
   - B3 = `Arquitetura IA`
   - B4 = `date(ano, mês, 1)`

2. **Ajustar número de dias:**
   - Se mesmo número de dias do template → pular
   - Se 31 dias (template 30): desfazer merged cells (linhas 37+), shiftar 37→38 até 42→43, limpar linha 37, refazer merged cells em 38+, corrigir fórmulas SUM (H7:H36→H7:H37 etc.)
   - Se 28/29 dias: remover linhas excedentes, ajustar merged cells e fórmulas

3. **Limpar dados do mês anterior:**
   - Para cada linha de dados (7 até 37): limpar colunas C, D, E, F, G (A e B serão reescritas)

4. **Preencher dias:**
   - Coluna A = número do dia (1-31)
   - Coluna B = dia da semana em português

5. **Aplicar os dados da HDI:**
   - Para cada dia com horas > 0 e não feriado:
     - C = `Desenvolvimento ` (com espaço no final!)
     - D = `09:00:00`, E = `12:00:00`, F = `13:00:00`, G = `18:00:00`
     - Colunas H, K, N = manter fórmulas (já existentes do template)
   - Para feriados:
     - C = `Feriado -  <nome>` (ex: `Feriado -  Revolução Constitucionalista de 1932`)
     - D, E, F, G, H, K, N = **limpar (None)**
   - Para fins de semana:
     - C, D, E, F, G, H, K, N = **limpar (None)**
   - Para dias úteis sem hora (ausência/férias):
     - C = `Não trabalhado`
     - D, E, F, G = `00:00:00`

6. **Verificar:**
   - Contar dias com "Desenvolvimento " na coluna C
   - Somar horas: dias × 8h
   - Verificar que NENHUMA célula de fim de semana/feriado tem "00:00:00" nas colunas D-G

### 4b. Preenchimento parcial do mês

Quando Igor ditar as horas em formato livre (ex.: "8h/dia até sexta dia 13, 0h nos dias seguintes"), isso é a evidência válida (mesmo caso do passo 1) — não exigir export do HDI. Aplicar as horas ditadas aos dias informados e preencher TODO dia útil restante do mês com o padrão de ausência do passo 5 (C = `Não trabalhado`, D–G = `00:00:00`); fins de semana e feriados seguem as Regras de Ouro inalteradas. Feriado que cai em fim de semana mantém o rótulo `Feriado -  <nome>` na coluna C com D–H vazias — não apagar o rótulo só porque é domingo.

### Gotchas de edição (openpyxl)

- Rodar openpyxl pelo Python do venv do Hermes (`~/.hermes/hermes-agent/venv/bin/python`) — o `python3` do sistema não tem o pacote.
- Escrever horários como TEXTO (`'09:00:00'`, `'00:00:00'`), nunca `datetime.time` — o template pré-gerado armazena os horários como strings e misturar tipos quebra a comparação/validação.
- Copiar o arquivo original para `backup_<data>_...xlsx` na mesma pasta ANTES da primeira edição.
- Validador: checar fim de semana ANTES de feriado, senão um feriado em domingo gera falso erro "fim de semana com conteúdo".

### 5. Enviar para aprovação

- Mostrar resumo (dias trabalhados, feriados, total de horas)
- Listar dias que NÃO estão no sistema HDI (se houver)
- Perguntar se Igor aprova
- Se aprovado, responder ao e-mail da Ariane com a planilha anexa

### 6. Envio do e-mail

```
Assunto: Re: URGENTE NOORDEN - planilha horas prestação de serviço - <MÊS> <ANO>

Olá Ariane,

Segue em anexo a planilha de horas de <MÊS>/<ANO>.

Total de horas normais: <X>h
Dias úteis: <Y>
Feriados: <Z>

Qualquer dúvida estou à disposição.

Atenciosamente,
Igor Ferreira
```

Anexar a planilha `.xlsx`. Envio: montar um `.eml` completo (EmailMessage com anexo base64) e enviar POR STDIN — `himalaya message send -a <conta> < arquivo.eml`. Passar o caminho do arquivo como ARGUMENTO não lê o arquivo: o binário interpreta o caminho como conteúdo e panica no mail-parser (`index out of bounds`). Confirmar a cópia em `envelope list --folder Sent` antes de reportar enviado.

## Verificação Final (checklist)

Antes de enviar, confirmar TODOS estes itens:
- [ ] B1 = `igor dos santos ferreira`, B2 = `HDI`, B3 = `Arquitetura IA`
- [ ] B4 = 1º dia do mês (datetime)
- [ ] Fins de semana: colunas C–H VAZIAS (não "00:00:00")
- [ ] Feriados: coluna C com formato `Feriado -  <nome>`, D–H VAZIAS
- [ ] Dias trabalhados: C = `Desenvolvimento ` (com espaço), D=09:00, E=12:00, F=13:00, G=18:00
- [ ] Fórmulas H, K, N presentes nos dias trabalhados (I,J,L,M = 00:00:00 em TODOS os dias)
- [ ] Fórmulas SUM com range correto (H7:H37 para 31 dias, H7:H36 para 30)
- [ ] Células mescladas preservadas: A6:B6, E6:F6, F38:G38, I38:J38, L38:M38, A43:C43
- [ ] Arquivo salvo com nome: `Controle horas Noorden - <MÊS> <ANO> - igor dos santos ferreira.xlsx`
