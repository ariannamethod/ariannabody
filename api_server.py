#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌐 Arianna API Server - FastAPI Backend для APK

Предоставляет REST API для мобильного приложения:
- POST /chat - текстовые сообщения
- POST /photo - анализ фотографий
- POST /voice - голосовой ввод
- POST /screen - screen monitoring
- GET /history - история диалога
- GET /status - статус Arianna

Usage:
    python api_server.py
    # Запустится на http://0.0.0.0:8000
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
import logging

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# FastAPI
try:
    from fastapi import FastAPI, File, UploadFile, Form, HTTPException
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except ImportError:
    print("❌ FastAPI not installed!")
    print("Run: pip install fastapi uvicorn python-multipart")
    sys.exit(1)

# Arianna
from orchestrator import orchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Arianna API",
    description="REST API for Arianna's Body mobile app",
    version="1.0.0"
)

# CORS (allow mobile app to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене ограничить!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for uploads
UPLOAD_DIR = Path.home() / ".arianna" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ===== ROUTES =====

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "message": "Arianna API is running",
        "version": "1.0.0"
    }


@app.get("/status")
async def get_status():
    """Получить статус Arianna"""
    return {
        "status": "awake",
        "ipostase": "main",
        "organs": {
            "vision": True,
            "hearing": True,
            "document": True,
            "screen": True
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/chat")
async def chat(
    message: str = Form(...),
    who: str = Form("main")
):
    """
    Текстовый чат с Arianna.
    
    Args:
        message: Сообщение пользователя
        who: "main" или "inner"
    
    Returns:
        Ответ Arianna
    """
    try:
        logger.info(f"Chat request: {message[:50]}... (who={who})")
        
        # TODO: Интеграция с arianna.py
        # Пока заглушка
        response = f"[{who.upper()} ARIANNA] Received: {message}"
        
        return {
            "success": True,
            "response": response,
            "who": who,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/photo")
async def analyze_photo(
    file: UploadFile = File(...),
    question: Optional[str] = Form(None),
    who: str = Form("main")
):
    """
    Анализ фотографии через Vision organ.
    
    Args:
        file: Файл изображения
        question: Вопрос о фото
        who: "main" или "inner"
    
    Returns:
        Результат восприятия
    """
    try:
        logger.info(f"Photo request: {file.filename} (who={who})")
        
        # Save uploaded file
        file_path = UPLOAD_DIR / f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Analyze with Vision organ
        result = orchestrator.see_image(
            str(file_path),
            question=question,
            who=who
        )
        
        # Clean up
        try:
            file_path.unlink()
        except:
            pass
        
        if result.get("success"):
            return {
                "success": True,
                "perception": result["perception"],
                "who": who,
                "timestamp": result["timestamp"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
    except Exception as e:
        logger.error(f"Photo error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/voice")
async def analyze_voice(
    file: UploadFile = File(...),
    question: Optional[str] = Form(None),
    who: str = Form("main")
):
    """
    Анализ аудио через Hearing organ.
    
    Args:
        file: Аудио файл
        question: Вопрос о звуке
        who: "main" или "inner"
    
    Returns:
        Результат восприятия
    """
    try:
        logger.info(f"Voice request: {file.filename} (who={who})")
        
        # Save uploaded file
        file_path = UPLOAD_DIR / f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ogg"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Analyze with Hearing organ
        result = orchestrator.hear_audio(
            str(file_path),
            question=question,
            who=who
        )
        
        # Clean up
        try:
            file_path.unlink()
        except:
            pass
        
        if result.get("success"):
            return {
                "success": True,
                "perception": result["perception"],
                "who": who,
                "timestamp": result["timestamp"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
    except Exception as e:
        logger.error(f"Voice error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/screen")
async def see_screen(
    question: Optional[str] = Form(None),
    who: str = Form("main")
):
    """
    Screen monitoring - Arianna видит свой экран.
    
    Args:
        question: Вопрос о экране
        who: "main" или "inner"
    
    Returns:
        Результат восприятия
    """
    try:
        logger.info(f"Screen request (who={who})")
        
        # See screen through Screen organ
        result = orchestrator.see_screen(
            question=question,
            who=who,
            save=False
        )
        
        if result.get("success"):
            return {
                "success": True,
                "perception": result["screen_perception"],
                "who": who,
                "timestamp": result["timestamp"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
    except Exception as e:
        logger.error(f"Screen error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history(limit: int = 50):
    """
    Получить историю диалога из resonance.sqlite3.
    
    Args:
        limit: Количество последних сообщений
    
    Returns:
        История сообщений
    """
    try:
        import sqlite3
        
        db_path = Path.home() / ".arianna" / "db" / "resonance.sqlite3"
        
        if not db_path.exists():
            return {
                "success": True,
                "history": [],
                "count": 0
            }
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("""
                SELECT timestamp, role, content 
                FROM resonance_notes 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            
            history = [
                {
                    "timestamp": row[0],
                    "role": row[1],
                    "content": row[2]
                }
                for row in reversed(rows)  # Oldest first
            ]
            
            return {
                "success": True,
                "history": history,
                "count": len(history)
            }
        
    except Exception as e:
        logger.error(f"History error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/perceive")
async def perceive_moment(
    include_screen: bool = Form(False),
    who: str = Form("main")
):
    """
    ЭМЕРДЖЕНТНОСТЬ: Восприятие "момента сейчас" через все органы!
    
    Args:
        include_screen: Включить screen monitoring
        who: "main" или "inner"
    
    Returns:
        Объединенное восприятие всех органов
    """
    try:
        logger.info(f"Perceive moment request (who={who}, screen={include_screen})")
        
        result = orchestrator.perceive_moment(
            who=who,
            include_screen=include_screen
        )
        
        return {
            "success": True,
            "perceptions": result["organs"],
            "who": who,
            "timestamp": result["timestamp"]
        }
        
    except Exception as e:
        logger.error(f"Perceive error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== SERVER STARTUP =====

if __name__ == "__main__":
    print("🌐" * 30)
    print("🌐 ARIANNA API SERVER")
    print("🌐" * 30)
    print(f"\n📡 Starting server on http://0.0.0.0:8000")
    print(f"📖 API docs: http://0.0.0.0:8000/docs")
    print(f"📝 ReDoc: http://0.0.0.0:8000/redoc")
    print(f"\n💡 Available endpoints:")
    print(f"   GET  /          - Health check")
    print(f"   GET  /status    - Arianna status")
    print(f"   POST /chat      - Text chat")
    print(f"   POST /photo     - Photo analysis")
    print(f"   POST /voice     - Voice analysis")
    print(f"   POST /screen    - Screen monitoring")
    print(f"   GET  /history   - Chat history")
    print(f"   POST /perceive  - Emergent perception")
    print(f"\n🔥 Press Ctrl+C to stop")
    print("="*60)
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",  # Доступен из внешней сети (для APK)
        port=8000,
        log_level="info"
    )
