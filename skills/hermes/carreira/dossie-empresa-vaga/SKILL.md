---
name: dossie-empresa-vaga
version: 1.0.0
author: Hermes (Benedito)
license: MIT
description: 'Use quando Igor pedir dossiê de empresa para uma vaga.'
metadata:
  hermes:
    tags: [carreira, glassdoor, entrevista, negociacao-salarial]
    related_skills: [web-research, browser-act, linkedin-optimization]
---

# Dossiê de empresa para oferta de vaga (Igor)

## When to Use

Dispare quando Igor oferecer/receber uma vaga e pedir dossiê da empresa: pesquisar no Glassdoor logado, pacote de benefícios, salários, notas e avaliações, perguntas para o recrutador, argumentos de negociação salarial, preparação de entrevista Dev Java Sênior ou perfil de executivo-chave (CTPO/CPO) no LinkedIn.

Classe de trabalho: Igor está em busca de emprego e periodicamente recebe ofertas; cada uma vira um pacote de arquivos. Idioma: SEMPRE pt-BR, nomes de arquivo sem acento. A fonte primária pedida é quase sempre o Glassdoor LOGADO na conta do Igor. Destino padrão: `~/MEGA/Documentos/oportunidades/<Empresa>/`.

## Ordem do trabalho

1. **Registrar o pedido** (protocolo da casa): Kanban `hermes kanban --board default create "<título>"` + linha em `~/clawd/PEDIDOS.md` com data/hora de início. Ler `~/MEGA/Regras/carreira.md` e `financas.md` antes de agir.
2. **Pesquisa web primeiro** (web_search em lote): o que a empresa faz, saúde financeira (receita, prejuízo, IPO/delisting, dívida, layoffs), notícias de 12 meses, benefícios divulgados em vagas — incluir uma busca de valores tipo `<empresa> vale alimentação R$ benefícios` e abrir a página de vaga oficial (Gupy) se aparecer — salários citados. Isso leva 3 minutos e valida os dados do Glassdoor depois; nos benefícios, os anúncios oficiais são a MELHOR fonte de valor, não a pior.
3. **Abrir a pasta e o rascunho do dossiê** em `~/MEGA/Documentos/oportunidades/<Empresa>/` (criar `INDEX.md` sempre). Escrever o achado de web ANTES de destravar o Glassdoor — se a extração travar, o trabalho já existe.
4. **Extrair Glassdoor logado** — ver `references/glassdoor-extracao-cdp.md`; use o driver pronto `scripts/cdp_extractor.py` (websockets + CDP, serve Glassdoor E LinkedIn). NÃO tentar vencer o Turnstile no browser do Hermes; use o Chrome clonado da máquina.
5. **Calcular a oferta centavo-exato** (INSS progressivo + IRRF, líquido, VA/auxílios, 13º+férias, sobra sobre o custo de vida de R$ 4.000) — parâmetros vigentes e o formato da saída em `references/calculo-clt-salarial.md`. Escrever o script em arquivo e rodar — nunca calcular de cabeça; valide o script reproduzindo um número já confirmado (ex.: recalcular um líquido que veio de outra fonte) antes de confiar nele. PLR só entra na conta se houver prova de pagamento real (pedir histórico).
6. **Quebrar em arquivos separados por contexto** (Igor pede isso explicitamente): dossiê, perguntas ao recrutador, argumentos de salário, preparação de entrevista, pessoas-chave (CTPO/CPO etc.), INDEX.md com status. NUNCA um único MD gigante. Quando o Igor pedir "em paralelo", disparar `delegate_task` com UM subagente por arquivo (tarefa independente): dar a cada filho o contexto completo embutido + a lista exata de arquivos para ler com read_file + o caminho de saída + 'NÃO mexa em Kanban/PEDIDOS'; o PAI valida cada arquivo (wc -l contra o alvo) e faz todo o bookkeeping — filho não fecha Kanban nem grava PEDIDOS.
7. **Fechar o ciclo**: patch em PEDIDOS.md (status ✅ + fim), `kanban complete <id> --result`, memória persistente (1 entrada compacta com os números-chave).
8. **Quando a vaga evolui para entrevista agendada**, registrar em `~/MEGA/Documentos/TAREFAS.md` (seção Profissionais, ID `TAR-AAAAMMDD-NNN`, nas visões ativas E no cadastro completo) e criar cron one-shot 30 min antes: `hermes cron create --name "Lembrete entrevista <empresa>" --deliver origin --repeat 1 "YYYY-MM-DD HH:MM" "<prompt>"`. Nunca registrar a entrevista só no chat.
9. **PACK de estudo único quando a entrevista se aproxima** (< 1 semana): consolidar TUDO num único MD que substitui os demais para o dia (cronograma de estudo dia a dia, ficha de 5 minutos com 3 frases da empresa + pacote de benefícios fixado + os 3 números do Igor, falas prontas de storytelling, N perguntas técnicas prováveis com resposta-chave em 2–3 linhas, perguntas comportamentais, perguntas pro recrutador priorizadas, script de negociação e checklist do dia). O pack é o ÚNICO que ele precisa estudar; os dossiês antigos ficam como profundidade. Duplicar o arquivo em `~/MEGA/Documentos/carreira/` (nomenclatura `YYYY-MM-DD_...`) — o Igor estuda também pelo celular e coleta os MDs de carreira.
10. **Leitura preparatória do líder-chave**: extrair a atividade completa dele no LinkedIn (`/recent-activity/all/` + scroll — ver `references/linkedin-pessoa-chave-cdp.md`) e destilar num MD: quem é (1 min), os N pilares da visão pública (com citações curtas), o que está construindo AGORA, e "golpes prontos" — como usar os conceitos dele na entrevista. Regra de uso: ESPELHE o vocabulário do líder (ex.: métrica favorita, nome que ele dá à plataforma) e conecte o histórico do Igor à tese dele; NUNCA cite que leu os posts de forma cangalheira ("li tudo seu") — use as IDEIAS naturalmente. Foto do entrevistador enviada pelo Igor: confere contra a foto de perfil do LinkedIn (vision nas duas) e registra o veredito no dossiê.
11. **Pacote de PDFs de leitura no celular** (a partir de < 1 semana da entrevista): converter os dossiês em PDFs com capa + outline + versão de letra grande, numerados em ordem de leitura com rótulo DOSSIE em todos os arquivos, e replicar no Google Drive — procedimento completo em `references/pdf-pacote-leitura.md`; builder validado em `templates/build_pdfs_leitura.py` (copie para scratch e adapte por empresa). Incluir SEMPRE o documento de perguntas-e-respostas (respostas modelo em 1ª pessoa com [CONFIRMAR] nos detalhes pessoais) e o dossiê da EMPRESA no pacote — não deixe faltar nenhum dos dois.

## Regras de sempre

- **Números exatos e fontes em todo dado**: nota, quantidade de avaliações, data de atualização. Sem fonte = não afirmar.
- **Banda salarial interna > oferta**: comparar a oferta com o próprio Glassdoor da empresa (percentis e registros individuais por cargo). "Banda fechada" abaixo do maior registro individual é argumento negociável.
- **Benefícios com valor real**: o VALOR em R$ (VA/VR/auxílios) quase nunca está na página de benefícios do Glassdoor (só notas) — a fonte primária é o anúncio oficial de vaga da própria empresa (Gupy/site de carreiras/LinkedIn Jobs), que lista os valores centavo a centavo; citações de funcionários servem de corroboração (a página de benefício por categoria do Glassdoor mostra a nota, "Confirmado pela empresa" e nº de funcionários que informaram — use para corroboração, não para o valor). Marcar PLR/variável como NÃO confiável sem histórico de pagamento. A proposta escrita é a fonte final — se o valor na proposta divergir do confirmado nos anúncios, refazer a conta.
- **Risco de estabilidade sempre avaliado**: layoffs, delisting, dívida, nota de liderança — o Igor negocia sabendo disso.
- **Pessoas-chave no LinkedIn logado** (Chrome clonado): CTPO/CPO/gestor do time; checar conexão em comum (SulAmérica, HDI, ex-colegas) e escrever mensagens rascunho para WhatsApp — mas NUNCA enviar nada sem aprovação explícita do Igor. Receita concreta de extração: `references/linkedin-pessoa-chave-cdp.md`.
- **Modo CLT vs PJ**: reescrever a análise financeira se a modalidade mudar; PJ pelo valor de um CLT é perda de ~R$ 2,5–3k/mês em direitos.
- Nunca registrar credenciais/tokens de sessão; login do Google só com aprovação 2FA do próprio Igor.

## Pitfalls

- **Nome de empresa ambíguo/coloquial (ex.: "Distro", "Distrito", apelidos): CONFIRMAR a identidade com o Igor (link do LinkedIn da empresa ou site) ANTES de extrair o Glassdoor** — nomes colidem entre empresas (fintech americana × importadora × plataforma) e o entrevistador citado também tem 30+ homônimos no LinkedIn; dossiê da empresa errada desinforma a negociação inteira. Uma busca web não resolve: use `clarify` com o Igor se a busca não cravar.
- Turnstile do Cloudflare no Glassdoor NÃO cede a cliques via CDP do browser do Hermes (desafio em iframe OOPIF) — cada tentativa custa minutos; vá direto para o Chrome clonado (ver reference).
- Clicar "Entrar com Google" no clone abre verificação em duas etapas: avisar o Igor ANTES (ele aprova a notificação no celular) e aguardar a aba do Google sumir — depois confirmar login no Glassdoor antes de navegar.
- Páginas logadas do Glassdoor têm sidebar gigante ("Empresas seguidas") no innerText — extrair `document.querySelector('main').innerText` ou fatiar a partir do título da seção, senão o arquivo bruto vira lixo de sidebar.
- Paginação de avaliações por URL `_P2.htm` costuma re-render a página 1; extraia o que a ordenação "mais relevantes" dá (5 avaliações completas + FAQ agregadas) e aceite — não gastar meia hora em loop de paginação.
- Links de salário por cargo usam sufixo `_D_KO7,27.htm` (salários) ≠ sufixo de avaliações (`_KO7,27.htm` sem `_D`); a URL certa sai das âncoras na página de salários da empresa.
