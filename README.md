<div align="center">

# 🛡️ Hermes Shield | هرمس شیلد

[![Version](https://img.shields.io/badge/Version-v1.1.0-blue.svg?style=for-the-badge)](https://github.com/your-username/hermes-shield)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Agent](https://img.shields.io/badge/Agent-Hermes%20%7C%20Claude%20%20OpenClaw-purple.svg?style=for-the-badge)](https://github.com/NousResearch/hermes-agent)

**Backup, Restore & Sync for AI Agent Configurations**
**بک‌آپ، بازیابی و همگام‌سازی تنظیمات ایجنت هوش مصنوعی**

[English](#-why-hermes-shield) • [فارسی](#فارسی) • [Quick Start](#-quick-start) • [Commands](#-commands)

</div>

---

<a id="فارسی"></a>

## 🇮🇷 فارسی

### چرا هرمس شیلد؟

ایجنت‌های هوش مصنوعی مثل **Hermes**، **Claude Code** و **OpenClaw** تنظیمات حیاتی‌شون رو روی سیستم شما ذخیره میکنن — اسکیل‌ها، پلاگین‌ها، cron job ها، حافظه و کانفیگ. اگه اینا از بین برن، هفته‌ها کار از دست میره!

**هرمس شیلد** بهتون اینا رو میده:
- ✅ بک‌آپ کامل با **یه دستور**
- ✅ رمزنگاری **AES-256** (استاندارد نظامی)
- ✅ نسخه‌بندی خودکار و پاکسازی
- ✅ بازیابی از هر نقطه در زمان
- ✅ مقایسه دو بک‌آپ (Diff)
- ✅ سازگار با **هرمس، Claude Code، OpenClaw**
- ✅ **بک‌آپ خودکار روی گوگل درایو** هر ۲ روز

### نصب سریع

```bash
# کلون کنید
git clone https://github.com/your-username/hermes-shield.git
cd hermes-shield

# نصب وابستگی
pip install cryptography

# بک‌آپ بگیرید
python3 scripts/hermes-shield.py backup
```

### نصب به عنوان اسکیل هرمس

```bash
mkdir -p ~/.hermes/skills/devops/hermes-shield
cp SKILL.md ~/.hermes/skills/devops/hermes-shield/
cp -r scripts ~/.hermes/skills/devops/hermes-shield/
pip install cryptography
```

### دستورات

| دستور | توضیح |
|-------|-------|
| `backup` | بک‌آپ کامل |
| `backup -l "توضیحات"` | بک‌آپ با برچسب |
| `backup -e -p رمز` | بک‌آپ رمزنگاری‌شده |
| `backup -c` | بک‌آپ + آپلود گوگل درایو |
| `restore` | بازیابی آخرین نسخه |
| `restore -f فایل` | بازیابی از فایل مشخص |
| `restore -t skills,config` | بازیابی فقط بخش‌های مشخص |
| `list` | نمایش لیست بک‌آپ‌ها |
| `list --cloud` | نمایش بک‌آپ‌های ابری |
| `push` | آپلود آخرین بک‌آپ به گوگل درایو |
| `pull` | دانلود آخرین بک‌آپ از گوگل درایو |
| `verify فایل` | بررسی سلامت بک‌آپ |
| `diff A.tar.gz B.tar.gz` | مقایسه دو بک‌آپ |
| `stats` | نمایش آمار |
| `config` | نمایش تنظیمات |
| `setup-rclone` | راه‌اندازی گوگل درایو |
| `config set key=value` | تغییر تنظیمات |

### چیا بک‌آپ میشه؟

```
~/.hermes/
├── skills/          ✅ اسکیل‌ها و ورک‌فلوها
├── plugins/         ✅ پلاگین‌ها
├── cron/            ✅ جاب‌های زمان‌بندی
├── memories/        ✅ حافظه پایدار
├── config.yaml      ✅ تنظیمات اصلی
└── sessions/        ⚙️ تاریخچه (اختیاری)
```

### رمزنگاری

از **AES-256** با **PBKDF2** (۴۸۰,۰۰۰ تکرار) استفاده میکنه — همون استاندارد رمزنگاری بانک‌ها و مدیر رمز عبور.

```bash
python3 scripts/hermes-shield.py backup -e -p "رمز-امن-من"
python3 scripts/hermes-shield.py restore -f backup.tar.gz
```

### بک‌آپ خودکار

```bash
# اضافه کردن به crontab (هر روز ساعت ۳ صبح)
0 3 * * * /usr/bin/python3 /path/to/hermes-shield.py backup -l "auto-daily"
```

### راه‌اندازی گوگل درایو

```bash
# یک‌بار تنظیم کنید (interactive)
python3 scripts/hermes-shield.py setup-rclone

# فعال کردن بک‌آپ خودکار ابری
python3 scripts/hermes-shield.py config set cloud_enabled=true

# تست آپلود
python3 scripts/hermes-shield.py backup -c

# بک‌آپ هر ۲ روز روی گوگل درایو
0 3 */2 * * /usr/bin/python3 /path/to/hermes-shield.py backup -l "auto" -c
```

### پشتیبانی از ایجنت‌ها

| ایجنت | مسیر تنظیمات | وضعیت |
|-------|-------------|-------|
| Hermes Agent | `~/.hermes/` | ✅ کامل |
| Claude Code | `~/.claude/` | ✅ جزئی |
| OpenClaw | `~/.openclaw/` | ✅ جزئی |
| ایجنت سفارشی | هر مسیری | 🔧 قابل تنظیم |

---

<a id="-why-hermes-shield"></a>

## 🎯 English

### Why Hermes Shield?

AI agents like Hermes, Claude Code, and OpenClaw store critical state locally — skills, plugins, cron jobs, memory, configuration. If you lose this, you lose weeks of work.

**Hermes Shield** gives you:
- ✅ One-command backup of everything
- ✅ AES-256 encryption (military-grade)
- ✅ Automatic versioning & cleanup
- ✅ Restore any point in time
- ✅ Diff between backups
- ✅ Cross-agent compatibility
- ✅ **Google Drive sync** — auto backup every 2 days

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/your-username/hermes-shield.git
cd hermes-shield

# Install dependency
pip install cryptography

# Create your first backup
python3 scripts/hermes-shield.py backup

# List backups
python3 scripts/hermes-shield.py list
```

## 📋 Commands

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
| `setup-rclone` | Interactive Google Drive setup |

## 🔒 Encryption

Uses **AES-256-CBC** with **PBKDF2** key derivation (480,000 iterations, SHA-256).

```bash
# Encrypted backup
python3 scripts/hermes-shield.py backup -e -p "my-secure-password"

# Restore
python3 scripts/hermes-shield.py restore -f backup.tar.gz
```

## ☁️ Google Drive Sync

One-time setup:
```bash
python3 scripts/hermes-shield.py setup-rclone
```

Enable auto cloud sync:
```bash
python3 scripts/hermes-shield.py config set cloud_enabled=true
```

Auto backup every 2 days:
```bash
# Add to crontab
0 3 */2 * * /usr/bin/python3 /path/to/hermes-shield.py backup -l "auto" -c
```

Manual upload/download:
```bash
python3 scripts/hermes-shield.py push    # Upload latest
python3 scripts/hermes-shield.py pull    # Download latest
python3 scripts/hermes-shield.py list --cloud  # List cloud backups
```

## 📁 What Gets Backed Up

```
~/.hermes/
├── skills/          ✅ All skills & workflows
├── plugins/         ✅ Extensions & plugins
├── cron/            ✅ Scheduled jobs
├── memories/        ✅ Persistent memory
├── config.yaml      ✅ Main configuration
└── sessions/        ⚙️ Optional (large)
```

## 🤖 Cross-Agent Support

| Agent | Config Path | Status |
|-------|-------------|--------|
| Hermes Agent | `~/.hermes/` | ✅ Full |
| Claude Code | `~/.claude/` | ✅ Partial |
| OpenClaw | `~/.openclaw/` | ✅ Partial |
| Custom | Any path | 🔧 Configurable |

## 📊 Stats

```bash
$ python3 scripts/hermes-shield.py stats

🛡️  Hermes Shield — Stats

  Backups:       12
  Total size:    2.3 MB
  Latest:        2026-07-23 14:30
  Max backups:   10
  Encryption:    ✅
  Auto backup:   ✅ Every 24h
  Current data:  45.2 KB
```

## 🛣️ Roadmap

- [ ] Google Drive / Dropbox upload
- [ ] S3 / Cloudflare R2 remote storage
- [ ] Sync between multiple machines
- [ ] Web dashboard
- [ ] Compression level options

## 🤝 Contributing

Contributions welcome! 🐛 Report bugs • 💡 Suggest features • 🔧 Submit PRs

## 📜 License

MIT License — use freely, contribute back.

## 🙏 Credits

Built for the [Hermes Agent](https://github.com/NousResearch/hermes-agent) community.

---

<div align="center">

**⭐ Star this repo if it saved your data!**
**⭐ اگه این ابزار به کارتون اومد، ستاره بدید!**

</div>
