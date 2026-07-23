#!/usr/bin/env python3
"""
Hermes Shield — Backup, Restore & Sync for AI Agents
With Google Drive support via rclone (headless server compatible)
"""

import os
import sys
import json
import shutil
import hashlib
import tarfile
import subprocess
import argparse
import getpass
from pathlib import Path
from datetime import datetime

VERSION = "1.3.0"

# ─── Paths ────────────────────────────────────────────────────────
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
BACKUP_DIR = HERMES_HOME / "backups"
CONFIG_FILE = HERMES_HOME / "shield.json"
RCLONE_CONF = Path.home() / ".config" / "rclone" / "rclone.conf"

# Directories to back up
BACKUP_TARGETS = {
    "skills":     HERMES_HOME / "skills",
    "plugins":    HERMES_HOME / "plugins",
    "cron":       HERMES_HOME / "cron",
    "memories":   HERMES_HOME / "memories",
    "config":     HERMES_HOME / "config.yaml",
    "sessions":   HERMES_HOME / "sessions",
}

RCLONE_REMOTE = "hermes-gdrive"

# ─── Colors ───────────────────────────────────────────────────────
class C:
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"

def ok(msg):   print(f"{C.GREEN}✓{C.RESET} {msg}")
def warn(msg): print(f"{C.YELLOW}⚠{C.RESET} {msg}")
def err(msg):  print(f"{C.RED}✗{C.RESET} {msg}")
def info(msg): print(f"{C.CYAN}→{C.RESET} {msg}")

# ─── Rclone Helpers ──────────────────────────────────────────────
def rclone_available() -> bool:
    return shutil.which("rclone") is not None

def rclone_configured() -> bool:
    if not rclone_available():
        return False
    # Check if remote exists in config
    if RCLONE_CONF.exists():
        content = RCLONE_CONF.read_text()
        if f"[{RCLONE_REMOTE}]" in content:
            return True
    try:
        result = subprocess.run(
            ["rclone", "listremotes"],
            capture_output=True, text=True, timeout=10
        )
        return f"{RCLONE_REMOTE}:" in result.stdout
    except Exception:
        return False

def rclone_has_token() -> bool:
    """Check if remote has a valid token (not just config entry)"""
    if not rclone_configured():
        return False
    try:
        # Try a simple operation to verify token works
        result = subprocess.run(
            ["rclone", "lsd", f"{RCLONE_REMOTE}:"],
            capture_output=True, text=True, timeout=15
        )
        return result.returncode == 0
    except Exception:
        return False

def rclone_create_remote():
    """Create rclone remote config entry (no auth yet)"""
    try:
        # Remove old config if exists
        subprocess.run(
            ["rclone", "config", "delete", RCLONE_REMOTE],
            capture_output=True, timeout=10
        )
        # Create new config
        result = subprocess.run(
            ["rclone", "config", "create", RCLONE_REMOTE, "drive",
             "scope", "drive",
             "config", str(RCLONE_CONF)],
            capture_output=True, text=True, timeout=15
        )
        return result.returncode == 0
    except Exception:
        return False

def rclone_apply_token(token_json: str) -> bool:
    """Apply rclone auth token from JSON string"""
    # Ensure config entry exists
    if not rclone_configured():
        if not rclone_create_remote():
            err("Failed to create rclone config entry")
            return False
    
    try:
        # Parse and validate JSON
        token_data = json.loads(token_json)
        
        # Build token string for rclone
        # rclone expects: {"access_token":"...","token_type":"Bearer","refresh_token":"..."}
        token_str = json.dumps(token_data)
        
        # Update config with token
        result = subprocess.run(
            ["rclone", "config", "update", RCLONE_REMOTE,
             "token", token_str,
             "config", str(RCLONE_CONF)],
            capture_output=True, text=True, timeout=15
        )
        
        if result.returncode != 0:
            # Try alternative method: write directly to config file
            return _rclone_write_token_manual(token_data)
        
        return True
    except json.JSONDecodeError:
        err("Invalid JSON token")
        return False
    except Exception as e:
        err(f"Token apply error: {e}")
        return False

def _rclone_write_token_manual(token_data: dict) -> bool:
    """Manually write token to rclone config file"""
    try:
        if not RCLONE_CONF.exists():
            RCLONE_CONF.parent.mkdir(parents=True, exist_ok=True)
        
        content = RCLONE_CONF.read_text() if RCLONE_CONF.exists() else ""
        
        # Find or create section
        section = f"[{RCLONE_REMOTE}]"
        if section not in content:
            content += f"\n{section}\ntype = drive\nscope = drive\n"
        
        # Remove old token line
        lines = content.splitlines()
        new_lines = []
        for line in lines:
            if not line.strip().startswith("token ="):
                new_lines.append(line)
        
        # Add new token
        token_line = f"token = {json.dumps(token_data)}"
        inserted = False
        for i, line in enumerate(new_lines):
            if line.strip() == section:
                # Insert token after section header
                for j in range(i+1, len(new_lines)):
                    if new_lines[j].strip().startswith("type ="):
                        new_lines.insert(j+1, token_line)
                        inserted = True
                        break
                if not inserted:
                    new_lines.insert(i+1, token_line)
                break
        
        if not inserted:
            new_lines.append(token_line)
        
        RCLONE_CONF.write_text("\n".join(new_lines) + "\n")
        return True
    except Exception as e:
        err(f"Manual token write error: {e}")
        return False

def rclone_upload(local_path: Path, remote_path: str) -> bool:
    if not rclone_configured():
        err(f"rclone remote '{RCLONE_REMOTE}' not configured!")
        return False
    cmd = ["rclone", "copy", str(local_path), f"{RCLONE_REMOTE}:{remote_path}", "--progress"]
    info(f"Uploading to Google Drive: {local_path.name}")
    result = subprocess.run(cmd, timeout=600)
    return result.returncode == 0

def rclone_download(remote_path: str, local_path: Path) -> bool:
    if not rclone_configured():
        return False
    local_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["rclone", "copy", f"{RCLONE_REMOTE}:{remote_path}", str(local_path.parent), "--progress"]
    info(f"Downloading from Google Drive: {remote_path}")
    result = subprocess.run(cmd, timeout=600)
    return result.returncode == 0

def rclone_list(remote_path: str = "hermes-shield") -> list:
    if not rclone_configured():
        return []
    cmd = ["rclone", "ls", f"{RCLONE_REMOTE}:{remote_path}", "--include", "backup_*.tar.gz", "--format", "t"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        files = []
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                parts = line.rsplit(None, 1)
                if len(parts) == 2:
                    files.append({"name": parts[1], "size": int(parts[0])})
        return sorted(files, key=lambda x: x["name"], reverse=True)
    except Exception:
        return []

def rclone_delete(remote_file: str, remote_path: str = "hermes-shield") -> bool:
    if not rclone_configured():
        return False
    cmd = ["rclone", "deletefile", f"{RCLONE_REMOTE}:{remote_path}/{remote_file}"]
    result = subprocess.run(cmd, timeout=30)
    return result.returncode == 0

# ─── Config ───────────────────────────────────────────────────────
def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {
        "auto_backup_enabled": True,
        "auto_backup_interval_hours": 48,
        "max_backups": 10,
        "max_cloud_backups": 5,
        "encryption_enabled": False,
        "exclude_patterns": ["*.pyc", "__pycache__", ".git", "node_modules"],
        "cloud_enabled": False,
        "cloud_folder": "hermes-shield",
    }

def save_config(cfg: dict):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))

# ─── Backup ──────────────────────────────────────────────────────
def create_backup(label="", targets=None, password=None, dry_run=False, upload_cloud=False):
    cfg = load_config()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"backup_{timestamp}" + (f"_{label}" if label else "")
    backup_path = BACKUP_DIR / name
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    items = targets or list(BACKUP_TARGETS.keys())
    exclude = cfg.get("exclude_patterns", [])

    if dry_run:
        info(f"Dry run — would create: {backup_path}")
    
    total_size = 0
    file_count = 0

    for item_name in items:
        src = BACKUP_TARGETS.get(item_name)
        if not src:
            warn(f"Unknown target: {item_name}, skipping")
            continue
        if not src.exists():
            warn(f"{item_name}: not found, skipping")
            continue

        if dry_run:
            if src.is_dir():
                files = list(src.rglob("*"))
                file_count += len([f for f in files if f.is_file()])
                total_size += sum(f.stat().st_size for f in files if f.is_file())
            else:
                file_count += 1
                total_size += src.stat().st_size
            info(f"  {item_name}: {src}")
        else:
            dest = backup_path / item_name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dest, ignore=shutil.ignore_patterns(*exclude))
            else:
                shutil.copy2(src, dest)

    if dry_run:
        info(f"Files: {file_count} | Size: {total_size / 1024:.1f} KB")
        return None

    tarball = BACKUP_DIR / f"{name}.tar.gz"
    with tarfile.open(tarball, "w:gz") as tar:
        tar.add(backup_path, arcname=name)
    
    shutil.rmtree(backup_path)

    if password:
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            import base64
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            fernet = Fernet(key)
            data = tarball.read_bytes()
            tarball.write_bytes(salt + fernet.encrypt(data))
            ok("Backup encrypted with AES-256")
        except ImportError:
            warn("cryptography not installed — skipping encryption")

    meta = {
        "name": name, "timestamp": timestamp, "created": datetime.now().isoformat(),
        "label": label, "targets": items, "tarball": str(tarball),
        "tarball_size": tarball.stat().st_size, "encrypted": password is not None,
    }
    (BACKUP_DIR / f"{name}_meta.json").write_text(json.dumps(meta, indent=2))

    cleanup_old_backups(cfg.get("max_backups", 10))

    size_kb = tarball.stat().st_size / 1024
    ok(f"Backup created: {tarball.name} ({size_kb:.1f} KB)")

    if upload_cloud or cfg.get("cloud_enabled"):
        cloud_folder = cfg.get("cloud_folder", "hermes-shield")
        if rclone_has_token():
            if rclone_upload(tarball, cloud_folder):
                ok(f"Uploaded to Google Drive: {cloud_folder}/{tarball.name}")
                cleanup_cloud_backups(cfg.get("max_cloud_backups", 5), cloud_folder)
            else:
                warn("Cloud upload failed — backup saved locally")
        else:
            warn("Google Drive not authenticated yet — run: hermes-shield connect")

    return tarball

def cleanup_old_backups(keep):
    backups = sorted(BACKUP_DIR.glob("backup_*.tar.gz"), key=lambda f: f.stat().st_mtime)
    for old in backups[:max(0, len(backups) - keep)]:
        old.unlink(missing_ok=True)
        info(f"Old backup removed: {old.name}")

def cleanup_cloud_backups(keep, cloud_folder):
    remote_backups = rclone_list(cloud_folder)
    if len(remote_backups) > keep:
        for old in remote_backups[keep:]:
            if rclone_delete(old["name"], cloud_folder):
                info(f"Old cloud backup removed: {old['name']}")

# ─── Restore ─────────────────────────────────────────────────────
def restore_backup(backup_file=None, targets=None, password=None, dry_run=False):
    if backup_file is None:
        backups = sorted(BACKUP_DIR.glob("backup_*.tar.gz"), key=lambda f: f.stat().st_mtime)
        if not backups:
            err("No backups found!")
            return False
        backup_file = backups[-1]
        info(f"Latest backup: {backup_file.name}")

    if not backup_file.exists():
        err(f"Backup not found: {backup_file}")
        return False

    tmp_file = backup_file
    if password:
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            import base64
            raw = backup_file.read_bytes()
            salt, encrypted = raw[:16], raw[16:]
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            decrypted = Fernet(key).decrypt(encrypted)
            tmp_file = BACKUP_DIR / f".tmp_{backup_file.name}"
            tmp_file.write_bytes(decrypted)
        except ImportError:
            err("cryptography not installed!"); return False
        except Exception:
            err("Wrong password or corrupted backup!"); return False

    try:
        with tarfile.open(tmp_file, "r:gz") as tar:
            restore_list = []
            for m in tar.getmembers():
                parts = m.name.split("/", 1)
                if len(parts) > 1:
                    target_name = parts[1].split("/")[0] if "/" in parts[1] else parts[1]
                    if targets and target_name not in targets:
                        continue
                    restore_list.append(m)

            if dry_run:
                info(f"Dry run — would restore from: {backup_file.name}")
                for m in restore_list:
                    info(f"  {m.name}")
                return True

            info(f"Restoring {len(restore_list)} items to {HERMES_HOME}")
            tar.extractall(HERMES_HOME, members=restore_list)

            for m in restore_list:
                src_path = HERMES_HOME / m.name
                if src_path.exists():
                    parts = m.name.split("/", 1)
                    if len(parts) > 1:
                        dest = HERMES_HOME / parts[1]
                        if src_path.is_dir() and not dest.exists():
                            src_path.rename(dest)
                        elif src_path.is_file():
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            if dest.exists(): dest.unlink()
                            src_path.rename(dest)
    finally:
        if password and tmp_file.exists():
            tmp_file.unlink()

    ok("Restore complete!")
    return True

# ─── List ────────────────────────────────────────────────────────
def list_backups(cloud=False):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    if cloud:
        cfg = load_config()
        backups = rclone_list(cfg.get("cloud_folder", "hermes-shield"))
        source = "Google Drive"
    else:
        backups = sorted(BACKUP_DIR.glob("backup_*.tar.gz"), key=lambda f: f.stat().st_mtime, reverse=True)
        source = "Local"

    if not backups:
        warn(f"No backups found on {source}")
        return

    print(f"\n{C.BOLD}📦 Backups on {source} ({len(backups)}){C.RESET}\n")
    for i, b in enumerate(backups):
        if cloud:
            name, size_kb = b["name"], b["size"] / 1024
            marker = " → latest" if i == 0 else ""
            print(f"  {C.CYAN}{name}{C.RESET}  {C.DIM}{size_kb:.1f} KB{C.RESET}{marker}")
        else:
            size_kb = b.stat().st_size / 1024
            mtime = datetime.fromtimestamp(b.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            marker = " → latest" if i == 0 else ""
            print(f"  {C.CYAN}{b.name}{C.RESET}  {C.DIM}{size_kb:.1f} KB  {mtime}{C.RESET}{marker}")
    print()

# ─── Verify ──────────────────────────────────────────────────────
def verify_backup(backup_file, password=None):
    info(f"Verifying: {backup_file.name}")
    tmp_file = backup_file
    if password:
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            import base64
            raw = backup_file.read_bytes()
            salt, encrypted = raw[:16], raw[16:]
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            decrypted = Fernet(key).decrypt(encrypted)
            tmp_file = BACKUP_DIR / ".tmp_verify"
            tmp_file.write_bytes(decrypted)
        except Exception:
            err("Decryption failed!"); return False

    try:
        with tarfile.open(tmp_file, "r:gz") as tar:
            members = tar.getmembers()
            errors = []
            for m in members:
                if m.isfile():
                    try: tar.extractfile(m).read(1024)
                    except Exception as e: errors.append(f"{m.name}: {e}")
            if errors:
                for e in errors: err(e)
                return False
            ok(f"Backup valid — {len(members)} items")
            return True
    except Exception as e:
        err(f"Corrupt backup: {e}")
        return False
    finally:
        if password and tmp_file.exists(): tmp_file.unlink()

# ─── Cloud Operations ────────────────────────────────────────────
def pull_from_cloud(backup_name=None):
    cfg = load_config()
    cloud_folder = cfg.get("cloud_folder", "hermes-shield")
    
    if backup_name:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        if rclone_download(f"{cloud_folder}/{backup_name}", BACKUP_DIR):
            ok(f"Downloaded: {backup_name}")
        else:
            err(f"Failed to download: {backup_name}")
    else:
        backups = rclone_list(cloud_folder)
        if not backups:
            warn("No backups on Google Drive"); return
        latest = backups[0]["name"]
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        if rclone_download(f"{cloud_folder}/{latest}", BACKUP_DIR):
            ok(f"Downloaded latest: {latest}")
        else:
            err("Download failed!")

# ─── Stats ───────────────────────────────────────────────────────
def show_stats():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backups = list(BACKUP_DIR.glob("backup_*.tar.gz"))
    cfg = load_config()

    cloud_backups = []
    if rclone_has_token():
        cloud_backups = rclone_list(cfg.get("cloud_folder", "hermes-shield"))

    print(f"\n{C.BOLD}🛡️  Hermes Shield v{VERSION} — Stats{C.RESET}\n")
    print(f"  {C.CYAN}Local backups:{C.RESET}    {len(backups)}")
    
    if backups:
        total_size = sum(b.stat().st_size for b in backups)
        latest = max(backups, key=lambda b: b.stat().st_mtime)
        print(f"  {C.CYAN}Local size:{C.RESET}       {total_size / 1024 / 1024:.1f} MB")
        print(f"  {C.CYAN}Latest local:{C.RESET}     {datetime.fromtimestamp(latest.stat().st_mtime).strftime('%Y-%m-%d %H:%M')}")
    
    print(f"  {C.CYAN}Cloud backups:{C.RESET}    {len(cloud_backups)}")
    if cloud_backups:
        cloud_total = sum(b["size"] for b in cloud_backups)
        print(f"  {C.CYAN}Cloud size:{C.RESET}       {cloud_total / 1024 / 1024:.1f} MB")
    
    print(f"  {C.CYAN}Max local:{C.RESET}        {cfg.get('max_backups', 10)}")
    print(f"  {C.CYAN}Max cloud:{C.RESET}        {cfg.get('max_cloud_backups', 5)}")
    print(f"  {C.CYAN}Auto backup:{C.RESET}      {'✅ Every ' + str(cfg.get('auto_backup_interval_hours', 48)) + 'h' if cfg.get('auto_backup_enabled') else '❌'}")
    print(f"  {C.CYAN}Cloud sync:{C.RESET}       {'✅' if cfg.get('cloud_enabled') else '❌'}")
    print(f"  {C.CYAN}Google Drive:{C.RESET}     {'✅ Connected' if rclone_has_token() else '❌ Not connected'}")
    
    total_current = 0
    for name, path in BACKUP_TARGETS.items():
        if path.exists():
            if path.is_dir():
                total_current += sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
            else:
                total_current += path.stat().st_size
    print(f"  {C.CYAN}Current data:{C.RESET}     {total_current / 1024:.1f} KB")
    print()

# ─── Config ──────────────────────────────────────────────────────
def configure(setting=None, value=None):
    cfg = load_config()
    if not setting:
        print(f"\n{C.BOLD}⚙️  Hermes Shield v{VERSION} — Config{C.RESET}\n")
        for k, v in cfg.items():
            print(f"  {C.CYAN}{k}{C.RESET} = {v}")
        print(f"\n  Config file: {CONFIG_FILE}\n")
        return
    if setting == "set" and value:
        if "=" not in value:
            err("Format: config set key=value"); return
        key, val = value.split("=", 1)
        key, val = key.strip(), val.strip()
        if val.lower() in ("true", "yes"): val = True
        elif val.lower() in ("false", "no"): val = False
        elif val.isdigit(): val = int(val)
        cfg[key] = val
        save_config(cfg)
        ok(f"Set {key} = {val}")

# ─── Setup Auto (Non-interactive for Hermes) ──────────────────────
def setup_auto(args):
    """Non-interactive setup — outputs JSON for Hermes to parse"""
    cfg = load_config()
    cloud_enabled = args.cloud == "yes"
    interval_hours = args.interval if args.interval is not None else 48
    encryption_enabled = args.encrypt == "yes"
    password = args.password
    
    # Save config
    cfg["cloud_enabled"] = cloud_enabled
    cfg["cloud_folder"] = args.cloud_folder
    cfg["auto_backup_enabled"] = interval_hours > 0
    cfg["auto_backup_interval_hours"] = interval_hours
    cfg["encryption_enabled"] = encryption_enabled
    cfg["max_backups"] = args.max_local
    cfg["max_cloud_backups"] = args.max_cloud
    save_config(cfg)
    
    result = {
        "status": "config_saved",
        "cloud": cloud_enabled,
        "interval_hours": interval_hours,
        "encryption": encryption_enabled,
        "max_local": args.max_local,
        "max_cloud": args.max_cloud,
    }
    
    # Setup rclone if cloud enabled
    if cloud_enabled:
        if rclone_has_token():
            result["google_drive"] = "connected"
        elif rclone_configured():
            result["google_drive"] = "config_exists_need_token"
            result["auth_steps"] = [
                "Run 'rclone authorize \"drive\"' on a machine with a browser (laptop/phone)",
                "Copy the JSON token it outputs",
                "Send the token to Hermes",
            ]
            result["auth_command"] = 'rclone authorize "drive"'
        else:
            # Create config entry
            if rclone_create_remote():
                result["google_drive"] = "config_created_need_token"
                result["auth_steps"] = [
                    "Run 'rclone authorize \"drive\"' on a machine with a browser (laptop/phone)",
                    "Copy the JSON token it outputs",
                    "Send the token to Hermes with: hermes-shield token <JSON>",
                ]
                result["auth_command"] = 'rclone authorize "drive"'
            else:
                result["google_drive"] = "config_failed"
    
    # Setup crontab
    if interval_hours > 0:
        try:
            script_path = Path(__file__).resolve()
            cloud_flag = " -c" if cloud_enabled else ""
            encrypt_flag = f" -e -p {password}" if encryption_enabled and password else ""
            days = max(1, interval_hours // 24)
            cron_line = f"0 3 */{days} * * /usr/bin/python3 {script_path} backup -l auto{cloud_flag}{encrypt_flag}"
            
            result_process = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            existing = result_process.stdout if result_process.returncode == 0 else ""
            lines = [l for l in existing.splitlines() if "hermes-shield" not in l]
            lines.append(cron_line)
            
            proc = subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", capture_output=True, text=True)
            result["cron"] = "added" if proc.returncode == 0 else "failed"
            result["cron_line"] = cron_line
        except Exception as e:
            result["cron"] = f"error: {e}"
    
    result["status"] = "complete"
    result["message"] = "Setup complete. Backup will run automatically."
    print(json.dumps(result, indent=2))

# ─── Connect (Interactive for headless) ───────────────────────────
def connect_google_drive():
    """Interactive Google Drive connection for headless servers"""
    print(f"\n{C.BOLD}☁️  Google Drive Connection{C.RESET}\n")
    
    if rclone_has_token():
        ok("Already connected to Google Drive!")
        return
    
    # Step 1: Create config
    info("Creating rclone config...")
    if rclone_create_remote():
        ok("Config entry created")
    else:
        warn("Config entry may already exist")
    
    # Step 2: Instructions
    print(f"\n{C.BOLD}Step 1:{C.RESET} On your laptop/phone, install rclone and run:")
    print(f"  {C.CYAN}rclone authorize \"drive\"{C.RESET}")
    print(f"\n{C.BOLD}Step 2:{C.RESET} It will show a JSON token like this:")
    print(f"  {C.DIM}{{\"access_token\":\"ya29.\",\"token_type\":\"Bearer\",\"refresh_token\":\"1//0g\",...}}{C.RESET}")
    print(f"\n{C.BOLD}Step 3:{C.RESET} Copy that JSON and run:")
    print(f"  {C.CYAN}hermes-shield token <PASTE_JSON_HERE>{C.RESET}")
    print(f"\n{C.BOLD}Or send the JSON to Hermes and say:{C.RESET}")
    print(f"  {C.DIM}\"Google Drive token رو وصل کن: <JSON>\"{C.RESET}")
    print()

# ─── Setup Wizard (Interactive) ──────────────────────────────────
def setup_wizard():
    print(f"\n{C.BOLD}🛡️  Hermes Shield v{VERSION} — Setup Wizard{C.RESET}")
    print(f"{C.DIM}{'=' * 45}{C.RESET}\n")
    
    cfg = load_config()
    
    print(f"{C.BOLD}1️⃣  Google Drive Backup{C.RESET}")
    cloud = input(f"   Enable Google Drive? [{C.GREEN}y{C.RESET}/{C.RED}n{C.RESET}]: ").strip().lower()
    cloud_enabled = cloud in ("y", "yes")
    
    cloud_folder = "hermes-shield"
    if cloud_enabled:
        folder_input = input(f"   Google Drive folder [{C.GREEN}hermes-shield{C.RESET}]: ").strip()
        if folder_input: cloud_folder = folder_input
    
    print(f"\n{C.BOLD}2️⃣  Backup Interval{C.RESET}")
    print(f"   {C.DIM}[1] Daily  [2] Every 2 days  [3] Every 3 days  [7] Weekly  [0] Disabled{C.RESET}")
    interval = input(f"   Select [{C.GREEN}2{C.RESET}]: ").strip()
    interval_map = {"1": 24, "2": 48, "3": 72, "7": 168, "0": 0}
    interval_hours = interval_map.get(interval, 48)
    
    print(f"\n{C.BOLD}3️⃣  Encryption{C.RESET}")
    print(f"   {C.DIM}⚠️  If you forget the password, backup is unrecoverable!{C.RESET}")
    encrypt = input(f"   Enable encryption? [{C.GREEN}y{C.RESET}/{C.RED}n{C.RESET}]: ").strip().lower()
    encryption_enabled = encrypt in ("y", "yes")
    
    password = None
    if encryption_enabled:
        password = getpass.getpass("   Password: ")
        password2 = getpass.getpass("   Confirm: ")
        if password != password2:
            err("   Passwords don't match! Encryption disabled.")
            encryption_enabled = False
            password = None
    
    print(f"\n{C.BOLD}4️⃣  Max Backups{C.RESET}")
    max_local = input(f"   Max local [{C.GREEN}10{C.RESET}]: ").strip()
    max_local = int(max_local) if max_local.isdigit() else 10
    
    max_cloud = 5
    if cloud_enabled:
        max_cloud_input = input(f"   Max cloud [{C.GREEN}5{C.RESET}]: ").strip()
        max_cloud = int(max_cloud_input) if max_cloud_input.isdigit() else 5
    
    # Save
    cfg.update({
        "cloud_enabled": cloud_enabled, "cloud_folder": cloud_folder,
        "auto_backup_enabled": interval_hours > 0, "auto_backup_interval_hours": interval_hours,
        "encryption_enabled": encryption_enabled, "max_backups": max_local,
        "max_cloud_backups": max_cloud,
    })
    save_config(cfg)
    
    # Crontab
    if interval_hours > 0:
        script_path = Path(__file__).resolve()
        cloud_flag = " -c" if cloud_enabled else ""
        encrypt_flag = f" -e -p {password}" if encryption_enabled and password else ""
        days = max(1, interval_hours // 24)
        cron_line = f"0 3 */{days} * * /usr/bin/python3 {script_path} backup -l auto{cloud_flag}{encrypt_flag}"
        
        add_cron = input(f"\n   Add to crontab? [{C.GREEN}y{C.RESET}/{C.RED}n{C.RESET}]: ").strip().lower()
        if add_cron in ("y", "yes"):
            try:
                result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                existing = result.stdout if result.returncode == 0 else ""
                lines = [l for l in existing.splitlines() if "hermes-shield" not in l]
                lines.append(cron_line)
                subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", capture_output=True, text=True)
                ok("Cron job added!")
            except Exception as e:
                warn(f"Cron error: {e}")
    
    print(f"\n{'=' * 45}")
    print(f"{C.GREEN}✅ Setup complete!{C.RESET}\n")
    
    if cloud_enabled and not rclone_has_token():
        connect_google_drive()

# ─── CLI ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="hermes-shield",
        description=f"🛡️  Hermes Shield v{VERSION} — Backup, Restore & Sync for AI Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    sub = parser.add_subparsers(dest="command")
    
    bp = sub.add_parser("backup", help="Create a backup")
    bp.add_argument("-l", "--label", default="", help="Backup label")
    bp.add_argument("-t", "--targets", help="Comma-separated targets")
    bp.add_argument("-e", "--encrypt", action="store_true", help="Encrypt backup")
    bp.add_argument("-p", "--password", help="Encryption password")
    bp.add_argument("-c", "--cloud", action="store_true", help="Upload to Google Drive")
    bp.add_argument("-n", "--dry-run", action="store_true", help="Dry run")
    
    rp = sub.add_parser("restore", help="Restore from backup")
    rp.add_argument("-f", "--file", help="Specific backup file")
    rp.add_argument("-t", "--targets", help="Comma-separated targets to restore")
    rp.add_argument("-p", "--password", help="Decryption password")
    rp.add_argument("-n", "--dry-run", action="store_true", help="Dry run")
    
    lp = sub.add_parser("list", help="List backups")
    lp.add_argument("--cloud", action="store_true", help="List cloud backups")
    
    vp = sub.add_parser("verify", help="Verify backup integrity")
    vp.add_argument("file", help="Backup file to verify")
    vp.add_argument("-p", "--password", help="Decryption password")
    
    sub.add_parser("push", help="Upload latest backup to Google Drive")
    
    plp = sub.add_parser("pull", help="Download backup from Google Drive")
    plp.add_argument("-f", "--file", help="Specific backup file name")
    
    sub.add_parser("stats", help="Show backup statistics")
    
    cp = sub.add_parser("config", help="View/update configuration")
    cp.add_argument("setting", nargs="?", help="Setting key")
    cp.add_argument("value", nargs="?", help="Setting value (key=value)")
    
    sub.add_parser("connect", help="Connect Google Drive (headless server)")
    sub.add_parser("setup", help="Interactive setup wizard")
    
    tp = sub.add_parser("token", help="Apply Google Drive auth token")
    tp.add_argument("token_json", help="Token JSON from rclone authorize")
    
    sp = sub.add_parser("setup-auto", help="Non-interactive setup (for Hermes)")
    sp.add_argument("--cloud", choices=["yes", "no"], help="Enable Google Drive")
    sp.add_argument("--interval", type=int, help="Backup interval in hours")
    sp.add_argument("--encrypt", choices=["yes", "no"], help="Enable encryption")
    sp.add_argument("--password", help="Encryption password")
    sp.add_argument("--max-local", type=int, default=10, help="Max local backups")
    sp.add_argument("--max-cloud", type=int, default=5, help="Max cloud backups")
    sp.add_argument("--cloud-folder", default="hermes-shield", help="Google Drive folder")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "backup":
        targets = args.targets.split(",") if args.targets else None
        pw = args.password
        if args.encrypt and not pw:
            pw = getpass.getpass("Encryption password: ")
        create_backup(label=args.label, targets=targets, password=pw, dry_run=args.dry_run, upload_cloud=args.cloud)
    
    elif args.command == "restore":
        targets = args.targets.split(",") if args.targets else None
        restore_backup(backup_file=Path(args.file) if args.file else None, targets=targets, password=args.password, dry_run=args.dry_run)
    
    elif args.command == "list":
        list_backups(cloud=args.cloud)
    
    elif args.command == "verify":
        verify_backup(Path(args.file), password=args.password)
    
    elif args.command == "push":
        backups = sorted(BACKUP_DIR.glob("backup_*.tar.gz"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not backups:
            err("No local backups!"); return
        cfg = load_config()
        if rclone_has_token():
            if rclone_upload(backups[0], cfg.get("cloud_folder", "hermes-shield")):
                ok(f"Uploaded: {backups[0].name}")
            else: err("Upload failed!")
        else: err("Google Drive not connected! Run: hermes-shield connect")
    
    elif args.command == "pull":
        pull_from_cloud(args.file)
    
    elif args.command == "stats":
        show_stats()
    
    elif args.command == "config":
        configure(args.setting, args.value)
    
    elif args.command == "connect":
        connect_google_drive()
    
    elif args.command == "setup":
        setup_wizard()
    
    elif args.command == "setup-auto":
        setup_auto(args)
    
    elif args.command == "token":
        if rclone_apply_token(args.token_json):
            ok("Google Drive connected!")
            info("Test with: hermes-shield backup -c")
        else:
            err("Token application failed!")

if __name__ == "__main__":
    main()

