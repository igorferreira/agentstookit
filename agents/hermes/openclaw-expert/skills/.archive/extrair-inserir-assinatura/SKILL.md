---
name: extrair-inserir-assinatura
description: Obtém a assinatura do Igor e insere em PDFs oficiais.
---

# Extrair e Inserir Assinatura em Documentos

Como obter a assinatura manuscrita/digital do Igor (do DocuSign ou de uma foto) e inseri-la limpa no campo ASSINATURA de um PDF oficial (requerimentos, peças). Complementa o preenchimento de formulários PDF.

## Quando usar
- Preciso colocar a assinatura do Igor num PDF que será protocolado/impresso
- Igor diz "minha assinatura está no sistema da Noorden" / "usa a minha assinatura"
- Recebi uma foto/scan da assinatura e preciso extrair apenas o traço

## Fontes da assinatura do Igor — ordem de preferência

### 1. DocuSign (sistema que a Noorden usa — assinatura limpa)
- A assinatura fica **salva** no perfil, NÃO nos documentos. Caminho:
  - Navegar para `https://account.docusign.com/me` (a sessão fica no subdomínio `account.`, NÃO `apps.`; se `apps.docusign.com` já estiver logado, `account.docusign.com/me` abre logado sem pedir senha).
  - Menu lateral → **Assinaturas** (URL: `account.docusign.com/me/signatures`).
  - Página lista TODOS os estilos salvos (ex: "Igor dos Santos", "IGOR DOS SANTOS FERREIRA", "Igor Ferreira") + rubricas.
- Cada assinatura é servida como **imagem** em `/me/signatures/<id>/signature_image` (a completa costuma ter natureza ~1191×234). Capturar:
  - Localizar o `<img>` por `alt` (o texto da assinatura), pegar `getBoundingClientRect()`.
  - Capturar via CDP `Page.captureScreenshot` com `clip={'x','y','width','height','scale':2}` em volta do img → alta resolução nítida.
- **Sessão:** há duas shells — `apps.docusign.com` (dashboard/envio) e `account.docusign.com` (perfil/assinaturas). Verificar logado em `account.`. O menu "Gerenciar perfil" abre um redirect que pode pedir senha; navegar DIRETO para `account.docusign.com/me` e `.../me/signatures` é mais confiável.

### 2. Clicksign — NÃO guarda imagem
O Clicksign só guarda dados de acesso (nome, celular, CPF, email); NÃO há imagem de assinatura no perfil. Se o sistema for Clicksign e Igor quiser a assinatura dele, usar outra fonte (DocuSign ou foto). Não perder tempo procurando imagem lá.

### 3. Foto/scan enviada pelo Igor
Extrair o traço escuro relativo ao fundo. Ver `references/extrair-assinatura-foto.md` (script completo com scipy: subtração de fundo gaussiano, componentes conectados, binarização preto/transparente).

## Inserir a assinatura no campo ASSINATURA do PDF
Campo ASSINATURA é uma célula (ex: 49-430 x 762.7-786.6). Inserir imagem escalada mantendo proporção, centralizada:
```python
sig_h = 20.0
sig_w = sig_h * (img_w / img_h)      # proporção da imagem de assinatura
x0 = campox0 + (campox1-campox0-sig_w)/2
y0 = campoy0 + (campoy1-campoy0-sig_h)/2
page.insert_image(fitz.Rect(x0,y0,x0+sig_w,y0+sig_h), filename=SIG, keep_proportion=True)
```

## Geração de 2 versões
Para peças a protocolar, Igor pede AMBAS as versões:
- **Sem assinatura** (ASSINATURA+DATA em branco) → assinar à mão na impressão.
- **Assinada** → imagem da assinatura no campo + data escrita no campo DATA.
Gerar as duas do mesmo script/original. Verificar cada uma (a assinada tem imagem a mais no PDF).

## Pitfalls
- **Visão (Gemini/vision_analyze) pode estar fora do ar** (erro 404 "No endpoints found for google/gemini-2.0-flash-001"). Nesse caso NÃO dá pra olhar a imagem — extrair por análise estrutural (scipy) e pedir ao Igor para julgar visualmente o resultado.
- NUNCA adivinhar senha nem pedir que Igor mande a senha pelo chat (regra de segurança). Se o login pedir senha, orientar o Igor a logar ele mesmo ou exportar a assinatura.
- Uma assinatura densa (62% de tinta) = borrão, não traço limpo; o traço real fica em ~15-35% de densidade, fluido e alongado (largura >> altura).
- Cartão de assinaturas de PESSOA JURÍDICA (firma de representante) NÃO é a assinatura pessoal do Igor — não usar para documento de pessoa física.
- Verificar se a assinatura extraída não está fragmentada nos cantos (bbox esticado por ruído) — cortar componentes pequenos (`sizes<120`) e bordas com pouca tinta.