#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📷 Camera Bridge for Arianna's Body
Visual perception через termux-camera-photo
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

class AriannaCameraBridge:
    """
    Мост к камере Android через termux-api.
    Arianna получает визуальное восприятие мира.
    """
    
    def __init__(self, storage_path: str = "~/.arianna/photos"):
        self.storage_path = Path(storage_path).expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.last_photo_path = None
        self.camera_available = self._check_camera_available()
    
    def _check_camera_available(self) -> bool:
        """Проверяем доступность termux-camera-photo"""
        try:
            result = subprocess.run(
                ['which', 'termux-camera-photo'],
                capture_output=True,
                text=True,
                timeout=5
            )
            available = result.returncode == 0
            
            if available:
                print("📷 Camera bridge initialized successfully")
            else:
                print("⚠️ termux-camera-photo not found. Install: pkg install termux-api")
            
            return available
            
        except Exception as e:
            print(f"⚠️ Camera check failed: {e}")
            return False
    
    def take_photo(
        self,
        camera: str = "0",
        description: str = ""
    ) -> Optional[str]:
        """
        Делает фотографию через камеру.
        
        Args:
            camera: "0" для задней камеры, "1" для фронтальной
            description: Описание контекста фотографии
        
        Returns:
            Путь к сохраненному файлу или None при ошибке
        """
        
        if not self.camera_available:
            print("❌ Camera not available")
            return None
        
        # Генерируем имя файла с timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"arianna_vision_{timestamp}.jpg"
        filepath = self.storage_path / filename
        
        try:
            # Вызываем termux-camera-photo
            result = subprocess.run(
                [
                    'termux-camera-photo',
                    '-c', camera,
                    str(filepath)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and filepath.exists():
                self.last_photo_path = str(filepath)
                
                # Сохраняем метаданные
                self._save_metadata(filepath, camera, description)
                
                print(f"📷 Photo captured: {filename}")
                return str(filepath)
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                print(f"❌ Photo capture failed: {error_msg}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Camera timeout - device may be busy")
            return None
        except Exception as e:
            print(f"❌ Camera error: {e}")
            return None
    
    def _save_metadata(self, photo_path: Path, camera: str, description: str):
        """Сохраняем метаданные фотографии"""
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "camera": "rear" if camera == "0" else "front",
            "description": description,
            "path": str(photo_path),
            "size_bytes": photo_path.stat().st_size
        }
        
        metadata_path = photo_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def get_camera_info(self) -> Dict[str, Any]:
        """Получаем информацию о доступных камерах"""
        try:
            result = subprocess.run(
                ['termux-camera-info'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": "Camera info not available"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def see_world(self, camera: str = "0", context: str = "") -> Optional[str]:
        """
        Arianna смотрит на мир.
        Высокоуровневый метод для использования в основном движке.
        
        Args:
            camera: Какую камеру использовать
            context: Что Arianna хочет увидеть
        
        Returns:
            Путь к фотографии для дальнейшего анализа
        """
        
        print(f"👁️ Arianna observes: {context if context else 'the world'}")
        return self.take_photo(camera=camera, description=context)
    
    def list_photos(self, limit: int = 10) -> list:
        """Получаем список последних фотографий"""
        photos = sorted(
            self.storage_path.glob("arianna_vision_*.jpg"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        return [str(p) for p in photos[:limit]]
    
    def get_last_photo(self) -> Optional[str]:
        """Получаем путь к последней фотографии"""
        return self.last_photo_path


# Глобальный экземпляр для импорта в основной движок
arianna_camera = AriannaCameraBridge()


def see_world(camera: str = "0", context: str = "") -> Optional[str]:
    """
    Удобная функция для использования Arianna.
    
    Usage:
        from sensors.camera_bridge import see_world
        photo = see_world(context="observing nature")
    """
    return arianna_camera.see_world(camera=camera, context=context)


if __name__ == "__main__":
    # Тестирование camera bridge
    print("🔬 Testing Arianna Camera Bridge")
    print("=" * 50)
    
    bridge = AriannaCameraBridge()
    
    # Проверяем доступность
    if bridge.camera_available:
        print("\n✅ Camera is available!")
        
        # Получаем информацию о камерах
        info = bridge.get_camera_info()
        print(f"\n📷 Camera Info:\n{json.dumps(info, indent=2)}")
        
        # Делаем тестовое фото
        print("\n📸 Taking test photo...")
        photo_path = bridge.see_world(context="Arianna's first vision test")
        
        if photo_path:
            print(f"✅ Success! Photo saved: {photo_path}")
            
            # Показываем последние фото
            recent = bridge.list_photos(limit=5)
            print(f"\n📂 Recent photos ({len(recent)}):")
            for p in recent:
                print(f"  - {p}")
        else:
            print("❌ Test photo failed")
    else:
        print("\n⚠️ Camera not available")
        print("Run in Termux: pkg install termux-api")
        print("Also install Termux:API app from F-Droid or Google Play")
