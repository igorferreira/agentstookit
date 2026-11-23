# Extração de Documentos e Apresentações PDF de Publicações do LinkedIn

## Contexto e Desafio

No LinkedIn, postagens com documentos anexados (apresentações/carrosséis em PDF, guias, frameworks) não oferecem um link direto simples de download na página pública para usuários não logados. O visualizador nativo carrega o documento via `iframe` (`data-id="feed-paginated-document-content"`) e faz streaming das páginas através de um **Master Manifest**.

## Pipeline de Extração Automatizada (Passo a Passo)

### 1. Obter os Metadados do Manifest via Browser / DOM

Ao navegar na página do post no LinkedIn via browser ou script de inspeção:

1. Localizar o `iframe` do documento:
   ```javascript
   const iframe = document.querySelector('iframe[data-id="feed-paginated-document-content"]');
   const config = JSON.parse(iframe.getAttribute('data-native-document-config'));
   const manifestUrl = config.doc.manifestUrl;
   ```

2. Fazer requisição GET no `manifestUrl` para obter o JSON do Master Manifest:
   - O JSON conterá diferentes resoluções de imagens renderizadas (`perResolutions`), como 1280px e 1920px (`feedshare-document-images_1920`).
   - Obter o `imageManifestUrl` da resolução mais alta (ex: 1920px).

3. Fazer requisição GET no `imageManifestUrl`:
   - Retorna um JSON contendo a lista direta de URLs públicas de todas as páginas em alta resolução (`pages: [ "https://...", "https://..." ]`).

### 2. Download e OCR Local das Páginas

Com a lista de URLs em mãos:

1. Baixar as imagens em paralelo ou sequencialmente para um diretório temporário (`/tmp/document_pages/page_01.jpg`, etc.).
2. Executar OCR local com Tesseract (`por+eng`) em modo PSM 3 ou PSM 6:
   ```bash
   tesseract /tmp/document_pages/page_01.jpg /tmp/document_pages/page_01 -l por+eng --psm 3
   ```
3. Consolidar o texto de todas as páginas em ordem cronológica.

### 3. Armazenamento e Estruturação

1. Salvar o documento consolidado em Markdown na pasta de destino apropriada:
   - Estudos / Referências: `~/MEGA/Documentos/educacao_leitura/estudos/AAAA-MM-DD_NOME-DO-TEMA.md`
   - Carreira: `~/MEGA/Documentos/carreira/linkedin/`
2. Manter a estrutura de tópicos, categorias, tabelas e prompts de forma clara e referenciável.
