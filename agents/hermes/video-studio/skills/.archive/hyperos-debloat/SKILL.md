---
name: hyperos-debloat
description: Use quando Igor quiser tirar anúncios do Xiaomi HyperOS.
---

# Remover anúncios e bloatware de Xiaomi/Redmi/POCO (HyperOS/MIUI)

Gatilho: reclamação de propaganda em celular Xiaomi, "bloatware", anúncios no sistema.

## Ordem de execução (ordem importa — MSA primeiro)

1. **MSA (Mobile System Ads)** — o cérebro dos anúncios:
   - Configurações → Senhas e segurança → **Autorização e revogação**
   - Desativar **msa** (às vezes precisa tentar 2x) e também **MIUI Daemon / System Daemon** se aparecer
   - NÃO revogar: Feedback, Downloads, Atualização de apps, Serviço SIM, Bateria, Configurações, GetApps (funcionais)
2. **Notificações do MSA:** Configurações → Apps → Gerenciar aplicativos → 3 pontinhos → Mostrar todos → buscar "msa" → Notificações OFF
3. **DNS privado bloqueador** (bloqueia anúncios no nível de rede):
   - Caminho varia por versão: Configurações → Conexão e compartilhamento → DNS privado (em alguns HyperOS: dentro de Wi-Fi ou Configurações adicionais)
   - **Se o caminho falhar, NUNCA adivinhar menus:** usar a barra "Pesquisar nas Configurações" digitando "privado" ou "DNS" — cai direto na tela certa
   - Host: `dns.adguard.com`
4. **App por app:** em cada app Xiaomi (Segurança, Downloads, Música, Vídeo, Temas, Navegador, Galeria, Explorador), procurar "Receber recomendações"/"Mostrar anúncios" e desligar. Padrão: engrenagem ou perfil → configurações.
5. **Tela inicial:** segurar espaço vazio → Configurações do launcher → "Mostrar sugestões" OFF. Pastas: tocar no nome → "Aplicativos promovidos" OFF.
6. **Privacidade:** pesquisa "anúncios" nas Configurações → desativar "Recomendação personalizada de anúncios" e afins.
7. **Bloatware:** Nível 1 = desinstalar direto; Nível 2 = Forçar parada + Desativar (app de sistema); Nível 3 = ADB `adb uninstall --user 0 <pacote>` (reversível com reset de fábrica; Igor aprova lista antes).

## Pitfalls validados
- **NÃO existe botão único** — são ~15 lugares; checklist leva 15-20 min.
- **Nomes de menu variam entre versões do HyperOS/MIUI.** Guias genéricos erram o caminho — SEMPRE validar com print da tela real do usuário antes de instruir; se o usuário já mandou prints das configurações, LER os itens exatos deles em vez de seguir o guia da web. Preferir sempre a barra de pesquisa das Configurações como rota à prova de versão.
- **Anúncios do app Segurança desaparecem sozinhos** quando MSA está revogado (MSA alimenta esses anúncios) — se o usuário não achar a opção no app, não insistir.
- Após atualização grande do HyperOS, opções podem religar — reexecutar checklist (5 min se já conhece os caminhos).
- NUNCA desativar: Telefonia, Mensagens, Sistema Android, Serviços Google Play, Configurações, GetApps.

## Contexto Igor (06-07/09/2026)
Execução validada no Redmi Note 13 (HyperOS): msa + System Daemon revogados, dns.adguard.com configurado (DNS privado ficava acessível via pesquisa, não no menu previsto), bloatware removido. Registro em ~/MEGA/Documentos/hardware/celulares/2026-09-07_NOTE13-LIMPEZA-EXECUTADA.md; guia completo em 2026-09-06_DUDA-GUIA-REMOVER-ANUNCIOS-XIAOMI.md. Após limpeza, avaliar se upgrade de aparelho ainda se justifica (dor real de RAM vs anúncio resolvível).