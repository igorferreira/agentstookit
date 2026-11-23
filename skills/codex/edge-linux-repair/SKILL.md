---
name: edge-linux-repair
description: Diagnosticar e corrigir Microsoft Edge que não abre no Linux, especialmente falhas do sandbox e conflitos de perfis AppArmor no Ubuntu. Usar quando o Edge fecha ao iniciar ou não exibe janela.
---

# Corrigir inicialização do Edge no Linux

Preservar favoritos, senhas, extensões e sessões. Confirmar a causa por evidências antes de alterar configurações. A autorização para reparar o Edge não autoriza apagar o perfil nem alterar políticas globais de segurança.

## Diagnóstico

- Verificar executável, pacote instalado, processos existentes, espaço livre e atalhos locais e do sistema. Ler instruções AGENTS.md aplicáveis antes de editar arquivos.
- Capturar stderr de uma abertura normal. Se já houver instância ativa, evitar encerrar sessões do usuário ou confundir uma chamada encaminhada à instância com um teste de inicialização.
- Distinguir restrições do ambiente do agente das restrições do computador. Uma falha bwrap do próprio terminal não demonstra defeito do navegador. Solicitar execução fora do sandbox pelo mecanismo de aprovação quando necessário.
- Se a abertura direta ainda deixar dúvida e a sessão gráfica usar systemd, testar via `systemd-run --user --unit=edge-diagnostic-IDENTIFICADOR --collect /usr/bin/microsoft-edge-stable about:blank`. Consultar estado e journal da unidade. Esse teste também abre uma janela real; não usar timeout que encerre o navegador do usuário.
- Para erros `Failed to move to new namespace`, `Operation not permitted`, `setuid sandbox` ou `Zygote process exited prematurely`, verificar logs do kernel/AppArmor, `kernel.apparmor_restrict_unprivileged_userns`, permissões de msedge-sandbox e opções de montagem de /opt. `nosuid` pode impedir o sandbox setuid mesmo com modo 4755; o sandbox por user namespaces precisa de autorização AppArmor apropriada.
- Inspecionar `/etc/apparmor.d/msedge`, outros perfis que apontem para o executável real e a lista carregada em `/sys/kernel/security/apparmor/profiles`. A existência dos arquivos não prova que estejam carregados. Se a leitura exigir root, usar sudo autorizado ou pkexec com autenticação gráfica; não pedir senha no chat.
- Links Singleton antigos não bastam para diagnosticar bloqueio. Confirmar ausência do processo e evidência explícita de erro de lock antes de qualquer intervenção nesses links.

## Caso de perfis AppArmor duplicados

No Ubuntu, o perfil padrão costuma associar `msedge` a `/opt/microsoft/msedge/msedge`, com `flags=(unconfined)` e regra `userns,`. Confirmar conteúdo, caminho e versão locais; consultar documentação oficial atual quando necessário.

Dois perfis carregados com nomes diferentes e a mesma associação de executável podem tornar a escolha do perfil ambígua. Tratar como hipótese até verificar a duplicação e comparar os resultados antes e depois da correção.

Quando houver duplicação confirmada:

1. Identificar qual perfil é padrão e qual é adicional. Verificar se o adicional contém regras necessárias antes de removê-lo da seleção.
2. Guardar cópia com metadados em diretório único e datado fora de `/etc/apparmor.d`. Registrar nomes, caminhos e comandos para reversão.
3. Com privilégios aprovados, descarregar somente o perfil redundante com `apparmor_parser -R CAMINHO_DO_PERFIL_ADICIONAL`. Retirar seu arquivo do diretório de carregamento, preservando-o no backup.
4. Recarregar somente o perfil mantido com `apparmor_parser -r CAMINHO_DO_PERFIL_PADRAO`.
5. Testar abertura normal. Se falhar, reavaliar as evidências e restaurar o backup quando apropriado; não acumular mudanças sem diagnóstico.

Não desabilitar AppArmor globalmente, não alterar o sysctl global para contornar o erro e não gravar `--no-sandbox` nos atalhos. Não remonte /opt com suid como correção automática.

## Validação e relato

Confirmar processo principal persistente, janela visível (por exemplo com `wmctrl -lx` em X11), ausência do erro fatal original e perfil efetivo em `/proc/PID/attr/current`. Confirmar que o comando principal não contém `--no-sandbox`. Diferenciar avisos incidentais de falhas que impedem a abertura.

Relatar causa comprovada, mudança aplicada, backup e resultado observado. Só afirmar que a janela abriu com evidência da janela; processo ativo sozinho não basta. Solicitar confirmação do usuário se a interface não puder ser observada. A correção deve persistir no carregamento seguinte, com apenas o perfil desejado na configuração ativa.

## Caso observado em 2026-10-13

Ubuntu 24.04.5 LTS, Edge 155.0.4283.45-1, /opt montado com nosuid. Havia dois perfis ativos: `msedge` e `microsoft-edge-stable`, ambos associados ao mesmo executável. O kernel registrava transição para `unprivileged_userns` e bloqueio de `sys_admin`; o Edge terminava com SIGTRAP.

Após descarregar e arquivar o perfil adicional `microsoft-edge-stable` e recarregar o padrão `msedge`, o Edge abriu com o perfil efetivo `msedge (unconfined)`, janela identificada via wmctrl e processos de renderização ativos. O usuário confirmou a resolução. Backup desta intervenção: `/var/backups/microsoft-edge-apparmor-20261013/`. Esses dados são históricos; revalidar estado e causa em toda execução.
