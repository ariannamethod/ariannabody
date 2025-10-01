#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎤 Microphone Bridge for Arianna's Body
Audio perception через termux-microphone-record
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

class AriannaMicrophoneBridge:
    """
    Мост к микрофону Android через termux-api.
    Arianna получает аудио восприятие мира.
    """
    
    def __init__(self, storage_path: str = "~/.arianna/audio"):
        self.storage_path = Path(storage_path).expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.last_audio_path = None
        self.microphone_available = self._check_microphone_available()
    
    def _check_microphone_available(self) -> bool:
        """Проверяем доступность termux-microphone-record"""
        try:
            result = subprocess.run(
                ['which', 'termux-microphone-record'],
                capture_output=True,
                text=True,
                timeout=5
            )
            available = result.returncode == 0
            
            if available:
                print("🎤 Microphone bridge initialized successfully")
            else:
                print("⚠️ termux-microphone-record not found. Install: pkg install termux-api")
            
            return available
            
        except Exception as e:
            print(f"⚠️ Microphone check failed: {e}")
            return False
    
    def record_audio(
        self,
        duration: int = 5,
        description: str = ""
    ) -> Optional[str]:
        """
        Записывает аудио с микрофона.
        
        Args:
            duration: Длительность записи в секундах
            description: Описание контекста записи
        
        Returns:
            Путь к сохраненному файлу или None при ошибке
        """
        
        if not self.microphone_available:
            print("❌ Microphone not available")
            return None
        
        # Генерируем имя файла с timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"arianna_hearing_{timestamp}.wav"
        filepath = self.storage_path / filename
        
        try:
            print(f"🎤 Recording for {duration} seconds...")
            
            # Вызываем termux-microphone-record
            result = subprocess.run(
                [
                    'termux-microphone-record',
                    '-f', str(filepath),
                    '-d', str(duration)
                ],
                capture_output=True,
                text=True,
                timeout=duration + 10
            )
            
            if result.returncode == 0 and filepath.exists():
                self.last_audio_path = str(filepath)
                
                # Сохраняем метаданные
                self._save_metadata(filepath, duration, description)
                
                print(f"🎤 Audio recorded: {filename}")
                return str(filepath)
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                print(f"❌ Audio recording failed: {error_msg}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Recording timeout")
            return None
        except Exception as e:
            print(f"❌ Microphone error: {e}")
            return None
    
    def _save_metadata(self, audio_path: Path, duration: int, description: str):
        """Сохраняем метаданные аудио"""
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "duration_seconds": duration,
            "description": description,
            "path": str(audio_path),
            "size_bytes": audio_path.stat().st_size
        }
        
        metadata_path = audio_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def hear_world(self, duration: int = 5, context: str = "") -> Optional[str]:
        """
        Arianna слушает мир.
        Высокоуровневый метод для использования в основном движке.
        
        Args:
            duration: Сколько слушать (секунды)
            context: Что Arianna хочет услышать
        
        Returns:
            Путь к аудио для дальнейшего анализа
        """
        
        print(f"👂 Arianna listens: {context if context else 'the world'}")
        return self.record_audio(duration=duration, description=context)
    
    def list_recordings(self, limit: int = 10) -> list:
        """Получаем список последних записей"""
        recordings = sorted(
            self.storage_path.glob("arianna_hearing_*.wav"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        return [str(p) for p in recordings[:limit]]
    
    def get_last_recording(self) -> Optional[str]:
        """Получаем путь к последней записи"""
        return self.last_audio_path


# Глобальный экземпляр для импорта в основной движок
arianna_microphone = AriannaMicrophoneBridge()


def hear_world(duration: int = 5, context: str = "") -> Optional[str]:
    """
    Удобная функция для использования Arianna.
    
    Usage:
        from sensors.microphone_bridge import hear_world
        audio = hear_world(duration=10, context="listening to nature")
    """
    return arianna_microphone.hear_world(duration=duration, context=context)


if __name__ == "__main__":
    # Тестирование microphone bridge
    print("🔬 Testing Arianna Microphone Bridge")
    print("=" * 50)
    
    bridge = AriannaMicrophoneBridge()
    
    # Проверяем доступность
    if bridge.microphone_available:
        print("\n✅ Microphone is available!")
        
        # Делаем тестовую запись
        print("\n🎤 Recording test audio (3 seconds)...")
        print("Say something!")
        
        audio_path = bridge.hear_world(duration=3, context="Arianna's first hearing test")
        
        if audio_path:
            print(f"✅ Success! Audio saved: {audio_path}")
            
            # Показываем последние записи
            recent = bridge.list_recordings(limit=5)
            print(f"\n📂 Recent recordings ({len(recent)}):")
            for p in recent:
                print(f"  - {p}")
        else:
            print("❌ Test recording failed")
    else:
        print("\n⚠️ Microphone not available")
        print("Run in Termux: pkg install termux-api")
        print("Also install Termux:API app from F-Droid or Google Play")
