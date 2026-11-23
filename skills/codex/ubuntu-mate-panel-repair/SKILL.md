---
name: ubuntu-mate-panel-repair
description: Corrigir barra deformada do Ubuntu MATE, Brisk com erro, icones gigantes, janelas espremidas e personalizacao permanente de CPU/memoria e Ulauncher. Usar quando Igor pedir reparo ou restauracao da barra MATE.
---

# Reparar a barra do Ubuntu MATE

## Preferencia permanente de Igor

Escolhas aprovadas em 13/10/2026: menu classico integrado ao MATE, Brisk fora dos objetos ativos; itens desbloqueados para mover/remover; sem montador de drives; graficos de CPU e memoria; relogio a direita; Ulauncher como lancador padrao, iniciando oculto junto com a sessao. Preservar essas preferencias ao reparar a barra.

Na verificacao final, classicmenu ja havia sido retirado da lista ativa durante a personalizacao da sessao. Preservar alteracoes manuais posteriores do usuario; com Ulauncher padrao, nao reintroduzir menu classico ausente sem pedido. Se precisar de menu no painel, usar o classico em vez do Brisk.

GSettings/dconf, icones locais e autostart persistem entre logins. Nao declarar um teste apos reboot quando somente se verificou a configuracao persistente.

## Diagnosticar antes de alterar

Usar a sessao grafica real do usuario, com DISPLAY e DBUS_SESSION_BUS_ADDRESS corretos. O sandbox pode mostrar somente processos isolados: solicitar escalacao para acessar a sessao quando necessario. Nunca usar sudo gsettings.

Salvar `dconf dump /org/mate/panel/` em backup com data/hora antes de alterar. Conferir pgrep -a -x mate-panel e brisk-menu, journalctl --user, xrandr --current, xwininfo -root -tree, tema de icones (`gsettings get org.mate.interface icon-theme`) e object-id-list atual.

Capturar a barra com `import -window root -crop LARGURAxALTURA+X+Y arquivo.png` e visualizar com view_image. Derivar coordenadas atuais de xrandr/xwininfo. Nesta sessao: principal 1920x1080+1920+0, painel inferior 1920x28+1920+1052. Nao assumir essas coordenadas em outra sessao.

Nao considerar a barra reparada so porque o menu abre ou o journal nao apresenta erros. Inspecionar a barra INTEIRA: Brisk e indicador gigante eram problemas independentes.

## Icone gigante: aviso de reinicializacao

Sintoma observado: faixa azul com imagem branca gigante e tooltip "E necessario reiniciar o sistema". IndicatorAppletComplete ocupava 1270x28 pixels, espremendo os titulos das janelas. O elemento era `un-reboot` do update-notifier.

Para descobrir indicadores e seus donos DBus:

```bash
gdbus call --session --dest org.ayatana.indicator.application \
  --object-path /org/ayatana/indicator/application/service \
  --method org.ayatana.indicator.application.service.GetApplications
```

IDs DBus :1.* mudam por sessao. Confirmar tooltip/icone e consultar Properties.GetAll de org.kde.StatusNotifierItem no caminho do item quando necessario.

Verificar qual arquivo GTK seleciona:

```bash
/usr/bin/python3 -c 'import gi; gi.require_version("Gtk","3.0"); from gi.repository import Gtk; print(Gtk.IconTheme.get_default().lookup_icon("un-reboot",16,0).get_filename())'
```

Aqui Yaru-bark-dark herdava `/usr/share/icons/Humanity/apps/24/un-reboot.svg`. Override somente em hicolor NAO resolveu: Humanity tinha prioridade.

Correcao testada, somente apos confirmar esse sintoma:

1. Obter tema ATIVO e localizar seu index.theme. Verificar que `/usr/share/icons/hicolor/16x16/apps/software-update-urgent.png` existe e e PNG pequeno.
2. Criar `~/.local/share/icons/TEMA/16x16/apps/`; salvar em backup qualquer un-reboot.png existente.
3. Copiar software-update-urgent.png para un-reboot.png nesse diretorio.
4. Se index.theme local nao existir, copiar do tema correspondente do sistema. Preservar index.theme preexistente.
5. Executar gtk-update-icon-cache -f no diretorio local do tema e reiniciar SOMENTE o painel.

Override persistente atual: `~/.local/share/icons/Yaru-bark-dark/16x16/apps/un-reboot.png`. Resultado: bloco caiu de 1270 para 646 pixels, imagem gigante sumiu e titulos voltaram. Largura varia conforme aplicativos ativos.

Preservar aviso de atualizacao/reinicio; nao matar update-notifier nem modificar icones do sistema. Se o problema persistir, investigar o elemento real em vez de repetir reinicios.

## Menu classico, desbloqueio e monitores

Brisk foi retirado da lista ativa, sem desinstalar pacotes. Consulta em 13/10/2026: https://github.com/getsolus/brisk-menu arquivado em 09/08/2025; README declara falta de manutencao. Revalidar se necessario.

Schema global correto: `org.mate.panel`, path `/org/mate/panel/general/`. `org.mate.panel.general` NAO existe. Objetos usam schema relocatable `org.mate.panel.object:/org/mate/panel/objects/ID/`.

Criar objeto menu classico com object-type=menu, toplevel-id do painel existente, position=0. Incluir na object-id-list atual e retirar apenas o objeto com applet-iid=BriskMenuFactory::BriskMenu. Nao aplicar reset global/redmond: reintroduz Brisk e atalhos quebrados. Validar caminhos de launchers antes de retira-los; preservar outros itens do usuario.

Para mover/remover, definir org.mate.panel locked-down=false E locked=false em cada objeto ativo. Na interface: botao direito > Mover / Remover do painel; tentar Alt+botao direito quando applet captura o clique. Icones internos da bandeja continuam gerenciados por seus aplicativos.

Retirar apenas o objeto DriveMountAppletFactory::DriveMountApplet da lista ativa. Isso nao desmonta discos.

Monitor atual `systemmonitor`: object-type=applet, applet-iid=MultiLoadAppletFactory::MultiLoadApplet, toplevel-id=bottom, relative-to-edge=end, position=30, locked=false. Schema de preferencias: `org.mate.panel.applet.multiload:/org/mate/panel/objects/systemmonitor/prefs/`. Definir view-cpuload=true, view-memload=true; view-netload/view-swapload/view-loadavg/view-diskload=false; size=55, speed=1000. Incluir ID na lista existente. CPU azul e memoria verde.

Relogio: ClockAppletFactory::ClockApplet, relative-to-edge=end, position=0; indicador completo position=10, area de notificacao position=20. Lista de janelas: group-windows=auto no schema org.mate.panel.applet.window-list do objeto atual.

## Ulauncher persistente

Conferir processo, `~/.config/autostart/ulauncher.desktop`, settings.json e systemctl --user status/is-enabled ulauncher.service antes de alterar. Evitar duas inicializacoes concorrentes.

Em 13/10/2026, Ulauncher estava executando, mas o arquivo XDG tinha Hidden=true e o servico systemd estava disabled. Foi corrigido para Hidden=false, X-GNOME-Autostart-enabled=true e Exec=ulauncher --hide-window. Manter esse autostart XDG; nao habilitar tambem o servico sem migracao explicita. Preservar settings.json. Atalho atual aprovado implicitamente por preservacao: Ctrl+Shift+Espaco.

## Validar e desfazer

Reiniciar apenas a barra com unidade TRANSITORIA de nome unico:

```bash
systemd-run --user --collect --unit="mate-panel-repair-$(date +%s)" /usr/bin/mate-panel --replace
```

Nao habilitar essa unidade no boot: mate-session ja inicia o painel. Conferir uma instancia, logs e captura completa: menu abre/fecha, imagem gigante ausente, titulos visiveis, relogio e CPU/memoria presentes, drives ausentes. Reler locked-down/locked, preferencias e autostart; salvar panel-after.ini.

Restaurar painel com `dconf load /org/mate/panel/ < panel-before.ini` e reiniciar o painel. Para desfazer override, restaurar PNG anterior ou retirar somente o criado e atualizar cache. Rollback do dconf sozinho nao desfaz icones nem autostart.

Evidencias: `/home/igorferreira/panel-repair-20261013/` contem backups, README.md e capturas. Usar para historico; revalidar estado atual sempre.
