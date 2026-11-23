# Archify
Website architecture analysis and sitemap generation.
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/archify-lockup-dark.svg" />
    <img src="docs/assets/archify-lockup-light.svg" alt="Archify" width="440" height="121" />
  </picture>
</p>
<h3 align="center">Turn anything you want to understand, plan, or share into an interactive visual.</h3>

<p align="center"><img src="docs/assets/archify-readme-hero.png" alt="Archify — interactive diagrams" width="960" /></p>

<p align="center">Start with an idea, a question, or a plan. Describe it to your AI agent, and Archify turns it into an interactive HTML you can explore, customize, and share. From travel itineraries and learning maps to complex systems—make it your own.</p>

<p align="center">See what the community is creating—and imagine what you could make next.</p>

<p align="center">
  <a href="https://tt-a1i.github.io/archify/gallery.html"><strong>Live demos</strong></a> &nbsp;·&nbsp;
  <a href="#start"><strong>Get started</strong></a> &nbsp;·&nbsp;
  <a href="https://tt-a1i.github.io/archify/guide.html"><strong>Scenario guide</strong></a> &nbsp;·&nbsp;
  <a href="#community"><strong>Community</strong></a> &nbsp;·&nbsp;
  <a href="./README_ZH.md"><strong>简体中文</strong></a> &nbsp;·&nbsp;
  <a href="./README_JA.md"><strong>日本語</strong></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/31352?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-31352" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/31352" alt="tt-a1i/archify | Trendshift" width="250" height="55" /></a>
</p>

<p align="center">
  <a href="https://github.com/tt-a1i/archify/stargazers"><img src="https://img.shields.io/github/stars/tt-a1i/archify?style=flat-square&amp;color=E5B650&amp;logo=github&amp;label=Stars" alt="GitHub stars" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square" alt="MIT License" /></a>
  <a href="archify/SKILL.md"><img src="https://img.shields.io/badge/Agent-Skill-7C3AED?style=flat-square" alt="Agent Skill" /></a>
  <a href="CHANGELOG.md#301--2026-09-28"><img src="https://img.shields.io/badge/version-3.0.1-0891b2?style=flat-square" alt="Stable version 3.0.1" /></a>
</p>

<p align="center">
  <a href="https://tt-a1i.github.io/archify/"><img src="https://img.shields.io/badge/Website-0891B2?style=for-the-badge" alt="Archify website" /></a>
  <a href="https://discord.gg/6xWMjgCeUq"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&amp;logo=discord&amp;logoColor=white" alt="Join Archify on Discord" /></a>
  <a href="#community"><img src="https://img.shields.io/badge/WeChat-07C160?style=for-the-badge&amp;logo=wechat&amp;logoColor=white" alt="Archify WeChat group" /></a>
  <a href="#community"><img src="https://img.shields.io/badge/QQ-1688D8?style=for-the-badge&amp;logo=qq&amp;logoColor=white" alt="Archify QQ group" /></a>
  <a href="https://x.com/t20000622yy"><img src="https://img.shields.io/badge/Creator_on_X-181717?style=for-the-badge&amp;logo=x&amp;logoColor=white" alt="Follow the creator on X" /></a>
</p>

<p align="center"><a href="#sponsors"><strong>❤️ Partners & sponsors: Kimi Work · Supercode · OpenLux</strong></a></p>

## See Archify in action

<!-- archify-launch-video -->

https://github.com/user-attachments/assets/78570807-ba1d-4737-953f-55504a378a87

**One sentence. Your repo, mapped.** Watch the 35-second demo: explore the diagram, follow source links, and trace a path. [Try the interactive examples ↗](https://tt-a1i.github.io/archify/gallery.html)

<a id="start"></a>

### Install, then describe your idea

Works with Cursor, Claude Code, Codex CLI, and OpenCode. See installation options below for additional integrations.

```bash
npx skills add tt-a1i/archify -g
```

Send this to your agent:

```text
Use Archify to diagram a web request: Browser calls the API,
the API checks Redis, and a cache miss queries PostgreSQL and fills the cache.
```

Then continue: “Add authentication”, “Highlight the cache-miss path”, or “Switch to the light theme”.

**No repository is required:** start with a description, or ask your agent to read a repository for a source-backed architecture diagram.

[Choose your agent](https://tt-a1i.github.io/archify/start.html?agent=cursor&type=architecture) · [Installation details and update checks](#quick-start)

<a id="sponsors"></a>

## ❤️ Sponsors

<p align="center">
  <a href="https://www.kimi.ai/?aff=archify"><img src="docs/assets/sponsors/archify-kimi-work.png" alt="Archify × Kimi Work collaboration banner" width="800" /></a>
</p>

**Archify × Kimi Work.** Find Archify in the Kimi Work plugin store as **Interactive Architecture Diagram**. Describe your system in one sentence to create an interactive diagram. **[Try it in Kimi Work →](https://www.kimi.ai/?aff=archify)**

<table>
<tr>
  <td align="center" width="240"><a href="https://supercode.sh/?utm_source=archify"><img src="https://cdn.supercode.sh/sponsors/supercode-logo.png" alt="Supercode" width="200"/></a><br/><strong><a href="https://supercode.sh/?utm_source=archify">supercode.sh</a></strong></td>
<td><a href="https://supercode.sh/?utm_source=archify">Supercode</a> sponsors Archify and enhances Codex and Cursor with token optimization, curated Skills, and spec-driven development. Archify is featured as a <a href="https://supercode.sh/en/skills/tt-a1i/archify/archify">Supercode Editor’s Choice</a> skill.<br/><br/><a href="https://supercode.sh/en/skills/tt-a1i/archify/archify"><img src="https://supercode.sh/badges/editors-choice.svg" alt="Supercode Editor’s Choice — Archify" width="240" height="55"/></a></td>
</tr>
<tr>
<td align="center" width="240"><a href="https://www.openlux.ai/register?channel=c_qdvanbpc"><img src="docs/assets/sponsors/openlux-logo.png" alt="OpenLux" width="200" /></a><br/><strong><a href="https://www.openlux.ai/register?channel=c_qdvanbpc">OpenLux</a></strong></td>
<td>Thank 