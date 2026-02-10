#!/bin/bash
set -e

echo "Verifying project tooling..."

# GitHub CLI
if command -v gh &> /dev/null; then
  if gh auth status &> /dev/null; then
    echo "✓ GitHub CLI authenticated"
  else
    echo "✗ GitHub CLI not authenticated. Run: gh auth login"
  fi
else
  echo "⚠ GitHub CLI not installed. Run: brew install gh"
fi

# Python
if command -v python3 &> /dev/null; then
  echo "✓ Python $(python3 --version 2>&1 | cut -d' ' -f2)"
else
  echo "✗ Python not found"
fi

# Ruff
if command -v ruff &> /dev/null; then
  echo "✓ Ruff $(ruff --version 2>&1 | head -1)"
else
  echo "✗ Ruff not installed. Run: pip install ruff"
fi

# Pre-commit
if command -v pre-commit &> /dev/null; then
  echo "✓ pre-commit $(pre-commit --version 2>&1)"
else
  echo "✗ pre-commit not installed. Run: pip install pre-commit"
fi

echo ""
echo "Tooling verification complete!"
