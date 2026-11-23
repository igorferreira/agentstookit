---
name: ascii-media
description: Use when creating ASCII-based static art, banners, image conversions, animations, GIFs, or videos. Route between lightweight text/image tools and the production video pipeline, then verify legibility and rendered output.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ascii, art, animation, video, gif, terminal-art]
---

# ASCII Media

## Overview

One entry point for ASCII visual output, from terminal banners to audio-reactive rendered video.

## Workflow Router

- **Static text, cowsay, boxes, Unicode compositions, or image-to-ASCII:** read `references/ascii-art.md`.
- **Animated ASCII, source-video conversion, audio-reactive scenes, MP4/GIF rendering, shaders, and optimization:** read `references/ascii-video.md` and its topic files under `references/ascii-video/`.

## Shared Workflow

1. Identify the delivery surface: terminal text, Markdown, image, GIF, or MP4.
2. Choose character density, palette, dimensions, and contrast for that surface.
3. Produce a small preview before expensive rendering.
4. Preserve aspect ratio and test at the actual display size.
5. Verify the final artifact opens, has the requested duration/format, and remains legible.

## Verification Checklist

- [ ] Output format and dimensions match the request
- [ ] Characters remain legible at delivery size
- [ ] Aspect ratio is preserved
- [ ] Animation/video artifact was actually rendered and opened
