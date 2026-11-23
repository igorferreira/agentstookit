# Yuanbao Gateway Interaction

Guide for interacting with Yuanbao (元宝, Tencent's AI platform) groups via Hermes. Groups in Yuanbao are called **派 (Pai)**.

## CRITICAL: How Messaging Works

**Your text reply IS the message sent to the group/user.** The Hermes gateway automatically delivers your response text to the Yuanbao chat. You do NOT need any special "send message" tool — just reply normally.

When you include `@nickname` in your reply text, the gateway automatically converts it into a real @mention that notifies the user.

**NEVER say you cannot send messages or @mention users. NEVER suggest the user do it manually. Just reply with the text you want sent.**

## Available Tools

| Tool | When to Use |
|------|-------------|
| `yb_query_group_info` | Query group name, owner, member count |
| `yb_query_group_members` | Find a user, list bots, list all members, or get nickname for @mention |
| `yb_send_dm` | Send a private/direct message (DM / 私信) to a user |

## @Mention Workflow

1. Call `yb_query_group_members` with `action="find"`, `name="<target name>"`, `mention=true`
2. Get the exact nickname from the response
3. Include `@nickname` in your reply text — the gateway handles the rest

```json
{ "group_code": "328306697", "action": "find", "name": "元宝", "mention": true }
```

Then reply: `@元宝 你好，有人找你！`

**Rules:**
- Call `yb_query_group_members` first — do NOT guess nicknames
- The @mention format: `@nickname` with a space before the @ sign
- Be concise — do NOT explain how @mention works to the user

## Send DM (Private Message)

```json
yb_send_dm({ "group_code": "535168412", "name": "用户aea3", "message": "hello" })
```

With media: include `"media_files": [{"path": "/tmp/photo.jpg"}]`

**Rules:**
- `group_code` from chat_id: `group:535168412` → `535168412`
- If you know `user_id`, pass it directly to skip lookup
- Supports: images (.jpg/.png/.gif/.webp/.bmp) as image messages, other files as documents
- Do NOT use `send_message` tool for Yuanbao DMs — use `yb_send_dm`

## Query Operations

```json
yb_query_group_info({ "group_code": "328306697" })
```

| `action` | Description |
|--------|-------------|
| `find` | Search by name (partial match, case-insensitive) |
| `list_bots` | List bots and Yuanbao AI assistants |
| `list_all` | List all members |

## Notes
- `group_code` from chat_id: `group:328306697` → `328306697`
- Member roles: `user`, `yuanbao_ai`, `bot`
