---
name: hermes-shield
description: "Use when backing up, restoring, or syncing Hermes Agent state. Full backup/restore engine with encryption, versioning, Google Drive sync, and cross-agent support."
version: 1.3.0
author: Reza (Autonexus)
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [python3, rclone]
  python_packages: [cryptography]
metadata:
  hermes:
    tags: [backup, restore, sync, encryption, google-drive, cloud, data-safety]
    related_skills: []
---

# Hermes Shield — Backup, Restore & Sync

## Overview

Hermes Shield is a complete backup/restore engine for AI agent configurations with **Google Drive sync**. Back up skills, plugins, cron jobs, memory, and config with AES-256 encryption, automatic versioning, and cloud sync. Works on headless servers without a browser.

## When to Use

- Before making major changes to skills, plugins, or config
- After completing a complex multi-session project
- When migrating to a new server or machine
- For periodic automated backups to cloud

## Quick Reference

| Command | Description |
|---------|-------------|
| `backup` | Full local backup |
| `backup -c` | Backup + upload to Google Drive |
| `backup -e -p PASS` | Encrypted backup |
| `restore` | Restore latest |
| `restore -f FILE` | Restore specific backup |
| `restore -t skills,config` | Restore only targets |
| `list` | List local backups |
| `list --cloud` | List cloud backups |
| `push` | Upload latest backup to Google Drive |
| `pull` | Download latest from Google Drive |
| `pull -f FILE` | Download specific from Google Drive |
| `verify FILE` | Verify backup integrity |
| `stats` | Show statistics |
| `config` | View/update config |
| `connect` | Connect Google Drive (headless) |
| `setup` | Interactive setup wizard |
| `setup-auto` | Non-interactive setup (for Hermes) |
| `token <JSON>` | Apply Google Drive auth token |

## Installation

```bash
# Clone
git clone https://github.com/h0j5bz0adh0-stack/hermes-shield.git
cd hermes-shield

# Install dependencies
pip install cryptography
# rclone for Google Drive support:
curl -fsSL https://rclone.org/install.sh | bash

# Test
python3 scripts/hermes-shield.py stats
```

## As Hermes Skill

```bash
mkdir -p ~/.hermes/skills/devops/hermes-shield
cp SKILL.md ~/.hermes/skills/devops/hermes-shield/
cp -r scripts ~/.hermes/skills/devops/hermes-shield/
pip install cryptography
```

## Google Drive Setup (Headless Server)

```bash
# 1. Connect
python3 scripts/hermes-shield.py connect

# 2. On your laptop/phone:
rclone authorize "drive"

# 3. Send the JSON token:
python3 scripts/hermes-shield.py token '{"access_token":"...","refresh_token":"...",...}'

# 4. Enable auto backup
python3 scripts/hermes-shield.py config set cloud_enabled=true
```

## Hermes Agent Integration

User says: "بک‌آپ گوگل درایو هر ۲ روز بگیر"

Hermes runs:
```bash
python3 scripts/hermes-shield.py setup-auto --cloud yes --interval 48
```

Hermes presents auth instructions to user. User sends token. Hermes applies:
```bash
python3 scripts/hermes-shield.py token '<JSON>'
```

## Automated Cloud Backups

```bash
# Every 2 days
0 3 */2 * * /usr/bin/python3 /path/to/hermes-shield.py backup -l "auto" -c
```

## Configuration

| Key | Default | Description |
|-----|---------|-------------|
| `auto_backup_enabled` | `true` | Enable auto backups |
| `auto_backup_interval_hours` | `48` | Hours between backups |
| `max_backups` | `10` | Max local backups to keep |
| `max_cloud_backups` | `5` | Max cloud backups to keep |
| `encryption_enabled` | `false` | Encrypt by default |
| `cloud_enabled` | `false` | Auto-upload to Google Drive |
| `cloud_folder` | `hermes-shield` | Google Drive folder name |
