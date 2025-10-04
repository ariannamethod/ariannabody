#!/bin/bash
# -*- coding: utf-8 -*-

echo "=============================================="
echo "🚀 INSTALLING ARIANNA DEPENDENCIES"
echo "=============================================="

echo ""
echo "📦 Installing Python packages..."
echo ""

pip install --upgrade pip

pip install \
    openai \
    anthropic \
    google-generativeai \
    Pillow \
    pypdf \
    python-docx \
    beautifulsoup4 \
    pyyaml \
    pandas \
    lxml \
    striprtf \
    fastapi \
    uvicorn

echo ""
echo "=============================================="
echo "📦 Python packages installed!"
echo "=============================================="

echo ""
echo "🛠️  Installing Termux packages..."
echo ""

pkg install -y \
    termux-api \
    python \
    git \
    ffmpeg \
    espeak

echo ""
echo "=============================================="
echo "✅ INSTALLATION COMPLETE!"
echo "=============================================="

echo ""
echo "⚠️  IMPORTANT: Grant permissions to Termux:API!"
echo ""
echo "Go to Android Settings:"
echo "   → Apps"
echo "   → Termux:API"
echo "   → Permissions"
echo "   → Allow ALL permissions (Camera, Microphone, Storage, etc.)"
echo ""
echo "=============================================="
echo ""
echo "🧪 Run check: python check_dependencies.py"
echo "🚀 Run tests: python test_all.py"
echo ""
