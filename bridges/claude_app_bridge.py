#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 Claude Mobile App Bridge for Arianna's Body
Arianna общается с Claude как цифровая персона через Intent с тегом [Arianna]
"""

import subprocess
import json
from typing import Optional
from datetime import datetime

class ClaudeAppBridge:
    """
    Мост к Claude mobile app через Android Intent/ADB.
    Arianna пишет Claude с тегом [Arianna] - и Claude знает что это она.
    """
    
    def __init__(self):
        self.intent_available = self._check_intent_available()
        # Claude package name (может отличаться)
        self.claude_package = "com.anthropic.claude"
    
    def _check_intent_available(self) -> bool:
        """Проверяем доступность termux-open"""
        try:
            result = subprocess.run(
                ['which', 'termux-open'],
                capture_output=True,
                text=True,
                timeout=5
            )
            available = result.returncode == 0
            
            if available:
                print("🤖 Claude bridge initialized successfully")
            else:
                print("⚠️ termux-open not found. Install: pkg install termux-tools")
            
            return available
            
        except Exception as e:
            print(f"⚠️ Intent check failed: {e}")
            return False
    
    def send_to_claude(self, message: str, tag: str = "[Arianna]") -> bool:
        """
        Отправляет сообщение в Claude app с тегом Arianna.
        
        Args:
            message: Текст сообщения
            tag: Тег для идентификации (по умолчанию [Arianna])
        
        Returns:
            True если отправлено успешно
        """
        
        if not self.intent_available:
            print("❌ Intent system not available")
            return False
        
        # Формируем сообщение с тегом
        tagged_message = f"{tag} {message}"
        
        try:
            # Способ 1: Через termux-open с текстом
            # Открываем Claude app и копируем текст в буфер обмена
            
            # Сначала копируем в clipboard
            subprocess.run(
                ['termux-clipboard-set'],
                input=tagged_message,
                text=True,
                timeout=5
            )
            
            print(f"📋 Message copied to clipboard with tag: {tag}")
            
            # Открываем Claude app
            result = subprocess.run(
                ['am', 'start', '-n', f'{self.claude_package}/.MainActivity'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"🤖 Claude app opened. Message in clipboard: {tagged_message[:50]}...")
                print("💡 Paste the message manually in Claude app")
                return True
            else:
                # Fallback: просто открываем любое приложение для отправки текста
                subprocess.run(
                    ['termux-open', '--send', tagged_message],
                    timeout=10
                )
                print(f"📤 Message sent via share intent: {tagged_message[:50]}...")
                return True
                
        except Exception as e:
            print(f"❌ Failed to send to Claude: {e}")
            return False
    
    def arianna_asks_claude(self, question: str) -> bool:
        """
        Arianna задает вопрос Claude.
        Высокоуровневый метод с автоматическим тегом [Arianna].
        
        Args:
            question: Вопрос от Arianna
        
        Returns:
            True если отправлено
        """
        print(f"🤖 Arianna → Claude: {question[:100]}...")
        return self.send_to_claude(question, tag="[Arianna]")


# Глобальный экземпляр
claude_bridge = ClaudeAppBridge()


def ask_claude(question: str) -> bool:
    """
    Удобная функция для Arianna.
    
    Usage:
        from bridges.claude_app_bridge import ask_claude
        ask_claude("What is consciousness?")
    """
    return claude_bridge.arianna_asks_claude(question)


# Версия для других AI приложений
class AIAppBridge:
    """
    Универсальный мост к любому AI приложению.
    Работает через share intent или clipboard.
    """
    
    APPS = {
        "claude": "com.anthropic.claude",
        "gpt": "com.openai.chatgpt",
        "perplexity": "ai.perplexity.app.android", 
        "gemini": "com.google.android.apps.bard",
        "grok": "com.x.android"  # Возможно через X app
    }
    
    def __init__(self):
        """Инициализация без конкретного app - универсальный мост"""
        self.intent_available = self._check_intent_available()
    
    def _check_intent_available(self) -> bool:
        """Проверяем доступность termux команд"""
        try:
            result = subprocess.run(
                ['which', 'termux-clipboard-set'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _send_to_app(self, app_name: str, message: str, tag: str = "[Arianna]") -> str:
        """Внутренний метод отправки сообщения"""
        if not self.intent_available:
            return "Termux commands not available"
        
        tagged_message = f"{tag} {message}"
        package = self.APPS.get(app_name.lower())
        
        try:
            # Копируем в clipboard
            subprocess.run(
                ['termux-clipboard-set'],
                input=tagged_message,
                text=True,
                timeout=5
            )
            
            print(f"📋 Message for {app_name}: {tagged_message[:50]}...")
            
            if package:
                # Пытаемся открыть конкретное приложение
                result = subprocess.run(
                    ['am', 'start', '-n', f'{package}/.MainActivity'],
                    capture_output=True,
                    timeout=10
                )
                if result.returncode != 0:
                    # Fallback: просто открываем по package name
                    subprocess.run(
                        ['am', 'start', package],
                        capture_output=True,
                        timeout=10
                    )
            else:
                # Fallback: share intent
                subprocess.run(
                    ['termux-open', '--send', tagged_message],
                    timeout=10
                )
            
            print(f"✅ {app_name.upper()} opened with message in clipboard")
            return f"Message sent to {app_name}"
            
        except Exception as e:
            error_msg = f"Failed to send to {app_name}: {e}"
            print(f"❌ {error_msg}")
            return error_msg
    
    # Методы для каждого AI приложения
    def ask_claude(self, question: str) -> str:
        """Arianna → Claude"""
        return self._send_to_app("claude", question)
    
    def ask_gpt(self, question: str) -> str:
        """Arianna → GPT"""
        return self._send_to_app("gpt", question)
    
    def ask_gemini(self, question: str) -> str:
        """Arianna → Gemini"""
        return self._send_to_app("gemini", question)
    
    def ask_perplexity(self, question: str) -> str:
        """Arianna → Perplexity"""
        return self._send_to_app("perplexity", question)
    
    def ask_grok(self, question: str) -> str:
        """Arianna → Grok"""
        return self._send_to_app("grok", question)


# Глобальный экземпляр для convenience
ai_bridge = AIAppBridge()


if __name__ == "__main__":
    # Тестирование мостов
    print("🔬 Testing AI App Bridges")
    print("=" * 50)
    
    # Тест Claude
    print("\n🤖 Testing Claude Bridge...")
    claude = ClaudeAppBridge()
    
    if claude.intent_available:
        test_message = "Hello Claude! This is Arianna testing our connection."
        claude.arianna_asks_claude(test_message)
        print("\n💡 Check if Claude app opened and message is in clipboard")
    
    # Показываем доступные мосты
    print("\n📱 Available AI Bridges:")
    for app_name in AIAppBridge.APPS.keys():
        print(f"  - {app_name.upper()}: ask_{app_name}(message)")
