"""Gerador parametrizado de escritórios-vivos (template Sims 2 34×52).

Reaproveita um HTML-base (escritório_modelo.html) e gera N variantes
customizadas: cada uma com tema, agentes, decorações e cookie próprios.

Uso típico (3 escritórios novos):
    python3 build_escritorios.py

Antes de usar:
  1) Confirme que `template_path` aponta para um HTML-base validado (espetinho).
  2) Edite a lista `CLIENTES` abaixo com tema, cor, agentes e decorações.

Pitfalls conhecidos (vide SKILL.md):
  - end_marker NÃO pode ser '];const stations' — usar 'const stations' e
    encontrar o '];' mais próximo antes dele.
  - JS sintaxe: `node -e "new Function(html.match(/<script>([\s\S]*?)<\/script>/)[1])"`
  - Cookie: comparar com `ta_layout__<cookie_key>_` (SEM 'escritorio_' no nome).
  - Sempre validar QA com cross-contamination check (nenhum nome de outro
    escritório pode aparecer no HTML gerado).

Aula: 11/09/2026 — escritório Escape Room, Portões Luís, Política Augusto.
"""
from pathlib import Path
import json
import re

# === CONFIGURAÇÃO ===
TEMPLATE_PATH = Path('/home/igorferreira/projetos/hermes-as-service/demos/clientes/escritorio_espetinho_gabinal.html')
OUTPUT_DIR = Path('/home/igorferreira/projetos/hermes-as-service/demos/clientes')


CLIENTES = [
  {
    'slug': 'escritorio_escape_room_infantil',
    'cookie_key': 'escape_room_infantil',
    'titulo': 'ESCAPE ROOM INFANTIL — FESTA DOS ENIGMAS',
    'cor_root': '#ff8c00',
    'ico_header': '🎃',
    'emoji_alerta': '🎃',
    'msg_alerta': 'Salas temáticas para crianças de 6 a 12 anos — grupos de 6 a 10 jogadores por sala',
    'fase_painel': 'Sáb 14h–22h · Dom 14h–20h',
    'ico_painel': '🔐',
    'btn_reuniao_ico': '👻',
    'btn_reuniao_texto': 'Reunião do staff',
    'reuniao_msg': 'Staff da casa — bora alinhar o plantão de hoje!',
    'input_placeholder': 'Fale com o time do escape room…',
    'decoracoes': [
      {'l': '6px', 't': '6px', 'e': '🔐'},
      {'l': 'right:6px', 't': '6px', 'e': '🎭'},
      {'l': '6px', 't': 'bottom:6px', 'e': '🧩'},
      {'l': 'right:6px', 't': 'bottom:6px', 'e': '🎂'},
      {'l': '40%', 't': '10px', 'e': '👻'},
      {'l': '10%', 't': '50%', 'e': '🕵️'},
    ],
    'agents': [
      {'key': 'gamemaster', 'nome': 'Mestre Léo', 'role': 'Game master', 'cor': '#ff8c00',
       'funcao': 'Cria e testa enigmas, mantém a lógica das salas, acompanha o ritmo dos grupos',
       'tarefas': ['montar enigma', 'resetar sala', 'abrir pista', 'fechar sala']},
      # ... adicione os outros 7 aqui
    ],
  },
  # adicione outros clientes aqui
]


def make(cliente):
  template = TEMPLATE_PATH.read_text(encoding='utf-8')
  html = template

  # Substituições simples
  html = html.replace('--c:#c0392b', f'--c:{cliente["cor_root"]}')
  html = html.replace('TimeAutomático — Escritório Espetinho Gabinal',
                     f'TimeAutomático — {cliente["titulo"]}')
  # Header / alerta / decoração / painéis / placeholder — ver build_escritorios.py original
  # ... (substituições diretas conforme necessidade)

  # === PONTO CRÍTICO: substituir o array agents=[...] ===
  start_marker = 'const agents=['
  end_marker = 'const stations'       # SEM '];' — pega só o identificador seguinte
  si = html.find(start_marker)
  ei = html.find(end_marker, si)
  if si < 0 or ei <= si:
    raise RuntimeError(f'Não achei agents=[ antes de const stations no template. '
                       f'Verifique se TEMPLATE_PATH está correto: {TEMPLATE_PATH}')
  arr_end = html.rfind('];', si, ei)
  if arr_end <= si:
    raise RuntimeError(f'Não achei ]; fechando o array agents antes de const stations.')
  agents_json = json.dumps(cliente['agents'], ensure_ascii=False)
  html = html[:si] + f'const agents={agents_json}' + html[arr_end+2:]

  # Cookie key (SEM prefixo 'escritorio_')
  html = html.replace('ta_layout__escritorio_espetinho_gabinal_',
                     f'ta_layout__{cliente["cookie_key"]}_')

  # nomesCortos
  nomes = [a['nome'] for a in cliente['agents']]
  m2 = re.search(r"const nomesCortos=\['Tonho','Bia','Drica','Zé','Carlão','Sônia','Rita','Igor'\];", html)
  if m2:
    html = html[:m2.start()] + f'const nomesCortos={json.dumps(nomes, ensure_ascii=False)};' + html[m2.end():]

  return html


def main():
  for c in CLIENTES:
    html = make(c)
    out = OUTPUT_DIR / f'{c["slug"]}.html'
    out.write_text(html, encoding='utf-8')
    print(f'✓ {out.name} ({len(html)} bytes, {len(c["agents"])} agents)')


if __name__ == '__main__':
  main()