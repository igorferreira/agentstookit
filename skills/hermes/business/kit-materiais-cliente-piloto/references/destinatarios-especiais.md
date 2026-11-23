# Perfis de destinatários não-piloto (validado 04/09/2026)

Nem todo kit é para cliente-piloto. Três perfis extras surgiram e têm pipelines distintos:

## 1. Parceiro estratégico (ex.: Rafael Alcemar/Webdec, Fernando Veronez)
- NÃO é cliente-piloto: recebe kit "parceiro".
- Conteúdo: deck "O Projeto" (produto, pacotes, pilotos, tese de parceria) + deck "Como Construímos" (jornada, arquitetura, segurança) + roteiros de áudio + logos.
- Tese de parceria: vertical (negócio do parceiro) × horizontal (multi-segmento); modelos: indicação/white-label/JV/integração técnica.
- Proposta societária SÓ em 2ª rodada, após interesse demonstrado.
- Tom: colega de profissão, respeitando senioridade — nunca pitch de vendas.
- Traçar perfil completo via web_search antes (cargo, empresa/CNPJ, formação, presença digital, números públicos) e salvar ficha em `05-execucao-clientes/` com limites de segurança explícitos.

## 2. Consumo assíncrono (destinatário viajando)
- Mensagem WhatsApp quebrada em partes curtas, sem pedir resposta imediata.
- Fechamento tipo "boa viagem, olha quando puder".
- Ordem: áudio de abertura → logos → deck principal → deck secundário → aguardar.

## 3. Regra de logos
- Copiar `04-nome-marketing/logo/LOGO-HORIZONTAL-CLARO.png` e `LOGO-HORIZONTAL-ESCURO.png` para todo kit.

## Pitfall crítico: subagente pode falhar silenciosamente
`delegate_task` pode retornar "completed" SEM ter gerado os arquivos (aconteceu com o kit Mariana Nalin). SEMPRE, após o retorno do subagente:
1. Listar os arquivos esperados e verificar existência + tamanho.
2. Se faltarem, regenerar manualmente (script python-pptx inline reusando helpers do deck de referência).
3. Só então auditar visualmente e sincronizar.
