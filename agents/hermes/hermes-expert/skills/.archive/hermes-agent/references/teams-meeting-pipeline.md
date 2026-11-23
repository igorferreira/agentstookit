# Teams Meeting Pipeline

Operate the Microsoft Teams meeting summary pipeline via `hermes teams-pipeline` subcommands. Use when the user asks about Teams meeting summaries, transcripts, recordings, action items, Graph subscriptions, or any operational question about this Hermes pipeline.

## Prerequisites

Set in `${HERMES_HOME:-~/.hermes}/.env`:
```bash
MSGRAPH_TENANT_ID=...
MSGRAPH_CLIENT_ID=...
MSGRAPH_CLIENT_SECRET=...
```

If missing, see the Azure app registration guide at `/docs/guides/microsoft-graph-app-registration`.

## Command Reference

### Status and Inspection (start here)
```bash
hermes teams-pipeline validate              # config snapshot — run first after any change
hermes teams-pipeline token-health          # Graph token status
hermes teams-pipeline token-health --force-refresh
hermes teams-pipeline list                  # recent meeting jobs
hermes teams-pipeline list --status failed  # only failed jobs
hermes teams-pipeline show <job-id>         # full detail of one job
hermes teams-pipeline subscriptions         # current Graph webhook subscriptions
```

### Re-running / Debugging
```bash
hermes teams-pipeline run <job-id>          # replay a stored job
hermes teams-pipeline fetch --meeting-id <id>    # dry-run: resolve without persisting
hermes teams-pipeline fetch --join-web-url "<url>"
```

### Subscription Management
```bash
hermes teams-pipeline subscribe \
  --resource communications/onlineMeetings/getAllTranscripts \
  --notification-url https://<your-host>/msgraph/webhook \
  --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE"

hermes teams-pipeline renew-subscription <sub-id> --expiration <iso-8601>
hermes teams-pipeline delete-subscription <sub-id>
hermes teams-pipeline maintain-subscriptions            # renew near-expiry ones
hermes teams-pipeline maintain-subscriptions --dry-run
```

## Decision Tree

- **"Why didn't I get a summary?"** → `list --status failed`, then `show <job-id>`. If job doesn't exist, check `subscriptions` — webhook may have expired.
- **"Is setup working?"** → `validate`, then `token-health`, then `subscriptions`.
- **"Re-run summary for meeting X"** → `list` to find job ID, then `run <job-id>`.

## Critical Pitfall: Graph Subscriptions Expire in 72 Hours

Microsoft Graph webhook subscriptions cap at 72 hours and **will not auto-renew**. If `maintain-subscriptions` is not scheduled, meeting notifications silently stop 3 days after creation.

When "pipeline worked yesterday but nothing today":
1. `hermes teams-pipeline subscriptions` — if empty or all expired, that's the cause.
2. Recreate with `subscribe`.
3. **Set up automated renewal immediately** via `hermes cron add` (12-hour interval is safe).

## Other Pitfalls

- **Transcript not available yet** — Teams takes 2–5 minutes after a meeting ends to generate transcript. Retry or let the webhook drive ingestion.
- **Delivery mode mismatch** — if summaries are produced but nothing arrives in Teams, check `platforms.teams.extra.delivery_mode` and target config.
- **Admin consent** — `token-health` passes but API returns 401/403 = permissions added but admin consent not re-granted. Go to Azure portal → grant admin consent.

## Related Docs

- Azure app registration: `/docs/guides/microsoft-graph-app-registration`
- Full pipeline setup: `/docs/user-guide/messaging/teams-meetings`
- Operator runbook: `/docs/guides/operate-teams-meeting-pipeline`
- Webhook listener: `/docs/user-guide/messaging/msgraph-webhook`
