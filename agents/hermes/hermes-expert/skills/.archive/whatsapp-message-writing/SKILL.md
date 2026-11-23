---
name: whatsapp-message-writing
description: Prepare concise, natural, copy-ready WhatsApp messages for Igor, including replies, explanations, invitations, sensitive messages, and forwarded summaries.
version: 1.0.0
metadata:
  hermes:
    tags: [whatsapp, messaging, copy-ready, writing, formatting]
---

# WhatsApp message writing

Use this skill whenever Igor asks for:

- a response or message "for WhatsApp";
- text to copy, send, forward, or answer someone on WhatsApp;
- a shorter or more natural WhatsApp version of an explanation;
- multiple WhatsApp reply options;
- a WhatsApp-formatted transcript excerpt.

## Non-negotiable delivery format

Every send-ready WhatsApp message must be placed inside a fenced `text` code block:

```text
Mensagem pronta para copiar e enviar.
```

This makes the Telegram/Hermes interface display a **Copy** button, which is Igor's explicit preference.

### Boundary rule

- Put only content intended for the recipient inside the `text` block.
- Put explanations, factual caveats, or advice to Igor outside and before the block.
- Never append assistant commentary inside the copied message.
- If offering alternatives, give each option its own `text` block so each has an independent Copy button.

## Writing style

1. Match Igor's intended relationship and tone: friend, family, professional contact, partner, service provider, etc.
2. Default to Brazilian Portuguese unless he asks otherwise.
3. Sound conversational and human, not corporate or AI-generated.
4. Keep paragraphs short enough for a phone screen.
5. Preserve all material facts, values, conditions, and boundaries.
6. Avoid overexplaining. For a simple message, deliver one polished option rather than an essay.
7. When a claim is uncertain or variable, tell Igor briefly outside the block and phrase the copied message without making an unsupported promise.

## WhatsApp-native formatting inside the block

Allowed when helpful:

- `*bold*`
- `_italic_`
- bullets
- short paragraphs
- restrained emojis
- separators such as `━━━`

Avoid:

- Markdown tables;
- `#` headings;
- Telegram-specific links or formatting;
- nested code fences;
- citations unless the recipient needs them;
- meta-labels such as "here is your message" inside the copied text.

## Workflow

1. Identify the recipient and desired outcome from context.
2. Verify current or consequential facts with the appropriate tools/skills before drafting.
3. Draft the shortest version that preserves the intended meaning.
4. Humanize the wording: natural rhythm, ordinary vocabulary, no canned chatbot phrases.
5. Separate advice/caveats from send-ready text.
6. Deliver the final message in a fenced `text` block.
7. If Igor asks to save it, store the canonical version in the relevant topic folder, not in a generic WhatsApp dump.
8. For emotionally charged exchanges, inspect the messages Igor has **already sent** before drafting anything new. If the intent is already clear, recommend silence instead of adding a polished follow-up merely because time has passed.

### Follow-up discipline in sensitive conversations

- Never schedule a new message “in one hour” solely to reduce the sender’s anxiety.
- A burst of messages followed by edits/deletions is a signal to stop, not an invitation to perfect the thread indefinitely.
- If a correction is essential, provide one short repair message; otherwise state explicitly that no send-ready message is recommended.
- When children, custody, alleged neglect, or family accusations are involved, avoid categorical diagnoses and adversarial claims. Use factual, non-inflammatory language and offer professional help conditionally.

## Multiple options

When tone genuinely matters, provide up to three labeled choices outside the blocks, for example:

**Direta**
```text
...
```

**Mais carinhosa**
```text
...
```

Do not manufacture alternatives when one straightforward message is enough.

## Pitfalls

- **Plain prose without a Copy button:** even a good WhatsApp draft is incomplete for Igor if it is not in a fenced `text` block.
- **Advice contaminating the message:** the recipient should not receive internal cautions meant only for Igor.
- **Promising variable prices or eligibility:** qualify externally and keep the forwarded wording accurate.
- **Over-formatting:** WhatsApp messages should read like a person wrote them.
- **Code-block confusion:** the fence is a delivery wrapper in Telegram. It exists to provide the Copy button; the copied text itself remains ordinary WhatsApp text.

## User-specific reference

See [`references/igor-format-preference.md`](references/igor-format-preference.md) for the correction that established the copy-button requirement.
