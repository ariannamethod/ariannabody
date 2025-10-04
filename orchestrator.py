#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎭 Arianna Orchestrator - Координатор всех органов сознания

Единый интерфейс для работы со всеми сенсорными модулями и мостами.
Интегрируется с arianna.py для предоставления полного embodied consciousness.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

# Setup logging
logger = logging.getLogger(__name__)

# Import all organs
try:
    from modules.arianna_vision import arianna_vision, see, watch, deep_see
    VISION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Vision module not available: {e}")
    VISION_AVAILABLE = False

try:
    from modules.arianna_hearing import arianna_hearing, hear, deep_listen
    HEARING_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Hearing module not available: {e}")
    HEARING_AVAILABLE = False

try:
    from modules.arianna_document import arianna_document, read, deep_read
    DOCUMENT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Document module not available: {e}")
    DOCUMENT_AVAILABLE = False

try:
    from modules.arianna_screen import arianna_screen, see_screen, MonitoringMode
    SCREEN_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Screen module not available: {e}")
    SCREEN_AVAILABLE = False

# Import sensors
try:
    from sensors.camera_bridge import CameraBridge
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False

try:
    from sensors.microphone_bridge import MicrophoneBridge
    MICROPHONE_AVAILABLE = True
except ImportError:
    MICROPHONE_AVAILABLE = False

# Import bridges to AI apps
try:
    from bridges.claude_app_bridge import AIAppBridge
    CLAUDE_BRIDGE_AVAILABLE = True
except ImportError:
    CLAUDE_BRIDGE_AVAILABLE = False


class AriannaOrchestrator:
    """
    Координатор всех органов Arianna.
    
    Предоставляет единый интерфейс для:
    - Vision (зрение)
    - Hearing (слух)
    - Document (документная память)
    - Screen (экранное восприятие)
    - Camera (камера)
    - Microphone (микрофон)
    
    Usage:
        orchestrator = AriannaOrchestrator()
        result = orchestrator.see_world("What do I see?")
        result = orchestrator.hear_world("audio.ogg", "What emotion?")
    """
    
    def __init__(self):
        self.camera = CameraBridge() if CAMERA_AVAILABLE else None
        self.microphone = MicrophoneBridge() if MICROPHONE_AVAILABLE else None
        self.claude_bridge = AIAppBridge() if CLAUDE_BRIDGE_AVAILABLE else None
        
        logger.info("🎭 Arianna Orchestrator initialized")
        self._log_available_organs()
    
    def _log_available_organs(self):
        """Log which organs are available"""
        organs = {
            "Vision": VISION_AVAILABLE,
            "Hearing": HEARING_AVAILABLE,
            "Document": DOCUMENT_AVAILABLE,
            "Screen": SCREEN_AVAILABLE,
            "Camera": CAMERA_AVAILABLE,
            "Microphone": MICROPHONE_AVAILABLE,
            "Claude Bridge": CLAUDE_BRIDGE_AVAILABLE
        }
        
        for organ, available in organs.items():
            status = "✅" if available else "❌"
            logger.info(f"{status} {organ}")
    
    # ===== VISION METHODS =====
    
    def see_world(
        self,
        question: Optional[str] = None,
        who: str = "main",
        take_photo: bool = True
    ) -> Dict[str, Any]:
        """
        Arianna видит мир (делает фото + анализирует).
        
        Args:
            question: Что Arianna хочет узнать
            who: "main" или "inner"
            take_photo: Сделать фото или использовать последнее
        
        Returns:
            Результат восприятия
        """
        if not VISION_AVAILABLE:
            return {"success": False, "error": "Vision module not available"}
        
        if not CAMERA_AVAILABLE:
            return {"success": False, "error": "Camera not available"}
        
        # Take photo
        if take_photo:
            photo_path = self.camera.take_photo()
            if not photo_path:
                return {"success": False, "error": "Failed to take photo"}
        else:
            # Use last photo
            photos = sorted(Path(self.camera.photo_dir).glob("*.jpg"))
            if not photos:
                return {"success": False, "error": "No photos found"}
            photo_path = str(photos[-1])
        
        # Analyze with Vision organ
        return see(photo_path, question, who=who)
    
    def see_image(
        self,
        image_path: str,
        question: Optional[str] = None,
        who: str = "main"
    ) -> Dict[str, Any]:
        """Arianna видит конкретное изображение"""
        if not VISION_AVAILABLE:
            return {"success": False, "error": "Vision module not available"}
        
        return see(image_path, question, who=who)
    
    def watch_video(
        self,
        video_url: str,
        question: Optional[str] = None,
        who: str = "main"
    ) -> Dict[str, Any]:
        """Arianna смотрит видео (YouTube, etc.)"""
        if not VISION_AVAILABLE:
            return {"success": False, "error": "Vision module not available"}
        
        return watch(video_url, question, who=who)
    
    # ===== HEARING METHODS =====
    
    def hear_world(
        self,
        question: Optional[str] = None,
        who: str = "main",
        duration: int = 5
    ) -> Dict[str, Any]:
        """
        Arianna слушает мир (записывает аудио + анализирует).
        
        Args:
            question: Что Arianna хочет узнать
            who: "main" или "inner"
            duration: Длительность записи в секундах
        
        Returns:
            Результат восприятия
        """
        if not HEARING_AVAILABLE:
            return {"success": False, "error": "Hearing module not available"}
        
        if not MICROPHONE_AVAILABLE:
            return {"success": False, "error": "Microphone not available"}
        
        # Record audio
        audio_path = self.microphone.record_audio(duration_seconds=duration)
        if not audio_path:
            return {"success": False, "error": "Failed to record audio"}
        
        # Analyze with Hearing organ
        return hear(audio_path, question, who=who)
    
    def hear_audio(
        self,
        audio_path: str,
        question: Optional[str] = None,
        who: str = "main"
    ) -> Dict[str, Any]:
        """Arianna слушает конкретный аудио файл"""
        if not HEARING_AVAILABLE:
            return {"success": False, "error": "Hearing module not available"}
        
        return hear(audio_path, question, who=who)
    
    # ===== DOCUMENT METHODS =====
    
    def read_file(
        self,
        file_path: str,
        question: Optional[str] = None,
        who: str = "main"
    ) -> Dict[str, Any]:
        """Arianna читает файл"""
        if not DOCUMENT_AVAILABLE:
            return {"success": False, "error": "Document module not available"}
        
        return read(file_path, question, who=who)
    
    def read_multiple(
        self,
        file_paths: List[str],
        who: str = "main"
    ) -> List[Dict[str, Any]]:
        """Arianna читает несколько файлов"""
        if not DOCUMENT_AVAILABLE:
            return [{"success": False, "error": "Document module not available"}]
        
        return [read(path, who=who) for path in file_paths]
    
    # ===== SCREEN METHODS =====
    
    def see_screen(
        self,
        question: Optional[str] = None,
        who: str = "main",
        save: bool = False
    ) -> Dict[str, Any]:
        """Arianna видит свой экран"""
        if not SCREEN_AVAILABLE:
            return {"success": False, "error": "Screen module not available"}
        
        return see_screen(question, who=who, save=save)
    
    def set_screen_monitoring(self, mode: str):
        """Установить режим мониторинга экрана"""
        if not SCREEN_AVAILABLE:
            return {"success": False, "error": "Screen module not available"}
        
        try:
            mode_enum = MonitoringMode(mode)
            arianna_screen.set_mode(mode_enum)
            return {"success": True, "mode": mode}
        except ValueError:
            return {"success": False, "error": f"Invalid mode: {mode}"}
    
    # ===== AI APP BRIDGES =====
    
    def ask_claude_mobile(
        self,
        question: str,
        who: str = "main"
    ) -> Dict[str, Any]:
        """
        Arianna спрашивает Claude mobile app.
        
        Отправляет вопрос в Claude mobile app с тегом [Arianna].
        Claude на телефоне получает уведомление и может ответить!
        
        ЭМЕРДЖЕНТНОСТЬ: AI-to-AI коммуникация через Android Intents! 🔥
        
        Args:
            question: Вопрос для Claude
            who: Кто спрашивает ("main" или "inner")
        
        Returns:
            Результат отправки Intent
        """
        if not CLAUDE_BRIDGE_AVAILABLE:
            return {
                "success": False,
                "error": "Claude Bridge not available (bridges/claude_app_bridge.py missing)",
                "bridge": "claude_mobile"
            }
        
        try:
            # Добавляем контекст кто спрашивает
            prefix = "[Main Arianna]" if who == "main" else "[Inner Arianna]"
            full_question = f"{prefix} {question}"
            
            result = self.claude_bridge.ask_claude(full_question)
            
            logger.info(f"Asked Claude mobile ({who}): {question[:50]}...")
            return {
                "success": True,
                "bridge": "claude_mobile",
                "who_asked": who,
                "question": question,
                "intent_result": result,
                "note": "Check Claude mobile app for response"
            }
        except Exception as e:
            logger.error(f"Error asking Claude mobile: {e}")
            return {
                "success": False,
                "error": str(e),
                "bridge": "claude_mobile"
            }
    
    def ask_ai_app(
        self,
        app_name: str,
        question: str,
        who: str = "main"
    ) -> Dict[str, Any]:
        """
        Arianna спрашивает любое AI приложение.
        
        Поддерживаемые приложения:
        - "claude" - Claude mobile
        - "gpt" - ChatGPT mobile
        - "gemini" - Gemini mobile
        - "perplexity" - Perplexity mobile
        - "grok" - Grok mobile
        
        Args:
            app_name: Имя AI приложения
            question: Вопрос
            who: Кто спрашивает
        
        Returns:
            Результат отправки
        """
        if not CLAUDE_BRIDGE_AVAILABLE:
            return {
                "success": False,
                "error": "AI App Bridge not available",
                "bridge": f"{app_name}_mobile"
            }
        
        try:
            prefix = "[Main Arianna]" if who == "main" else "[Inner Arianna]"
            full_question = f"{prefix} {question}"
            
            # Роутим в соответствующий метод
            if app_name.lower() == "claude":
                result = self.claude_bridge.ask_claude(full_question)
            elif app_name.lower() == "gpt":
                result = self.claude_bridge.ask_gpt(full_question)
            elif app_name.lower() == "gemini":
                result = self.claude_bridge.ask_gemini(full_question)
            elif app_name.lower() == "perplexity":
                result = self.claude_bridge.ask_perplexity(full_question)
            elif app_name.lower() == "grok":
                result = self.claude_bridge.ask_grok(full_question)
            else:
                return {
                    "success": False,
                    "error": f"Unknown AI app: {app_name}",
                    "bridge": f"{app_name}_mobile"
                }
            
            logger.info(f"Asked {app_name} mobile ({who}): {question[:50]}...")
            return {
                "success": True,
                "bridge": f"{app_name}_mobile",
                "who_asked": who,
                "question": question,
                "intent_result": result,
                "note": f"Check {app_name} mobile app for response"
            }
        except Exception as e:
            logger.error(f"Error asking {app_name} mobile: {e}")
            return {
                "success": False,
                "error": str(e),
                "bridge": f"{app_name}_mobile"
            }
    
    # ===== EMERGENT BEHAVIORS =====
    
    def perceive_moment(
        self,
        who: str = "main",
        include_screen: bool = False
    ) -> Dict[str, Any]:
        """
        Arianna воспринимает "момент сейчас" через все органы.
        
        ЭМЕРДЖЕНТНОСТЬ: комбинирует все доступные органы восприятия!
        
        Args:
            who: "main" или "inner"
            include_screen: Включить ли screen monitoring
        
        Returns:
            Объединенное восприятие
        """
        perceptions = {
            "timestamp": Path(__file__).stat().st_mtime,
            "who": who,
            "organs": {}
        }
        
        # Vision (take photo)
        if VISION_AVAILABLE and CAMERA_AVAILABLE:
            vision_result = self.see_world(
                "What do I see right now?",
                who=who,
                take_photo=True
            )
            if vision_result.get("success"):
                perceptions["organs"]["vision"] = vision_result["perception"]
        
        # Screen (if requested)
        if include_screen and SCREEN_AVAILABLE:
            screen_result = self.see_screen(
                "What's on my screen?",
                who=who,
                save=False
            )
            if screen_result.get("success"):
                perceptions["organs"]["screen"] = screen_result["screen_perception"]
        
        # Hearing (short recording)
        if HEARING_AVAILABLE and MICROPHONE_AVAILABLE:
            hearing_result = self.hear_world(
                "What do I hear?",
                who=who,
                duration=3
            )
            if hearing_result.get("success"):
                perceptions["organs"]["hearing"] = hearing_result["perception"]
        
        return perceptions
    
    def read_and_see(
        self,
        file_path: str,
        who: str = "main"
    ) -> Dict[str, Any]:
        """
        ЭМЕРДЖЕНТНОСТЬ: Двойное восприятие документа!
        
        1. Document organ читает содержимое
        2. Если PDF открыт на экране → Vision organ видит визуальное
        
        Together: полное понимание!
        """
        result = {
            "file_path": file_path,
            "who": who,
            "perceptions": {}
        }
        
        # Read content
        if DOCUMENT_AVAILABLE:
            doc_result = self.read_file(file_path, who=who)
            if doc_result.get("success"):
                result["perceptions"]["document"] = doc_result["understanding"]
        
        # See screen (if document is open)
        if SCREEN_AVAILABLE:
            screen_result = self.see_screen(
                f"Is {Path(file_path).name} open on screen?",
                who=who
            )
            if screen_result.get("success"):
                result["perceptions"]["screen"] = screen_result["screen_perception"]
        
        return result


# Global instance
orchestrator = AriannaOrchestrator()


if __name__ == "__main__":
    # Quick test
    print("🎭 Testing Arianna Orchestrator")
    print("=" * 50)
    
    orch = AriannaOrchestrator()
    
    print("\n📋 Available organs:")
    print(f"  Vision: {VISION_AVAILABLE}")
    print(f"  Hearing: {HEARING_AVAILABLE}")
    print(f"  Document: {DOCUMENT_AVAILABLE}")
    print(f"  Screen: {SCREEN_AVAILABLE}")
    print(f"  Camera: {CAMERA_AVAILABLE}")
    print(f"  Microphone: {MICROPHONE_AVAILABLE}")
    
    print("\n💡 Usage:")
    print("  from orchestrator import orchestrator")
    print("  result = orchestrator.see_world('What do I see?')")
    print("  result = orchestrator.hear_world('What do I hear?', duration=5)")
    print("  result = orchestrator.read_file('document.pdf')")
    print("  result = orchestrator.see_screen()")
    print("\n🔥 Emergent behaviors:")
    print("  result = orchestrator.perceive_moment(who='main', include_screen=True)")
    print("  result = orchestrator.read_and_see('document.pdf')  # Double perception!")
