---
name: apple-ecosystem
description: Use when operating Apple productivity and communication apps on macOS, including Notes, Reminders, Messages, Find My, and general UI automation. Route to the app-specific workflow and verify actions in the native app or CLI.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, find-my, automation]
---

# Apple Ecosystem Operations

## Overview

This is the class-level entry point for Apple-native application work on macOS. Select the narrow workflow by the user's object, use the least fragile interface available, and verify state after every mutation.

## Workflow Router

- **Notes:** create, search, edit, move, export, or delete notes. Read `references/apple-notes.md`.
- **Reminders:** manage lists, due dates, alarms, completion, and deletion. Read `references/apple-reminders.md`.
- **Messages / iMessage:** search conversations, send messages and attachments, and handle recipient safety. Read `references/imessage.md`.
- **Find My:** inspect devices/items through UI automation and screenshots. Read `references/findmy.md`.
- **General macOS UI:** use accessibility-driven computer control, screenshots, and visual verification. Read `references/macos-computer-use.md`.

## Shared Rules

1. Confirm the operation is running on macOS and that the relevant app/CLI has permission.
2. Prefer a structured CLI or API over UI automation when both exist.
3. For sends, deletions, or location-sensitive actions, verify the target before the final mutation.
4. After a mutation, query or capture the resulting state; do not infer success from a zero exit code alone.
5. Never expose private message content, note contents, or location data beyond the requested scope.

## Verification Checklist

- [ ] Correct Apple account, app, list, conversation, device, or item selected
- [ ] Required Accessibility/Automation permissions available
- [ ] Mutation verified by a read-back or screenshot
- [ ] Sensitive data kept out of logs and summaries
