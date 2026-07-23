#!/bin/bash
# Hermes Shield — Quick Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/your-username/hermes-shield/main/install.sh | bash

set -e

echo "🛡️  Hermes Shield Installer"
echo "=========================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python $PYTHON_VERSION found"

# Check pip
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip not found. Please install pip"
    exit 1
fi

# Install cryptography
echo "📦 Installing cryptography..."
python3 -m pip install cryptography --quiet 2>/dev/null || python3 -m pip install cryptography
echo "✓ cryptography installed"

# Determine install location
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
INSTALL_DIR="$HERMES_HOME/skills/devops/hermes-shield"

echo ""
echo "📂 Installing to: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR/scripts"

# Download files
REPO_URL="https://raw.githubusercontent.com/your-username/hermes-shield/main"

echo "⬇️  Downloading files..."
curl -fsSL "$REPO_URL/SKILL.md" -o "$INSTALL_DIR/SKILL.md"
curl -fsSL "$REPO_URL/scripts/hermes-shield.py" -o "$INSTALL_DIR/scripts/hermes-shield.py"
chmod +x "$INSTALL_DIR/scripts/hermes-shield.py"

echo "✓ Files installed"

# Test
echo ""
echo "🧪 Testing installation..."
if python3 "$INSTALL_DIR/scripts/hermes-shield.py" stats > /dev/null 2>&1; then
    echo "✓ Installation successful!"
else
    echo "⚠️  Installation complete but test failed. Check manually."
fi

echo ""
echo "🛡️  Hermes Shield is ready!"
echo ""
echo "Usage:"
echo "  python3 $INSTALL_DIR/scripts/hermes-shield.py backup"
echo "  python3 $INSTALL_DIR/scripts/hermes-shield.py list"
echo "  python3 $INSTALL_DIR/scripts/hermes-shield.py stats"
echo ""

