---
name: casa-smart
description: Use ao automatizar a casa Tuya/Smart Life do Igor.
---

# casa-smart — Automação Residencial (ecossistema do Igor)

## Contexto do Igor
- Casa toda no app **Smart Life** (Tuya) no RJ.
- Objetivo: pedir ao Hermes para ligar/desligar/consultar dispositivos ("liga a luz da sala", "quanto a tomada tá consumindo").
- **Descoberta-chave (05/09/2026):** dispositivos Tuya estão em **OUTRA SUB-REDE** que o PC do Hermes (PC em 192.168.15.x; scan local = 0 dispositivos). Controle local direto não funciona sem roteamento entre redes.
- Agente especialista criado: perfil Hermes `casa-smart` ("Otto") com bíblia de referências (Tuya docs, Zigbee2MQTT, HA, canais BR).

## Plano acordado
1. ~~Scan local~~ (feito — 0 dispositivos, rede errada)
2. **Conta dev Tuya** (pendente — portal iot.tuya.com fora do ar na noite de 05/09; retentar de dia ou pelo celular)
3. Tuya Cloud API → wizard tinytuya → devices.json → Hermes controla via nuvem (independe de sub-rede)
4. Futuro: migração local-first (Home Assistant em mini-PC na rede dos dispositivos)

## Regra de credenciais (crítica)
API ID/Secret do Tuya: **Igor insere manualmente**; o agente NUNCA lê, pede colado no chat ou registra o valor. Verificar apenas PRESENÇA do arquivo de config.

## Detalhes técnicos
Ver `references/tinytuya-setup.md` — passos da conta dev, sintaxe testada do tinytuya 1.20.0 (deviceScan assinatura real, scans que falharam e por quê), e decisão de arquitetura para dispositivos em outra sub-rede.
