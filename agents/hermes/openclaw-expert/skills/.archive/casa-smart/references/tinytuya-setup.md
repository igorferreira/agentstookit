# TinyTuya — controlar dispositivos Tuya/Smart Life do Igor via Hermes

## Estado atual (05/09/2026)
- Casa do Igor: dispositivos Tuya via app **Smart Life**, mas em **OUTRA SUB-REDE** que o PC do Hermes (PC em 192.168.15.x; scan local achou 0 dispositivos).
- tinytuya instalável via `uv run --with tinytuya` (não está no python do sistema).
- Portal dev iot.tuya.com ficou inacessível na noite de 05/09 (~00h BRT) — developer.tuya.com abria, iot.tuya.com não. Retentar de dia; tentar também pelo celular/dados móveis.

## Caminho completo (quando a conta dev existir)
1. Igor cria conta em iot.tuya.com (Account Type: "Skip this step"), Cloud → Create Cloud Project (região Americas). Copia API ID + Secret — **Igor insere, o agente NUNCA lê/recebe o valor** (regra absoluta de credenciais).
2. Devices → Link Tuya App Account → QR escaneado pelo app Smart Life (aba "Eu" → botão QR). Subscribe: IoT Core + Authorization.
3. Wizard: `uv run --with tinytuya python -m tinytuya wizard` (gera devices.json com nome/id/ip/local_key).
4. Controle local: `tinytuya.OutletDevice(dev_id, address, local_key, version=3.4).turn_on()/.status()`. Não toca na nuvem no dia-a-dia.
5. Conta trial Tuya: subscribe IoT Core expira (1-6 meses; renovar por formulário). Migração 100% local é o plano B.

## Sintaxe testada (tinytuya 1.20.0)
- `tinytuya.deviceScan()` — assinatura real: (verbose, maxretry, color, poll, forcescan, byID). NÃO tem `maxtime`; `forcescan` exige devices.json com chaves (sem chaves, desabilita silenciosamente).
- Scan simples: `python -m tinytuya scan` (18s, UDP 6666/6667/7000). Sem dispositivos na MESMA sub-rede → 0 achados (este foi o caso do Igor).
- nmap disponível sem sudo: `nmap -sn 192.168.15.0/24` para mapear hosts da rede do PC.

## Decisão de arquitetura
Dispositivos em outra sub-rede ⇒ controle local do PC exige roteamento entre redes OU mover dispositivos OU rota nuvem (Tuya Cloud API — funciona de qualquer rede). **Rota nuvem escolhida** (setup pendente da conta dev).
