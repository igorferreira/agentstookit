# Mapeamento de Emissores de Cartões de Loja

> Atualizado: 31/07/2026 | Fonte: pesquisas na web + faturas analisadas

## Cartões de Igor — emissores confirmados

| Cartão | Final | Emissor | Bandeira | Fonte |
|---|---|---|---|---|
| Nubank | 3033 | Nu Pagamentos S.A. | Mastercard | App |
| Itaú Signature | 6651 | Itaú Unibanco | Visa/Master | Fatura |
| Itaú Passaí Gold | 6698 | Itaú | Visa/Master | Fatura |
| Itaú Luiza Ouro | 9105 | Luizacred (Itaú) | Visa/Master | Fatura |
| Itaú Vivo | 6423 | Itaú Unibanco | Visa/Master | Fatura |
| Porto Seguro | 8121 | Porto Seguro (admin. Itaú) | Visa/Master | Fatura |
| Carrefour | 3825 | Banco CSF (Carrefour) | Visa Gold | Fatura |
| Amazon | 3018 | Bradescard | Mastercard Platinum | Fatura |
| Méliuz | 2048 | **Banco PAN** | Mastercard Platinum | Web search |
| Atacadão | 1843 | **Banco Carrefour** (CSF) | Mastercard/Visa | Web search |
| C&A Pay | — | **Bradescard** | — | Web search |
| Casas Bahia | 6015 | **Bradescard** | — | Fatura |
| PAN Méliuz | 4863 | **Banco PAN** | — | Fatura |
| PAN Buscapé | 5014 | **Banco PAN** | — | Fatura |
| Inter | 1982 | Banco Inter | Mastercard | App |
| PicPay Gold | — | PicPay/PAN? | — | App |
| RecargaPay | — | RecargaPay | — | App |
| Digio | — | Digio (Bradesco?) | — | App |
| BrasilCard | 5382 | BrasilCard | — | Web search |

## Emissores por grupo

| Grupo | Cartões de Igor |
|---|---|
| **Itaú** | Signature, Passaí, Luiza Ouro, Vivo |
| **Banco PAN** | Méliuz (2048), Méliuz (4863), Buscapé (5014) |
| **Bradescard** | Amazon, Casas Bahia, C&A Pay |
| **Carrefour (CSF)** | Carrefour (3825), Atacadão (1843) |
| **Nu Pagamentos** | Nubank (3033) |
| **Porto Seguro** | Porto (8121) |
| **Inter** | Inter (1982) |

## Como identificar emissor de cartão desconhecido

1. **Buscar na web:** `"cartão [NOME] qual banco emissor"` — priorizar site oficial e ReclameAqui
2. **Ler a fatura em PDF:** `pdftotext` no PDF da fatura → procurar CNPJ e razão social
3. **Identificar pelo grupo:** Cartões de loja do mesmo grupo varejista compartilham emissor (ex: Atacadão e Carrefour → ambos Banco CSF)
4. **App do cartão:** Verificar "Sobre" ou "Termos de Uso" no app
