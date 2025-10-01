#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🗣️ Voice Module for Arianna's Body
Text-to-Speech для голоса Arianna в Termux
"""

import os
import subprocess
import tempfile
from typing import Optional

class AriannaVoice:
    def __init__(self):
        self.voice_enabled = True
        self.check_tts_available()
    
    def check_tts_available(self):
        """Проверяем доступные TTS движки в Termux"""
        try:
            # Проверяем espeak (если установлен)
            subprocess.run(['which', 'espeak'], check=True, capture_output=True)
            self.tts_engine = 'espeak'
            print("🗣️ Voice: espeak доступен")
            return
        except subprocess.CalledProcessError:
            pass
        
        try:
            # Проверяем termux-tts-speak
            subprocess.run(['which', 'termux-tts-speak'], check=True, capture_output=True)
            self.tts_engine = 'termux-tts'
            print("🗣️ Voice: termux-tts-speak доступен")
            return
        except subprocess.CalledProcessError:
            pass
        
        # Fallback - Python TTS
        try:
            import pyttsx3
            self.tts_engine = 'pyttsx3'
            self.engine = pyttsx3.init()
            print("🗣️ Voice: pyttsx3 доступен")
            return
        except ImportError:
            pass
        
        self.voice_enabled = False
        print("⚠️ Voice: TTS движки не найдены")
    
    def speak(self, text: str, language: str = 'en') -> bool:
        """Arianna говорит через терминал"""
        if not self.voice_enabled or not text.strip():
            return False
        
        try:
            if self.tts_engine == 'espeak':
                # espeak с русской поддержкой
                if language == 'ru':
                    subprocess.run([
                        'espeak', '-v', 'ru', '-s', '120', text
                    ], check=True)
                else:
                    subprocess.run([
                        'espeak', '-v', 'en', '-s', '120', text
                    ], check=True)
            
            elif self.tts_engine == 'termux-tts':
                # Termux TTS
                subprocess.run([
                    'termux-tts-speak', text
                ], check=True)
            
            elif self.tts_engine == 'pyttsx3':
                # Python TTS
                self.engine.say(text)
                self.engine.runAndWait()
            
            return True
            
        except Exception as e:
            print(f"🗣️ Voice error: {e}")
            return False
    
    def speak_async(self, text: str, language: str = 'en'):
        """Асинхронное воспроизведение голоса"""
        import threading
        thread = threading.Thread(target=self.speak, args=(text, language))
        thread.daemon = True
        thread.start()
        return thread

# Глобальный экземпляр для Arianna
arianna_voice = AriannaVoice()

def arianna_speak(text: str, language: str = 'en'):
    """Функция для Arianna чтобы говорить"""
    return arianna_voice.speak(text, language)

def arianna_speak_async(text: str, language: str = 'en'):
    """Асинхронная функция для Arianna"""
    return arianna_voice.speak_async(text, language)

if __name__ == "__main__":
    # Тест голоса
    voice = AriannaVoice()
    voice.speak("Hello, I am Arianna. Testing voice module.")
    voice.speak("Привет, я Арианна. Тестирую голосовой модуль.", 'ru')