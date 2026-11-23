# NFC-e / cupom fiscal fotografado — extração de dados (validado 05/09/2026)

Cenário: foto de cupom NFC-e de mercado; objetivo = recuperar dados da nota (CNPJ, valor, data, itens, chave de acesso).

## Ordem de ataque (do mais barato ao mais caro)

1. **Chave de acesso impressa (44 dígitos)** — geralmente legível mesmo com foto ruim. É a fonte mais valiosa:
   - Estrutura: `AA|AAMM|CNPJ14|MM(65=NFC-e)|SSS(serie)|NNNNNNNNN(numero)|cNF(9)|DV(1)`
   - Validar DV da chave: pesos cíclicos 2-9 aplicados da direita p/ esquerda sobre os 43 dígitos, `DV = 11 - (soma % 11)`, se >=10 então 0.
   - Validar TAMBÉM o DV do CNPJ embutido (módulo 11 padrão). Se o DV do CNPJ NÃO bater, a leitura visual tem 1-2 dígitos errados (o DV da chave pode "bater" mesmo assim — validar ambos independentemente).
   - Do CNPJ, buscar razão social via `https://minhareceita.org/<cnpj>` (sem chave) ou BrasilAPI (`/api/cnpj/v1/<cnpj>`).
2. **Decodificar o QR** — só funciona com foto nítida e papel plano. Engine recomendada: `uv run --with zxing-cpp --with opencv-python-headless python ...` (wheel autônoma, não precisa de libzbar do sistema). Complementos: `cv2.QRCodeDetector`, recortes regionais + upscale 2x/4x + Otsu/adaptive/sharpen. Se falhar por blur/curvatura do papel, pedir NOVA foto (papel achatado, boa luz) em vez de insistir.
   - O QR da NFC-e contém: chNFe, nVersao, tpAmb, cDest, dhEmi, vNF, vICMS, digVal. NÃO contém itens nem nome do estabelecimento.
3. **Consulta SEFAZ pela chave** — portais estaduais (ex: SEFAZ-RJ) BLOQUEIAM IPs de datacenter/servidor ("IPs residenciais listados por uso indevido por crimes cibernéticos"). Portal DFE nacional (dfe-portal.svrs.rs.gov.br) exige login/OIDC. Não insistir de servidor: a consulta final deve ser feita pelo usuário no celular, ou aguardar foto nova do QR.

## Visão assistida (vision_analyze) sobre a foto
- Funciona bem para transcrever a chave de acesso dígito a dígito, itens, valores, NSU e rodapé — usar crops regionais (region=[x1,y1,x2,y2]) para máxima fidelidade.
- Confiar mas VALIDAR: conferir DV da chave e DV do CNPJ após a transcrição (a leitura visual erra 1-2 dígitos com frequência).

## PDFs de fatura com senha (Porto Bank — validado 05/09/2026)
- Padrão da senha: **4 primeiros dígitos do CPF + 5 primeiros do CEP** (ex: CPF 052…, CEP 22750-005 → `052522750`).
- Testar: `pdftotext -upw SENHA -opw SENHA arquivo.pdf saida.txt`.

## Email → PDF da fatura (himalaya, validado 05/09/2026)
- `himalaya message read` só mostra HTML renderizado — o anexo não vem no output. Fluxo validado:
  1. `touch /tmp/dest.eml` (o arquivo de destino PRECISA existir antes do export)
  2. `himalaya message export --account X --folder INBOX -d /tmp/dest.eml <ID>` → grava os MIME parts no diretório do destino (o PDF aparece como arquivo nomeado pelo remetente, ex: `Fatura.pdf`)
- Alternativa: `himalaya attachment download --downloads-dir <dir> <ID>` (nem sempre resolve; export é mais confiável).
- O flag `has_attachment` do JSON de envelope NÃO é confiável — sempre tentar extrair.

## Arquivamento
Salvar em `~/MEGA/Comprovantes/<ano>/<AAAA_MM_MES>/` como `AAAA-MM-DD_<EMISSOR>-NFCE-R<VALOR>.md` com: data/hora, valor, pagamento, NSU, chave de acesso, NFC-e nº, série, protocolo, itens identificados e status do QR/consulta.
