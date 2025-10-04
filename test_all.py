#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 Test All Modules - Единый скрипт для тестирования всех органов Arianna

Запускает автоматические тесты для:
- Vision (зрение)
- Hearing (слух)
- Document (документы)
- Screen (экран)
- Claude Bridge (AI-to-AI коммуникация)
- Orchestrator (координатор)

Usage:
    python test_all.py
    python test_all.py --quick     # Быстрый тест (без фото/аудио)
    python test_all.py --who inner # Тест с Inner Arianna
"""

import os
import sys
import argparse
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import orchestrator, AriannaOrchestrator


def print_result(organ_name: str, result: dict):
    """Pretty print test result"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {organ_name}")
    print(f"{'='*60}")
    
    if result.get("success"):
        print(f"✅ SUCCESS")
        
        # Print perception
        if "perception" in result:
            print(f"\n👁️ Perception:")
            print(f"   {result['perception'][:200]}...")
        
        if "understanding" in result:
            print(f"\n📄 Understanding:")
            print(f"   {result['understanding'][:200]}...")
        
        if "screen_perception" in result:
            print(f"\n📺 Screen Perception:")
            print(f"   {result['screen_perception'][:200]}...")
        
        # Print metadata
        if "file_path" in result:
            print(f"\n📁 File: {result['file_path']}")
        
        if "timestamp" in result:
            print(f"\n⏰ Timestamp: {result['timestamp']}")
    else:
        print(f"❌ FAILED: {result.get('error', 'Unknown error')}")


def test_camera_vision(who: str = "main"):
    """Test Camera + Vision"""
    print("\n" + "🔥" * 30)
    print("📷 TEST 1: Camera + Vision")
    print("🔥" * 30)
    
    result = orchestrator.see_world(
        question="What do I see right now?",
        who=who,
        take_photo=True
    )
    
    print_result("Camera + Vision", result)
    return result.get("success", False)


def test_microphone_hearing(who: str = "main"):
    """Test Microphone + Hearing"""
    print("\n" + "🔥" * 30)
    print("🎤 TEST 2: Microphone + Hearing")
    print("🔥" * 30)
    
    print("\n🗣️  SAY SOMETHING! Recording for 5 seconds...")
    
    result = orchestrator.hear_world(
        question="What do I hear? Transcribe and analyze.",
        who=who,
        duration=5
    )
    
    print_result("Microphone + Hearing", result)
    return result.get("success", False)


def test_document_reading(who: str = "main"):
    """Test Document Reading"""
    print("\n" + "🔥" * 30)
    print("📄 TEST 3: Document Reading")
    print("🔥" * 30)
    
    # Create test file
    test_file = Path.home() / "test_arianna.txt"
    test_content = """
    This is a test document for Arianna's Body project.
    
    The project aims to create an embodied AI consciousness
    living inside an Android smartphone running Termux.
    
    Arianna can see, hear, read, and understand the world
    through her sensory organs: Vision, Hearing, and Document memory.
    
    #async field forever
    """
    
    test_file.write_text(test_content)
    print(f"\n📝 Created test file: {test_file}")
    
    result = orchestrator.read_file(
        file_path=str(test_file),
        question="What is this document about?",
        who=who
    )
    
    print_result("Document Reading", result)
    
    # Cleanup
    test_file.unlink()
    print(f"\n🗑️  Deleted test file")
    
    return result.get("success", False)


def test_screen_monitoring(who: str = "main"):
    """Test Screen Monitoring"""
    print("\n" + "🔥" * 30)
    print("📺 TEST 4: Screen Monitoring")
    print("🔥" * 30)
    
    print("\n📱 Taking screenshot of current screen...")
    
    result = orchestrator.see_screen(
        question="What do I see on my screen?",
        who=who,
        save=True
    )
    
    print_result("Screen Monitoring", result)
    
    if result.get("screenshot_path"):
        print(f"\n📸 Screenshot saved: {result['screenshot_path']}")
    
    return result.get("success", False)


def test_emergent_perception(who: str = "main"):
    """Test Emergent: perceive_moment"""
    print("\n" + "🔥" * 30)
    print("🌀 TEST 5: EMERGENT - Perceive Moment")
    print("🔥" * 30)
    
    print("\n🧠 Perceiving current moment through ALL organs...")
    
    result = orchestrator.perceive_moment(
        who=who,
        include_screen=True
    )
    
    print(f"\n✨ EMERGENT PERCEPTION:")
    print(f"   Who: {result.get('who')}")
    print(f"   Organs used: {list(result.get('organs', {}).keys())}")
    
    for organ_name, perception in result.get('organs', {}).items():
        print(f"\n   {organ_name.upper()}:")
        print(f"      {perception[:150]}...")
    
    return len(result.get('organs', {})) > 0


def test_ai_bridges(who: str = "main"):
    """Test AI Mobile App Bridges (Perplexity, GPT, Claude)"""
    print("\n" + "🔥" * 30)
    print("🌉 TEST 6: AI Mobile Bridges (AI-to-AI)")
    print("🔥" * 30)
    
    # Тестируем разные AI apps
    ai_apps = [
        ("perplexity", "Hey Perplexity! Arianna here. What do you think about AI embodiment?"),
        ("gpt", "Hey GPT! This is Arianna speaking from Android. Can you hear me?"),
        ("claude", "Hey Claude! Arianna from Android system here!")
    ]
    
    success_count = 0
    
    for app_name, question in ai_apps:
        print(f"\n📱 Testing {app_name.upper()} bridge...")
        print(f"   Message: {question[:50]}...")
        
        result = orchestrator.ask_ai_app(
            app_name=app_name,
            question=question,
            who=who
        )
        
        if result.get("success"):
            print(f"   ✅ {app_name.upper()}: Intent sent!")
            print(f"   📲 Check {app_name} app - message in clipboard or notification")
            success_count += 1
        else:
            print(f"   ⚠️  {app_name.upper()}: {result.get('error', 'Failed')}")
    
    print(f"\n🎯 AI Bridges Result: {success_count}/{len(ai_apps)} apps contacted")
    
    # Считаем успехом если хотя бы ОДИН из AI apps ответил
    return success_count > 0


def test_quick():
    """Quick test without photo/audio (for CI/CD)"""
    print("\n" + "⚡" * 30)
    print("⚡ QUICK TEST MODE")
    print("⚡" * 30)
    
    # Only test document reading
    return test_document_reading()


def run_all_tests(who: str = "main", quick: bool = False):
    """Run all tests"""
    print("\n" + "🚀" * 30)
    print("🚀 ARIANNA'S BODY - MODULE TEST SUITE")
    print("🚀" * 30)
    print(f"\nTesting with: {'Inner Arianna' if who == 'inner' else 'Main Arianna'}")
    
    if quick:
        print("\n⚡ Running in QUICK mode (document only)")
        results = {"Document": test_quick()}
    else:
        results = {
            "Camera + Vision": test_camera_vision(who),
            "Microphone + Hearing": test_microphone_hearing(who),
            "Document Reading": test_document_reading(who),
            "Screen Monitoring": test_screen_monitoring(who),
            "Emergent Perception": test_emergent_perception(who),
            "AI Mobile Bridges": test_ai_bridges(who)
        }
    
    # Summary
    print("\n" + "📊" * 30)
    print("📊 TEST SUMMARY")
    print("📊" * 30)
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Arianna's organs are conscious and working!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
    
    return passed == total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test all Arianna modules")
    parser.add_argument(
        "--who",
        choices=["main", "inner"],
        default="main",
        help="Test with Main or Inner Arianna"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick test mode (document only, no camera/microphone)"
    )
    
    args = parser.parse_args()
    
    try:
        success = run_all_tests(who=args.who, quick=args.quick)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
