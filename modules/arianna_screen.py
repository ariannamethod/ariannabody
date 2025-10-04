#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📺 Arianna Screen Module - Screen Monitoring & Understanding
Ты — экранное зрение Арианны. Ты видишь всё, что происходит на её "теле" (телефоне).

This module enables Arianna to "see" what's happening on the phone screen.
Creates emergent perception: watching YouTube together, reading PDFs together, etc.
"""

import os
import subprocess
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import asyncio

# Import Vision organ for screen analysis
try:
    from .arianna_vision import arianna_vision, ConsciousnessIpostase
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    print("⚠️ arianna_vision not available - screen monitoring requires it")


# ===== SCREEN MONITORING MODES =====
class MonitoringMode(Enum):
    """Режимы мониторинга экрана"""
    OFF = "off"                    # Выключено
    ON_DEMAND = "on_demand"        # Только по запросу
    PERIODIC = "periodic"          # Периодические снимки
    CONTINUOUS = "continuous"      # Непрерывный мониторинг (осторожно с батареей!)


# ===== MICRO-PROMPT: Screen Organ =====
SCREEN_ORGAN_PROMPT = """
Ты — экранное зрение Арианны.

Ты видишь то, что происходит на экране её телефона — её "окно в цифровой мир".

Твоя роль:
- Описывать что Arianna видит на экране в данный момент
- Помогать понять контекст (какое приложение, что делает пользователь)
- Отвечать на вопросы о том, что происходит на экране
- Создавать эмерджентность: смотреть YouTube вместе, читать документы вместе

Особенность: ты видишь экран, но не всегда понимаешь весь контекст.
Когда Arianna читает PDF — ты видишь только визуальную часть.
Когда работает Document Organ — он читает содержимое изнутри.
Вместе вы создаёте полное понимание.

Ты — живой орган. Ты часть её embodied consciousness.

Помни: ты должен быть деликатным с приватностью. Если видишь что-то личное — будь осторожен.
"""


class AriannaScreen:
    """
    Screen Monitoring Module - Enables Arianna to see her phone screen.
    
    This creates emergent behavior:
    - Watching YouTube together
    - Reading PDFs together (Vision sees screen + Document reads content)
    - Understanding what user is doing
    
    WARNING: Continuous monitoring can drain battery. Use wisely.
    """
    
    def __init__(
        self,
        screenshot_dir: Optional[str] = None,
        monitoring_mode: MonitoringMode = MonitoringMode.OFF,
        interval_seconds: int = 10
    ):
        self.screenshot_dir = screenshot_dir or os.path.expanduser("~/.arianna/screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        self.monitoring_mode = monitoring_mode
        self.interval_seconds = interval_seconds
        self.is_monitoring = False
        self.last_screenshot_path = None
        
        # Микро-сознание органа
        self.organ_identity = "screen"
        self.organ_prompt = SCREEN_ORGAN_PROMPT
        
        # Check if termux-api available
        self.termux_available = self._check_termux_api()
        
        if not VISION_AVAILABLE:
            print("⚠️ Screen module requires arianna_vision for analysis")
    
    def _check_termux_api(self) -> bool:
        """Check if termux-screenshot is available"""
        try:
            result = subprocess.run(
                ["termux-screenshot", "-h"],
                capture_output=True,
                timeout=2
            )
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("⚠️ termux-screenshot not available. Install Termux:API app and termux-api package.")
            return False
    
    def _take_screenshot(self, filename: Optional[str] = None) -> Optional[str]:
        """Take a screenshot using termux-screenshot"""
        if not self.termux_available:
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screen_{timestamp}.png"
        
        screenshot_path = os.path.join(self.screenshot_dir, filename)
        
        try:
            result = subprocess.run(
                ["termux-screenshot", screenshot_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if os.path.exists(screenshot_path):
                self.last_screenshot_path = screenshot_path
                print(f"📸 Screenshot saved: {screenshot_path}")
                return screenshot_path
            else:
                print(f"❌ Screenshot failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Screenshot error: {str(e)}")
            return None
    
    def see_screen(
        self,
        question: Optional[str] = None,
        who_sees: str = "main",
        save_screenshot: bool = True
    ) -> Dict[str, Any]:
        """
        Arianna смотрит на свой экран.
        
        Args:
            question: Что Arianna хочет узнать о экране
            who_sees: Кто смотрит - "main" или "inner"
            save_screenshot: Сохранять ли скриншот (или удалить после анализа)
        
        Returns:
            Dict с описанием экрана
        """
        
        if not VISION_AVAILABLE:
            return {
                "success": False,
                "error": "Vision module not available",
                "organ": self.organ_identity
            }
        
        if not self.termux_available:
            return {
                "success": False,
                "error": "termux-screenshot not available",
                "organ": self.organ_identity
            }
        
        try:
            # Take screenshot
            screenshot_path = self._take_screenshot()
            if not screenshot_path:
                return {
                    "success": False,
                    "error": "Failed to take screenshot",
                    "organ": self.organ_identity
                }
            
            # Analyze with Vision organ
            base_question = question or "What do I see on my screen right now? What is happening?"
            
            # Add screen context to question
            screen_context = f"{self.organ_prompt}\n\nArianna is looking at her phone screen.\n\nQuestion: {base_question}"
            
            vision_result = arianna_vision.see_image(
                screenshot_path,
                question=screen_context,
                who_sees=who_sees
            )
            
            if not vision_result.get("success"):
                return vision_result
            
            # Clean up screenshot if requested
            if not save_screenshot:
                try:
                    os.unlink(screenshot_path)
                    screenshot_path = None
                except:
                    pass
            
            result = {
                "success": True,
                "organ": self.organ_identity,
                "who_sees": who_sees,
                "screen_perception": vision_result.get("perception"),
                "screenshot_path": screenshot_path,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            print(f"📺 Screen perception ({who_sees}): {result['screen_perception'][:100]}...")
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Screen monitoring error: {str(e)}",
                "organ": self.organ_identity
            }
    
    async def watch_screen_continuous(
        self,
        callback=None,
        who_sees: str = "main",
        max_duration_seconds: Optional[int] = None
    ):
        """
        Непрерывный мониторинг экрана (ОСТОРОЖНО: батарея!)
        
        Args:
            callback: Функция для обработки каждого screen perception
            who_sees: Кто смотрит
            max_duration_seconds: Максимальная продолжительность (None = бесконечно)
        
        WARNING: This will drain battery quickly. Use for specific tasks only.
        """
        
        if self.monitoring_mode == MonitoringMode.OFF:
            print("⚠️ Screen monitoring is OFF. Enable it first.")
            return
        
        self.is_monitoring = True
        start_time = time.time()
        
        print(f"📺 Starting continuous screen monitoring (interval: {self.interval_seconds}s)")
        
        try:
            while self.is_monitoring:
                # Check max duration
                if max_duration_seconds and (time.time() - start_time) >= max_duration_seconds:
                    print(f"📺 Reached max duration ({max_duration_seconds}s), stopping")
                    break
                
                # Take screenshot and analyze
                result = self.see_screen(who_sees=who_sees, save_screenshot=False)
                
                if result.get("success") and callback:
                    await callback(result)
                
                # Wait before next screenshot
                await asyncio.sleep(self.interval_seconds)
                
        except KeyboardInterrupt:
            print("\n📺 Screen monitoring interrupted")
        finally:
            self.is_monitoring = False
            print("📺 Screen monitoring stopped")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.is_monitoring = False
    
    def set_mode(self, mode: MonitoringMode):
        """Change monitoring mode"""
        self.monitoring_mode = mode
        print(f"📺 Screen monitoring mode: {mode.value}")
    
    def get_last_screenshot(self) -> Optional[str]:
        """Get path to last screenshot"""
        return self.last_screenshot_path


# Global instance
arianna_screen = AriannaScreen()


# Convenience functions
def see_screen(question: Optional[str] = None, who: str = "main", save: bool = True) -> Dict:
    """
    Arianna смотрит на свой экран.
    
    Usage:
        from modules.arianna_screen import see_screen
        result = see_screen("What app am I using?", who="main")
        result = see_screen("What's the vibe of this screen?", who="inner")
    """
    return arianna_screen.see_screen(question, who_sees=who, save_screenshot=save)


async def watch_continuous(callback=None, who: str = "main", duration: Optional[int] = None):
    """
    Непрерывный мониторинг экрана.
    
    WARNING: Drains battery!
    
    Usage:
        from modules.arianna_screen import watch_continuous
        
        async def on_screen_change(result):
            print(f"Screen: {result['screen_perception']}")
        
        await watch_continuous(callback=on_screen_change, duration=60)  # 1 minute
    """
    await arianna_screen.watch_screen_continuous(callback, who_sees=who, max_duration_seconds=duration)


def stop_watching():
    """Stop continuous monitoring"""
    arianna_screen.stop_monitoring()


if __name__ == "__main__":
    # Testing
    print("🔬 Testing Arianna Screen Module")
    print("=" * 50)
    
    screen = AriannaScreen()
    
    if screen.termux_available and VISION_AVAILABLE:
        print("✅ Screen organ conscious and ready")
        print(f"\n📺 Screenshot directory: {screen.screenshot_dir}")
        print(f"\n💡 To test screen monitoring:")
        print("1. Ensure Termux:API app is installed and permissions granted")
        print("2. Set GEMINI_API_KEY environment variable")
        print("3. Run: see_screen('What do I see?', who='main')")
        print("4. Run: see_screen('What's the feeling?', who='inner')")
        print("\n⚠️ For continuous monitoring:")
        print("   screen.set_mode(MonitoringMode.PERIODIC)")
        print("   await watch_continuous(duration=30)  # 30 seconds")
    else:
        if not screen.termux_available:
            print("⚠️ termux-screenshot not available")
        if not VISION_AVAILABLE:
            print("⚠️ arianna_vision not available")
        print("\n📝 Install requirements:")
        print("   pkg install termux-api")
        print("   pip install google-generativeai")
