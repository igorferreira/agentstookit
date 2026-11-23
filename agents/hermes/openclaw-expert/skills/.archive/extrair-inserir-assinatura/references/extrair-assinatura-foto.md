# Extrair assinatura manuscrita de uma foto/scan (sem visão)

Usado quando o Igor manda uma FOTO da assinatura e a ferramenta de visão (Gemini/vision_analyze) está fora do ar (erro 404 `No endpoints found for google/gemini-2.0-flash-001`). Extração 100% por análise estrutural com scipy — o traço escuro relativo ao fundo local.

## Abordagem

1. **Análise do meio ambiente primeiro** (tamanho, cor, densidade):
   - Foto de assinatura boa tem formato alongado (largura >> altura), fundo ~cinza (lum ~140), traço escuro (lum ~92).
   - Se a imagem tem 62% de tinta espalhada e cor cinza puro (max-min canal ~6), é foto com fundo texturizado, não recorte limpo.

2. **Subtração de fundo gaussiano** para realçar o traço (o traço é mais escuro que o fundo local):
   ```python
   from PIL import Image
   import numpy as np
   from scipy import ndimage
   a = np.array(Image.open(foto).convert('L')).astype(float)
   bg = ndimage.gaussian_filter(a, sigma=10)
   struc = a - bg
   mask = struc < -18        # traço escuro relativo ao fundo
   ```

3. **Componentes conectados** para remover ruído — manter só componentes com área razoável:
   ```python
   lab, n = ndimage.label(mask)
   sizes = ndimage.sum(mask, lab, range(1, n+1))
   big = np.isin(lab, [i+1 for i,s in enumerate(sizes) if s > 120])
   ```

4. **Binarizar** traço preto (0,0,0) sobre fundo transparente (alpha 0). Suavizar borda do alpha com `gaussian_filter(..., 0.5)`.

5. **Cortar margens ruidosas** que esticam o bbox falsamente (conferir perfil de tinta por coluna/linha; descartar bandas de borda com densidade baixa).

## Critérios de qualidade (quando visão fora, julgamento do user)
- Traço real ~15-35% de densidade de tinta; fluido e alongado (largura 7:1). 62% = borrão/ruído.
- Perfil vertical de tinta deve concentrar numa BANDA CENTRAL (assinatura), com queda nas bordas (ruído).
- Componente principal grande + alceots (assinatura legível); múltiplos fragmentos grandes = pode ser texto/ruído junto.

## Limite da técnica
Sem visão, não dá para CONFIRMAR visualmente se saiu limpo. Extraia, insira, renderize um zoom do campo ASSINATURA e PEÇA ao Igor para julgar ("Como ficou o zoom? nítido ou com pedaços soltos?"). Se vier borrado/fragmentado, ajustar: subir/diminuir o limiar (`<-18`), aumentar o corte de componentes pequenos, ou usar outra fonte (DocuSign).

## Validação no PDF (sem visão)
Após inserir, confirmar por dados, não por olho:
- `doc[0].get_images()` → número aumenta na versão assinada (1 imagem a mais).
- `doc[0].get_image_rects(xref)` → rect dentro do campo ASSINATURA.
- Renderizar zoom do campo e medir densidade de tinta presente (assinatura está lá).