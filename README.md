<div align="center">

# ðŸ›¡ï¸ Hermes Shield | Ù‡Ø±Ù…Ø³ Ø´ÛŒÙ„Ø¯

[![Version](https://img.shields.io/badge/Version-v1.3.0-blue.svg?style=for-the-badge)](https://github.com/h0j5bz0adh0-stack/hermes-shield)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Agent](https://img.shields.io/badge/Agent-Hermes%20%7C%20Claude%20Code%20%7C%20OpenClaw-purple.svg?style=for-the-badge)](https://github.com/NousResearch/hermes-agent)

**Backup, Restore & Sync for AI Agent Configurations**
**Ø¨Ú©â€ŒØ¢Ù¾ØŒ Ø¨Ø§Ø²ÛŒØ§Ø¨ÛŒ Ùˆ Ù‡Ù…Ú¯Ø§Ù…â€ŒØ³Ø§Ø²ÛŒ ØªÙ†Ø¸ÛŒÙ…Ø§Øª Ø§ÛŒØ¬Ù†Øª Ù‡ÙˆØ´ Ù…ØµÙ†ÙˆØ¹ÛŒ**

[English](#-why-hermes-shield) â€¢ [ÙØ§Ø±Ø³ÛŒ](#ÙØ§Ø±Ø³ÛŒ) â€¢ [Quick Start](#-quick-start) â€¢ [Commands](#-commands)

</div>

---

<a id="ÙØ§Ø±Ø³ÛŒ"></a>

## ðŸ‡®ðŸ‡· ÙØ§Ø±Ø³ÛŒ

### Ú†Ø±Ø§ Ù‡Ø±Ù…Ø³ Ø´ÛŒÙ„Ø¯ØŸ

Ø§ÛŒØ¬Ù†Øªâ€ŒÙ‡Ø§ÛŒ Ù‡ÙˆØ´ Ù…ØµÙ†ÙˆØ¹ÛŒ Ù…Ø«Ù„ **Hermes**ØŒ **Claude Code** Ùˆ **OpenClaw** ØªÙ†Ø¸ÛŒÙ…Ø§Øª Ø­ÛŒØ§ØªÛŒâ€ŒØ´ÙˆÙ† Ø±Ùˆ Ø±ÙˆÛŒ Ø³ÛŒØ³ØªÙ… Ø´Ù…Ø§ Ø°Ø®ÛŒØ±Ù‡ Ù…ÛŒÚ©Ù†Ù† â€” Ø§Ø³Ú©ÛŒÙ„â€ŒÙ‡Ø§ØŒ Ù¾Ù„Ø§Ú¯ÛŒÙ†â€ŒÙ‡Ø§ØŒ cron job Ù‡Ø§ØŒ Ø­Ø§ÙØ¸Ù‡ Ùˆ Ú©Ø§Ù†ÙÛŒÚ¯. Ø§Ú¯Ù‡ Ø§ÛŒÙ†Ø§ Ø§Ø² Ø¨ÛŒÙ† Ø¨Ø±Ù†ØŒ Ù‡ÙØªÙ‡â€ŒÙ‡Ø§ Ú©Ø§Ø± Ø§Ø² Ø¯Ø³Øª Ù…ÛŒØ±Ù‡!

**Ù‡Ø±Ù…Ø³ Ø´ÛŒÙ„Ø¯** Ø¨Ù‡ØªÙˆÙ† Ø§ÛŒÙ†Ø§ Ø±Ùˆ Ù…ÛŒØ¯Ù‡:
- âœ… Ø¨Ú©â€ŒØ¢Ù¾ Ú©Ø§Ù…Ù„ Ø¨Ø§ **ÛŒÙ‡ Ø¯Ø³ØªÙˆØ±**
- âœ… Ø±Ù…Ø²Ù†Ú¯Ø§Ø±ÛŒ **AES-256** (Ø§Ø³ØªØ§Ù†Ø¯Ø§Ø±Ø¯ Ù†Ø¸Ø§Ù…ÛŒ)
- âœ… Ù†Ø³Ø®Ù‡â€ŒØ¨Ù†Ø¯ÛŒ Ø®ÙˆØ¯Ú©Ø§Ø± Ùˆ Ù¾Ø§Ú©Ø³Ø§Ø²ÛŒ
- âœ… Ø¨Ø§Ø²ÛŒØ§Ø¨ÛŒ Ø§Ø² Ù‡Ø± Ù†Ù‚Ø·Ù‡ Ø¯Ø± Ø²Ù…Ø§Ù†
- âœ… Ù…Ù‚Ø§ÛŒØ³Ù‡ Ø¯Ùˆ Ø¨Ú©â€ŒØ¢Ù¾ (Diff)
- âœ… Ø³Ø§Ø²Ú¯Ø§Ø± Ø¨Ø§ **Ù‡Ø±Ù…Ø³ØŒ Claude CodeØŒ OpenClaw**
- âœ… **Ø¨Ú©â€ŒØ¢Ù¾ Ø®ÙˆØ¯Ú©Ø§Ø± Ø±ÙˆÛŒ Ú¯ÙˆÚ¯Ù„ Ø¯Ø±Ø§ÛŒÙˆ** Ù‡Ø± Û² Ø±ÙˆØ²
- âœ… **Ø³Ø§Ø²Ú¯Ø§Ø± Ø¨Ø§ Ø³Ø±ÙˆØ±Ù‡Ø§ÛŒ headless** (Ø¨Ø¯ÙˆÙ† Ù…Ø±ÙˆØ±Ú¯Ø±)

### Ù†ØµØ¨ Ø³Ø±ÛŒØ¹

```bash
git clone https://github.com/h0j5bz0adh0-stack/hermes-shield.git
cd hermes-shield
pip install cryptography
python3 scripts/hermes-shield.py backup
```

### Ù†ØµØ¨ Ø¨Ù‡ Ø¹Ù†ÙˆØ§Ù† Ø§Ø³Ú©ÛŒÙ„ Ù‡Ø±Ù…Ø³

```bash
mkdir -p ~/.hermes/skills/devops/hermes-shield
cp SKILL.md ~/.hermes/skills/devops/hermes-shield/
cp -r scripts ~/.hermes/skills/devops/hermes-shield/
pip install cryptography
```

### Ø¯Ø³ØªÙˆØ±Ø§Øª

| Ø¯Ø³ØªÙˆØ± | ØªÙˆØ¶ÛŒØ­ |
|-------|-------|
| `backup` | Ø¨Ú©â€ŒØ¢Ù¾ Ú©Ø§Ù…Ù„ |
| `backup -l "ØªÙˆØ¶ÛŒØ­Ø§Øª"` | Ø¨Ú©â€ŒØ¢Ù¾ Ø¨Ø§ Ø¨Ø±Ú†Ø³Ø¨ |
| `backup -e -p Ø±Ù…Ø²` | Ø¨Ú©â€ŒØ¢Ù¾ Ø±Ù…Ø²Ù†Ú¯Ø§Ø±ÛŒâ€ŒØ´Ø¯Ù‡ |
| `backup -c` | Ø¨Ú©â€ŒØ¢Ù¾ + Ø¢Ù¾Ù„ÙˆØ¯ Ú¯ÙˆÚ¯Ù„ Ø¯Ø±Ø§ÛŒÙˆ |
| `restore` | Ø¨Ø§Ø²ÛŒØ§Ø¨ÛŒ Ø¢Ø®Ø±ÛŒÙ† Ù†Ø³Ø®Ù‡ |
| `restore -f ÙØ§ÛŒÙ„` | Ø¨Ø§Ø²ÛŒØ§Ø¨ÛŒ Ø§Ø² ÙØ§ÛŒÙ„ Ù…Ø´Ø®Øµ |
| `restore -t skills,config` | Ø¨Ø§Ø²ÛŒØ§Ø¨ÛŒ ÙÙ‚Ø· Ø¨Ø®Ø´â€ŒÙ‡Ø§ÛŒ Ù…Ø´Ø®Øµ |
| `list` | Ù†Ù…Ø§ÛŒØ´ Ù„ÛŒØ³Øª Ø¨Ú©â€ŒØ¢Ù¾â€ŒÙ‡Ø§ |
| `list --cloud` | Ù†Ù…Ø§ÛŒØ´ Ø¨Ú©â€ŒØ¢Ù¾â€ŒÙ‡Ø§ÛŒ Ø§Ø¨Ø±ÛŒ |
| `push` | Ø¢Ù¾Ù„ÙˆØ¯ Ø¢Ø®Ø±ÛŒÙ† Ø¨Ú©â€ŒØ¢Ù¾ Ø¨Ù‡ Ú¯ÙˆÚ¯Ù„ Ø¯Ø±Ø§ÛŒÙˆ |
| `pull` | Ø¯Ø§Ù†Ù„ÙˆØ¯ Ø¢Ø®Ø±ÛŒÙ† Ø¨Ú©â€ŒØ¢Ù¾ Ø§Ø² Ú¯ÙˆÚ¯Ù„ Ø¯Ø±Ø§ÛŒÙˆ |
| `verify ÙØ§ÛŒÙ„` | Ø¨Ø±Ø±Ø³ÛŒ Ø³Ù„Ø§Ù…Øª Ø¨Ú©â€ŒØ¢Ù¾ |
| `diff A.tar.gz B.tar.gz` | Ù…Ù‚Ø§ÛŒØ³Ù‡ Ø¯Ùˆ Ø¨Ú©â€ŒØ¢Ù¾ |
| `stats` | Ù†Ù…Ø§ÛŒØ´ Ø¢Ù…Ø§Ø± |
| `config` | Ù†Ù…Ø§ÛŒØ´ ØªÙ†Ø¸ÛŒÙ…Ø§Øª |
| `connect` | Ø§ØªØµØ§Ù„ Ú¯ÙˆÚ¯Ù„ Ø¯Ø±Ø§ÛŒÙˆ (Ø³Ø±ÙˆØ± headless) |
| `setup` | Ø±Ø§Ù‡â€ŒØ§Ù†Ø¯Ø§Ø²ÛŒ ØªØ¹Ø§Ù…Ù„ÛŒ |
| `setup-auto` | Ø±Ø§Ù‡â€ŒØ§Ù†Ø¯Ø§Ø²ÛŒ Ø®ÙˆØ¯Ú©Ø§Ø± (Ø¨Ø±Ø§ÛŒ Ù‡Ø±Ù…Ø³) |
| `token <JSON>` | Ø§Ø¹Ù…Ø§Ù„ ØªÙˆÚ©Ù† Ú¯ÙˆÚ¯Ù„ Ø¯Ø±Ø§ÛŒÙˆ |

### Ú†ÛŒØ§ Ø¨Ú©â€ŒØ¢Ù¾ Ù…ÛŒØ´Ù‡ØŸ

```
~/.hermes/
â”œâ”€â”€ skills/          âœ… Ø§Ø³Ú©ÛŒÙ„â€ŒÙ‡Ø§ Ùˆ ÙˆØ±Ú©â€ŒÙÙ„ÙˆÙ‡Ø§
â”œâ”€â”€ plugins/         âœ… Ù¾Ù„Ø§Ú¯ÛŒÙ†â€ŒÙ‡Ø§
â”œâ”€â”€ cron/            âœ… Ø¬Ø§Ø¨â€ŒÙ‡Ø§ÛŒ Ø²Ù…Ø§Ù†â€ŒØ¨Ù†Ø¯ÛŒ
â”œâ”€â”€ memories/        âœ… Ø­Ø§ÙØ¸Ù‡ Ù¾Ø§ÛŒØ¯Ø§Ø±
â”œâ”€â”€ config.yaml      âœ… ØªÙ†Ø¸ÛŒÙ…Ø§Øª Ø§ØµÙ„ÛŒ
â””â”€â”€ sessions/        âš™ï¸ ØªØ§Ø±ÛŒØ®Ú†Ù‡ (Ø§Ø®ØªÛŒØ§Ø±ÛŒ)
```

### Ø±Ù…Ø²Ù†Ú¯Ø§Ø±ÛŒ

Ø§Ø² **AES-256** Ø¨Ø§ **PBKDF2** (Û´Û¸Û°,Û°Û°Û° ØªÚ©Ø±Ø§Ø±) Ø§Ø³ØªÙØ§Ø¯Ù‡ Ù…ÛŒÚ©Ù†Ù‡ â€” Ù‡Ù…ÙˆÙ† Ø§Ø³ØªØ§Ù†Ø¯Ø§Ø±Ø¯ Ø±Ù…Ø²Ù†Ú¯Ø§Ø±ÛŒ Ø¨Ø§Ù†Ú©â€ŒÙ‡Ø§ Ùˆ Ù…Ø¯ÛŒØ± Ø±Ù…Ø² Ø¹Ø¨ÙˆØ±.

```bash
python3 scripts/hermes-shield.py backup -e -p "Ø±Ù…Ø²-Ø§Ù…Ù†-Ù…Ù†"
python3 scripts/hermes-shield.py restore -f backup.tar.gz
```

### Ø§ØªØµØ§Ù„ Ú¯ÙˆÚ¯Ù„ Ø¯Ø±Ø§ÛŒÙˆ (Ø³Ø±ÙˆØ± Headless)

```bash
# Û±. Ø§ØªØµØ§Ù„
python3 scripts/hermes-shield.py connect

# Û². Ø±ÙˆÛŒ Ù„Ù¾â€ŒØªØ§Ù¾/Ù…ÙˆØ¨Ø§ÛŒÙ„:
#    Ø§Ù„Ù) rclone Ø±Ùˆ Ø¯Ø§Ù†Ù„ÙˆØ¯ Ú©Ù†:
#    https://downloads.rclone.org/current/rclone-current-windows-amd64.zip
#    Ø¨) ÙÙ‚Ø· extract Ú©Ù† (Ù†ÛŒØ§Ø²ÛŒ Ø¨Ù‡ Ù†ØµØ¨ Ù†ÛŒØ³Øª)
#    Ø¬) ØªÙˆÛŒ Ù¾ÙˆØ´Ù‡ rclone ØªØ±Ù…ÛŒÙ†Ø§Ù„ Ø¨Ø§Ø² Ú©Ù†
#    Ø¯) Ø§ÛŒÙ† Ø¯Ø³ØªÙˆØ± Ø±Ùˆ Ø¨Ø²Ù†:
rclone authorize "drive"

# Û³. ÛŒÙ‡ Ù¾Ù†Ø¬Ø±Ù‡ Ù…Ø±ÙˆØ±Ú¯Ø± Ø¨Ø§Ø² Ù…ÛŒØ´Ù‡ â†’ Ø§Ú©Ø§Ù†Øª Ú¯ÙˆÚ¯Ù„Øª Ø±Ùˆ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù† â†’ Allow Ø¨Ø²Ù†
# Û´. ÛŒÙ‡ Ù…ØªÙ† JSON Ø¨Ù‡Øª Ù…ÛŒØ¯Ù‡ â†’ Ú©Ù¾ÛŒ Ú©Ù† Ùˆ Ø§ÛŒÙ†Ø¬Ø§ Ø¨ÙØ±Ø³Øª:
python3 scripts/hermes-shield.py token '{"access_token":"...","refresh_token":"...",...}'

# Ûµ. ÙØ¹Ø§Ù„ Ú©Ø±Ø¯Ù† Ø¨Ú©â€ŒØ¢Ù¾ Ø®ÙˆØ¯Ú©Ø§Ø±
python3 scripts/hermes-shield.py config set cloud_enabled=true
```

### Ø¨Ú©â€ŒØ¢Ù¾ Ø®ÙˆØ¯Ú©Ø§Ø± Ù‡Ø± Û² Ø±ÙˆØ²

```bash
# crontab
0 3 */2 * * /usr/bin/python3 /path/to/hermes-shield.py backup -l "auto" -c
```

### Ù¾Ø´ØªÛŒØ¨Ø§Ù†ÛŒ Ø§Ø² Ø§ÛŒØ¬Ù†Øªâ€ŒÙ‡Ø§

| Ø§ÛŒØ¬Ù†Øª | Ù…Ø³ÛŒØ± ØªÙ†Ø¸ÛŒÙ…Ø§Øª | ÙˆØ¶Ø¹ÛŒØª |
|-------|-------------|-------|
| Hermes Agent | `~/.hermes/` | âœ… Ú©Ø§Ù…Ù„ |
| Claude Code | `~/.claude/` | âœ… Ø¬Ø²Ø¦ÛŒ |
| OpenClaw | `~/.openclaw/` | âœ… Ø¬Ø²Ø¦ÛŒ |
| Ø§ÛŒØ¬Ù†Øª Ø³ÙØ§Ø±Ø´ÛŒ | Ù‡Ø± Ù…Ø³ÛŒØ±ÛŒ | ðŸ”§ Ù‚Ø§Ø¨Ù„ ØªÙ†Ø¸ÛŒÙ… |

---

<a id="-why-hermes-shield"></a>

## ðŸŽ¯ English

### Why Hermes Shield?

AI agents like Hermes, Claude Code, and OpenClaw store critical state locally â€” skills, plugins, cron jobs, memory, configuration. If you lose this, you lose weeks of work.

**Hermes Shield** gives you:
- âœ… One-command backup of everything
- âœ… AES-256 encryption (military-grade)
- âœ… Automatic versioning & cleanup
- âœ… Restore any point in time
- âœ… Diff between backups
- âœ… Cross-agent compatibility
- âœ… **Google Drive sync** â€” auto backup every 2 days
- âœ… **Headless server compatible** (no browser needed)

## ðŸš€ Quick Start

```bash
git clone https://github.com/h0j5bz0adh0-stack/hermes-shield.git
cd hermes-shield
pip install cryptography
python3 scripts/hermes-shield.py backup
```

## ðŸ“‹ Commands

| Command | Description |
|---------|-------------|
| `backup` | Create a full backup |
| `backup -l "label"` | Create a labeled backup |
| `backup -e -p PASS` | Create an encrypted backup |
| `backup -c` | Backup + upload to Google Drive |
| `restore` | Restore the latest backup |
| `restore -f FILE` | Restore from a specific file |
| `restore -t skills,config` | Restore only selected targets |
| `list` | List local backups |
| `list --cloud` | List cloud backups |
| `push` | Upload latest to Google Drive |
| `pull` | Download latest from Google Drive |
| `pull -f FILE` | Download specific from Google Drive |
| `verify FILE` | Verify backup integrity |
| `stats` | Show backup statistics |
| `config` | View configuration |
| `config set key=value` | Update a config setting |
| `connect` | Connect Google Drive (headless) |
| `setup` | Interactive setup wizard |
| `setup-auto` | Non-interactive setup (for Hermes) |
| `token <JSON>` | Apply Google Drive auth token |

## ðŸ”’ Encryption

Uses **AES-256-CBC** with **PBKDF2** key derivation (480,000 iterations, SHA-256).

```bash
# Encrypted backup
python3 scripts/hermes-shield.py backup -e -p "my-secure-password"

# Restore
python3 scripts/hermes-shield.py restore -f backup.tar.gz
```

## â˜ï¸ Google Drive Sync (Headless Server)

```bash
# 1. Connect
python3 scripts/hermes-shield.py connect

# 2. On your laptop/phone:
#    a) Download rclone:
#    https://downloads.rclone.org/current/rclone-current-windows-amd64.zip
#    b) Just extract (no installation needed)
#    c) Open terminal in the rclone folder
#    d) Run this command:
rclone authorize "drive"

# 3. A browser window opens â†’ select your Google account â†’ Allow
# 4. It outputs a JSON token â†’ copy it and send here:
python3 scripts/hermes-shield.py token '{"access_token":"...","refresh_token":"...",...}'

# 5. Enable auto backup
python3 scripts/hermes-shield.py config set cloud_enabled=true
```

## ðŸ¤– Hermes Agent Integration

When user says: "Ø¨Ú©â€ŒØ¢Ù¾ Ú¯ÙˆÚ¯Ù„ Ø¯Ø±Ø§ÛŒÙˆ Ù‡Ø± Û² Ø±ÙˆØ² Ø¨Ú¯ÛŒØ±"

Hermes runs:
```bash
python3 scripts/hermes-shield.py setup-auto --cloud yes --interval 48
```

Outputs JSON with auth instructions. User sends token. Hermes applies it:
```bash
python3 scripts/hermes-shield.py token '<JSON>'
```

## ðŸ“ What Gets Backed Up

```
~/.hermes/
â”œâ”€â”€ skills/          âœ… All skills & workflows
â”œâ”€â”€ plugins/         âœ… Extensions & plugins
â”œâ”€â”€ cron/            âœ… Scheduled jobs
â”œâ”€â”€ memories/        âœ… Persistent memory
â”œâ”€â”€ config.yaml      âœ… Main configuration
â””â”€â”€ sessions/        âš™ï¸ Optional (large)
```

## ðŸ¤– Cross-Agent Support

| Agent | Config Path | Status |
|-------|-------------|--------|
| Hermes Agent | `~/.hermes/` | âœ… Full |
| Claude Code | `~/.claude/` | âœ… Partial |
| OpenClaw | `~/.openclaw/` | âœ… Partial |
| Custom | Any path | ðŸ”§ Configurable |

## ðŸ“Š Stats

```bash
$ python3 scripts/hermes-shield.py stats

ðŸ›¡ï¸  Hermes Shield v1.3.0 â€” Stats

  Local backups:    12
  Local size:       2.3 MB
  Cloud backups:    5
  Max local:        10
  Max cloud:        5
  Auto backup:      âœ… Every 48h
  Cloud sync:       âœ…
  Google Drive:     âœ… Connected
  Current data:     45.2 KB
```

## ðŸ›£ï¸ Roadmap

- [ ] Dropbox / OneDrive support
- [ ] S3 / Cloudflare R2 remote storage
- [ ] Sync between multiple machines
- [ ] Web dashboard
- [ ] Compression level options

## ðŸ¤ Contributing

Contributions welcome! ðŸ› Report bugs â€¢ ðŸ’¡ Suggest features â€¢ ðŸ”§ Submit PRs

## ðŸ“œ License

MIT License â€” use freely, contribute back.

## ðŸ™ Credits

Built for the [Hermes Agent](https://github.com/NousResearch/hermes-agent) community.

---

<div align="center">

**â­ Star this repo if it saved your data!**
**â­ Ø§Ú¯Ù‡ Ø§ÛŒÙ† Ø§Ø¨Ø²Ø§Ø± Ø¨Ù‡ Ú©Ø§Ø±ØªÙˆÙ† Ø§ÙˆÙ…Ø¯ØŒ Ø³ØªØ§Ø±Ù‡ Ø¨Ø¯ÛŒØ¯!**

</div>
