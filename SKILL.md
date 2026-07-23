---
name: hermes-shield
description: "Use when backing up, restoring, or syncing Hermes Agent state. Full backup/restore engine with encryption, versioning, Google Drive sync, and cross-agent support."
version: 1.1.0
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

Hermes Shield is a complete backup/restore engine for AI agent configurations with **Google Drive sync**. Back up skills, plugins, cron jobs, memory, and config with AES-256 encryption, automatic versioning, and cloud sync.

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
| `setup-rclone` | Interactive Google Drive setup |

## Installation

```bash
# Clone
git clone https://github.com/your-username/hermes-shield.git
cd hermes-shield

# Install dependencies
pip install cryptography
# rclone is pre-installed on most systems, or:
curl -fsSL https://rclone.org/install.sh | bash

# Test
python3 scripts/hermes-shield.py stats
```

## Google Drive Setup (One-Time)

```bash
# Run interactive setup
python3 scripts/hermes-shield.py setup-rclone

# Or manually:
rclone config
# → New remote → Name: hermes-gdrive → Storage: Google Drive → Done

# Enable auto cloud sync
python3 scripts/hermes-shield.py config set cloud_enabled=true

# Test upload
python3 scripts/hermes-shield.py backup -c
```

## Automated Cloud Backups

```bash
# Every 2 days (48 hours) — local + Google Drive
# Add to crontab:
0 3 */2 * * /usr/bin/python3 /path/to/hermes-shield.py backup -l "auto" -c

# Or use Hermes Agent cron:
# Schedule: every 48h
# Prompt: Run hermes-shield backup with label "auto" and upload to cloud
```

## Commands

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
| `stats` | Show statistics |
| `config` | View configuration |
| `config set key=value` | Update a config setting |
| `setup-rclone` | Interactive Google Drive setup |

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
