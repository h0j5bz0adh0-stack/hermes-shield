
```markdown
<div align="center">

# 🛡️ Hermes Shield | هرمس شیلد

[![Version](https://img.shields.io/badge/Version-v1.3.0-blue.svg?style=for-the-badge)](https://github.com/h0j5bz0adh0-stack/hermes-shield)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Agent](https://img.shields.io/badge/Agent-Hermes%20%7C%20Claude%20Code%20%7C%20OpenClaw-purple.svg?style=for-the-badge)](https://github.com/NousResearch/hermes-agent)

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
- ✅ **سازگار با سرورهای headless** (بدون مرورگر)

### نصب سریع

```bash
git clone https://github.com/h0j5bz0adh0-stack/hermes-shield.git
cd hermes-shield
pip install cryptography
python3 scripts/hermes-shield.py backup
```

نصب به عنوان اسکیل هرمس

```bash
mkdir -p ~/.hermes/skills/devops/hermes-shield
cp SKILL.md ~/.hermes/skills/devops/hermes-shield/
cp -r scripts ~/.hermes/skills/devops/hermes-shield/
pip install cryptography
```

دستورات

دستور توضیح
backup بک‌آپ کامل
backup -l "توضیحات" بک‌آپ با برچسب
backup -e -p رمز بک‌آپ رمزنگاری‌شده
backup -c بک‌آپ + آپلود گوگل درایو
restore بازیابی آخرین نسخه
restore -f فایل بازیابی از فایل مشخص
restore -t skills,config بازیابی فقط بخش‌های مشخص
list نمایش لیست بک‌آپ‌ها
list --cloud نمایش بک‌آپ‌های ابری
push آپلود آخرین بک‌آپ به گوگل درایو
pull دانلود آخرین بک‌آپ از گوگل درایو
verify فایل بررسی سلامت بک‌آپ
diff A.tar.gz B.tar.gz مقایسه دو بک‌آپ
stats نمایش آمار
config نمایش تنظیمات
connect اتصال گوگل درایو (سرور headless)
setup راه‌اندازی تعاملی
setup-auto راه‌اندازی خودکار (برای هرمس)
token <JSON> اعمال توکن گوگل درایو

چیا بک‌آپ میشه؟

```
~/.hermes/
├── skills/          ✅ اسکیل‌ها و ورک‌فلوها
├── plugins/         ✅ پلاگین‌ها
├── cron/            ✅ جاب‌های زمان‌بندی
├── memories/        ✅ حافظه پایدار
├── config.yaml      ✅ تنظیمات اصلی
└── sessions/        ⚙️ تاریخچه (اختیاری)
```

رمزنگاری

از AES-256 با PBKDF2 (۴۸۰,۰۰۰ تکرار) استفاده میکنه — همون استاندارد رمزنگاری بانک‌ها و مدیر رمز عبور.

```bash
python3 scripts/hermes-shield.py backup -e -p "رمز-امن-من"
python3 scripts/hermes-shield.py restore -f backup.tar.gz
```

اتصال گوگل درایو (سرور Headless)

```bash
# ۱. اتصال
python3 scripts/hermes-shield.py connect

# ۲. روی لپ‌تاپ/موبایل:
#    الف) rclone رو دانلود کن:
#    https://downloads.rclone.org/current/rclone-current-windows-amd64.zip
#    ب) فقط extract کن (نیازی به نصب نیست)
#    ج) توی پوشه rclone ترمینال باز کن
#    د) این دستور رو بزن:
rclone authorize "drive"

# ۳. یه پنجره مرورگر باز میشه → اکانت گوگلت رو انتخاب کن → Allow بزن
# ۴. یه متن JSON بهت میده → کپی کن و اینجا بفرست:
python3 scripts/hermes-shield.py token '{"access_token":"...","refresh_token":"...",...}'

# ۵. فعال کردن بک‌آپ خودکار
python3 scripts/hermes-shield.py config set cloud_enabled=true
```

بک‌آپ خودکار هر ۲ روز

```bash
# crontab
0 3 */2 * * /usr/bin/python3 /path/to/hermes-shield.py backup -l "auto" -c
```

پشتیبانی از ایجنت‌ها

ایجنت مسیر تنظیمات وضعیت
Hermes Agent ~/.hermes/ ✅ کامل
Claude Code ~/.claude/ ✅ جزئی
OpenClaw ~/.openclaw/ ✅ جزئی
ایجنت سفارشی هر مسیری 🔧 قابل تنظیم

---

<a id="-why-hermes-shield"></a>

🎯 English

Why Hermes Shield?

AI agents like Hermes, Claude Code, and OpenClaw store critical state locally — skills, plugins, cron jobs, memory, configuration. If you lose this, you lose weeks of work.

Hermes Shield gives you:

· ✅ One-command backup of everything
· ✅ AES-256 encryption (military-grade)
· ✅ Automatic versioning & cleanup
· ✅ Restore any point in time
· ✅ Diff between backups
· ✅ Cross-agent compatibility
· ✅ Google Drive sync — auto backup every 2 days
· ✅ Headless server compatible (no browser needed)

🚀 Quick Start

```bash
git clone https://github.com/h0j5bz0adh0-stack/hermes-shield.git
cd hermes-shield
pip install cryptography
python3 scripts/hermes-shield.py backup
```

📋 Commands

Command Description
backup Create a full backup
backup -l "label" Create a labeled backup
backup -e -p PASS Create an encrypted backup
backup -c Backup + upload to Google Drive
restore Restore the latest backup
restore -f FILE Restore from a specific file
restore -t skills,config Restore only selected targets
list List local backups
list --cloud List cloud backups
push Upload latest to Google Drive
pull Download latest from Google Drive
pull -f FILE Download specific from Google Drive
verify FILE Verify backup integrity
stats Show backup statistics
config View configuration
config set key=value Update a config setting
connect Connect Google Drive (headless)
setup Interactive setup wizard
setup-auto Non-interactive setup (for Hermes)
token <JSON> Apply Google Drive auth token

🔒 Encryption

Uses AES-256-CBC with PBKDF2 key derivation (480,000 iterations, SHA-256).

```bash
# Encrypted backup
python3 scripts/hermes-shield.py backup -e -p "my-secure-password"

# Restore
python3 scripts/hermes-shield.py restore -f backup.tar.gz
```

☁️ Google Drive Sync (Headless Server)

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

# 3. A browser window opens → select your Google account → Allow
# 4. It outputs a JSON token → copy it and send here:
python3 scripts/hermes-shield.py token '{"access_token":"...","refresh_token":"...",...}'

# 5. Enable auto backup
python3 scripts/hermes-shield.py config set cloud_enabled=true
```

🤖 Hermes Agent Integration

When user says: "بک‌آپ گوگل درایو هر ۲ روز بگیر"

Hermes runs:

```bash
python3 scripts/hermes-shield.py setup-auto --cloud yes --interval 48
```

Outputs JSON with auth instructions. User sends token. Hermes applies it:

```bash
python3 scripts/hermes-shield.py token '<JSON>'
```

📁 What Gets Backed Up

```
~/.hermes/
├── skills/          ✅ All skills & workflows
├── plugins/         ✅ Extensions & plugins
├── cron/            ✅ Scheduled jobs
├── memories/        ✅ Persistent memory
├── config.yaml      ✅ Main configuration
└── sessions/        ⚙️ Optional (large)
```

🤖 Cross-Agent Support

Agent Config Path Status
Hermes Agent ~/.hermes/ ✅ Full
Claude Code ~/.claude/ ✅ Partial
OpenClaw ~/.openclaw/ ✅ Partial
Custom Any path 🔧 Configurable

📊 Stats

```bash
$ python3 scripts/hermes-shield.py stats

🛡️  Hermes Shield v1.3.0 — Stats

  Local backups:    12
  Local size:       2.3 MB
  Cloud backups:    5
  Max local:        10
  Max cloud:        5
  Auto backup:      ✅ Every 48h
  Cloud sync:       ✅
  Google Drive:     ✅ Connected
  Current data:     45.2 KB
```

🛣️ Roadmap

· Dropbox / OneDrive support
· S3 / Cloudflare R2 remote storage
· Sync between multiple machines
· Web dashboard
· Compression level options

🤝 Contributing

Contributions welcome! 🐛 Report bugs • 💡 Suggest features • 🔧 Submit PRs

📜 License

MIT License — use freely, contribute back.

🙏 Credits

Built for the Hermes Agent community.

---

<div align="center">

⭐ Star this repo if it saved your data!
⭐ اگه این ابزار به کارتون اومد، ستاره بدید!

</div>
```
