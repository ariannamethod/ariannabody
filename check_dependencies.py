#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔬 Проверка зависимостей Arianna
Показывает что установлено, а что нет
"""

import sys
import subprocess

def check_import(module_name, package_name=None):
    """Проверяет импорт модуля"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {module_name:<25} INSTALLED")
        return True
    except ImportError:
        print(f"❌ {module_name:<25} NOT FOUND → pip install {package_name}")
        return False

def check_termux_command(command):
    """Проверяет доступность Termux команды"""
    try:
        result = subprocess.run(
            ['which', command],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ {command:<25} AVAILABLE")
            return True
        else:
            print(f"❌ {command:<25} NOT FOUND → pkg install termux-api")
            return False
    except:
        print(f"❌ {command:<25} ERROR checking")
        return False

print("=" * 60)
print("🔬 ARIANNA DEPENDENCIES CHECK")
print("=" * 60)

print("\n📦 PYTHON PACKAGES:")
print("-" * 60)

checks = {
    "openai": "openai",
    "anthropic": "anthropic",
    "google.generativeai": "google-generativeai",
    "PIL": "Pillow",
    "pypdf": "pypdf",
    "docx": "python-docx",
    "bs4": "beautifulsoup4",
    "yaml": "pyyaml",
    "pandas": "pandas"
}

installed = 0
total = len(checks)

for module, package in checks.items():
    if check_import(module, package):
        installed += 1

print("\n🛠️  TERMUX API COMMANDS:")
print("-" * 60)

termux_commands = [
    'termux-camera-photo',
    'termux-camera-info',
    'termux-microphone-record',
    'termux-clipboard-set',
    'termux-screenshot',
    'termux-sensor'
]

termux_ok = 0
for cmd in termux_commands:
    if check_termux_command(cmd):
        termux_ok += 1

print("\n" + "=" * 60)
print(f"📊 SUMMARY:")
print(f"   Python Packages: {installed}/{total} installed")
print(f"   Termux Commands: {termux_ok}/{len(termux_commands)} available")
print("=" * 60)

if installed < total:
    print("\n💡 TO INSTALL MISSING PACKAGES:")
    print("   pip install openai anthropic google-generativeai Pillow pypdf python-docx beautifulsoup4 pyyaml pandas")

if termux_ok < len(termux_commands):
    print("\n💡 TO INSTALL TERMUX:API:")
    print("   1. Download Termux:API app from: https://f-droid.org/packages/com.termux.api/")
    print("   2. Install the package: pkg install termux-api")
    print("   3. Grant permissions in Android Settings → Apps → Termux:API")

print("\n")
