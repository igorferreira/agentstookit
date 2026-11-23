# OpenHue CLI — Philips Hue Control

Control Philips Hue lights and scenes directly from the terminal via the OpenHue CLI. Use this when the user has direct access to a Hue Bridge (local network) and wants to avoid setting up Home Assistant.

For Hermes's built-in Home Assistant integration (via the `homeassistant` toolset), use `hermes tools enable homeassistant` instead — HA can also control Hue through its integrations.

## Installation

```bash
# Linux (pre-built binary)
curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue

# macOS
brew install openhue/cli/openhue-cli
```

First run requires pressing the button on your Hue Bridge to pair. The bridge must be on the same local network.

## Common Commands

```bash
# List resources
openhue get light       # List all lights
openhue get room        # List all rooms
openhue get scene       # List all scenes

# Turn on/off
openhue set light "Bedroom Lamp" --on
openhue set light "Bedroom Lamp" --off

# Brightness (0-100)
openhue set light "Bedroom Lamp" --on --brightness 50

# Color temperature (warm to cool: 153-500 mirek)
openhue set light "Bedroom Lamp" --on --temperature 300

# Color
openhue set light "Bedroom Lamp" --on --color red
openhue set light "Bedroom Lamp" --on --rgb "#FF5500"

# Control entire room
openhue set room "Bedroom" --off
openhue set room "Bedroom" --on --brightness 30

# Activate a scene
openhue set scene "Relax" --room "Bedroom"
```

## Quick Presets

```bash
# Bedtime (dim warm)
openhue set room "Bedroom" --on --brightness 20 --temperature 450

# Work mode (bright cool)
openhue set room "Office" --on --brightness 100 --temperature 250

# Movie mode
openhue set room "Living Room" --on --brightness 10

# Everything off
for room in "Bedroom" "Office" "Living Room"; do openhue set room "$room" --off; done
```

## Notes

- Bridge must be on the same local network as the machine running Hermes
- First run: physically press the Hue Bridge button to authorize
- Colors only work on color-capable bulbs (not white-only models)
- Light/room names are case-sensitive — use `openhue get light` to check exact names
- Works well in cron jobs for scheduled lighting (dim at bedtime, bright at wake-up)
- Homepage: https://www.openhue.io/cli
