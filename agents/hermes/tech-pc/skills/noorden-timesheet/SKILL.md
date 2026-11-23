---
name: noorden-timesheet
description: Preenche a planilha de horas da Noorden com dados do sistema da HDI
version: 2.0.0
category: productivity
---

# Preenchimento de Timesheet Noorden

Fluxo mensal: as horas lançadas no sistema da HDI são transferidas para a planilha da Noorden e enviadas por e-mail.

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
- **Pasta das planilhas:** `/home/igorferreira/MEGA/Documentos/09_Timesheets/`
- **Template base:** último arquivo preenchido do mês anterior (NUNCA o template em branco)
- **Padrão de nomenclatura:** `Controle horas Noorden - <MÊS> <ANO> - igor dos santos ferreira.xlsx`

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

Anexar a planilha `.xlsx`.

## Verificação Final (checklist)

Antes de enviar, confirmar TODOS estes itens:
- [ ] B1 = `igor dos santos ferreira`, B2 = `HDI`, B3 = `Arquitetura IA`
- [ ] Fins de semana: colunas D-G VAZIAS (não "00:00:00")
- [ ] Feriados: coluna C com formato `Feriado -  <nome>`, D-G VAZIAS
- [ ] Dias trabalhados: C = `Desenvolvimento ` (com espaço), D=09:00, E=12:00, F=13:00, G=18:00
- [ ] Fórmulas H, K, N presentes nos dias trabalhados
- [ ] Fórmulas SUM com range correto (H7:H37 para 31 dias, H7:H36 para 30)
- [ ] Arquivo salvo com nome: `Controle horas Noorden - <MÊS> <ANO> - igor dos santos ferreira.xlsx`
