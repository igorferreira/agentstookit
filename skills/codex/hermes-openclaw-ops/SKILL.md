---
name: hermes-openclaw-ops
description: "Manage locally installed Hermes Agent and OpenClaw services on Linux: inspect gateway health, logs and configuration, and carry out requested lifecycle operations."
---

# Hermes and OpenClaw operations

Use this skill when Igor asks to inspect or operate the Hermes Agent or OpenClaw installation on his Linux machine, especially their messaging gateways.

## Discover the current installation

- Check the available CLI and version (`hermes --version`, `openclaw --version`) before relying on a command or diagnosing a version-specific issue.
- These are user-level systemd services on this host. The currently observed unit names are `hermes-gateway.service` and `openclaw-gateway.service`; confirm with `systemctl --user list-units --type=service --all` before acting, since profiles or future installations may use different names.
- Prefer the product CLI for health and diagnostics, and systemd for inspecting or operating the confirmed local service units.

## Gateway operations

- Hermes: use `hermes gateway status`; for logs use `hermes logs gateway -n 100` or `journalctl --user -u hermes-gateway.service -n 100 --no-pager`.
- OpenClaw: use `openclaw gateway status` (add `--deep` for deeper health checks); diagnose reachability with `openclaw doctor`; for logs use `openclaw logs --follow` or `journalctl --user -u openclaw-gateway.service -n 100 --no-pager`.
- For a requested Hermes restart, use `systemctl --user restart hermes-gateway.service` or the documented Hermes gateway CLI. For a requested OpenClaw restart, use `openclaw gateway restart` or `systemctl --user restart openclaw-gateway.service`.
- After lifecycle operations, confirm each unit's state with `systemctl --user --no-pager status <unit>` and check recent logs if it did not return to `active (running)`. Report each gateway separately.
- Prefer graceful service operations over killing a process. OpenClaw may drain active work during shutdown; inspect its current status, `TimeoutStopUSec`, and logs while waiting. Do not send repeated restarts or force-kill it just because shutdown is taking time. Only force termination when the user explicitly asks for it and the normal shutdown has failed.

## Configuration and changes

- Before changing configuration, inspect only the relevant setting and use the product CLI where supported. Hermes provides `hermes config check`; OpenClaw provides `openclaw config validate`.
- Do not print, copy, or include API keys, tokens, cookies, or credential files in output. Redact secrets from logs or configuration excerpts before reporting them.
- Restart only the service that needs the change, then verify health and report any remaining issue.
- Do not install, uninstall, update, enable lingering, change plugins, or alter messaging accounts unless the user requested that specific operation. Use current CLI help or current product documentation for version-dependent operations.
