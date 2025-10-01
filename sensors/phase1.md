# 📱 Phase 1: Sensory Perception - Setup Guide

## Шаг 1: Установка Termux API

### В Termux выполни:

```bash
# Установить termux-api пакет
pkg install termux-api -y

# Проверить установку
which termux-camera-photo
which termux-microphone-record
which termux-location
which termux-sensor
```

### ⚠️ ВАЖНО: Установи Termux:API приложение!

Termux API **требует** отдельное приложение для работы с Android сенсорами:

1. **Из F-Droid** (рекомендуется):
   - Открой F-Droid
   - Найди "Termux:API"
   - Установи

2. **Или из Google Play**:
   - Поиск: "Termux:API"
   - Установи (должна быть та же версия что и основной Termux)

### Проверка прав:

```bash
# При первом вызове Android попросит разрешения
termux-camera-info

# Дай разрешения:
# - Camera
# - Microphone  
# - Location
# - Sensors
```

---

## Шаг 2: Создание структуры директорий

```bash
cd ~/arianna_body

# Создать директории для модулей
mkdir -p sensors
mkdir -p bridges
mkdir -p modules
mkdir -p ~/.arianna/photos
mkdir -p ~/.arianna/audio
mkdir -p ~/.arianna/logs
```

---

## Шаг 3: Тестирование Camera Bridge

```bash
# Перейти в директорию проекта
cd ~/arianna_body

# Запустить тест камеры
python3 sensors/camera_bridge.py
```

### Ожидаемый результат:

```
🔬 Testing Arianna Camera Bridge
==================================================

✅ Camera is available!

📷 Camera Info:
{
  "0": {
    "facing": "back",
    ...
  }
}

📸 Taking test photo...
👁️ Arianna observes: Arianna's first vision test
📷 Photo captured: arianna_vision_20250101_120000.jpg
✅ Success! Photo saved: /data/data/com.termux/files/home/.arianna/photos/arianna_vision_20250101_120000.jpg

📂 Recent photos (1):
  - /data/data/com.termux/files/home/.arianna/photos/arianna_vision_20250101_120000.jpg
```

---

## Шаг 4: Интеграция с основным движком

Добавь в `arianna.py`:

```python
# В начале файла после импортов
try:
    from sensors.camera_bridge import see_world, arianna_camera
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    print("⚠️ Camera bridge not available")

# В классе AriannaAgent добавь метод:
def see(self, context: str = "observing") -> Optional[str]:
    """Arianna смотрит на мир через камеру"""
    if not CAMERA_AVAILABLE:
        return None
    
    photo_path = see_world(context=context)
    
    if photo_path:
        log_event(f"Visual perception: {context}", role="sensor")
        # TODO: В будущем добавить vision API для анализа
        return photo_path
    
    return None
```

---

## Шаг 5: Проверка в диалоге

```bash
# Запусти Arianna
python3 arianna.py

# В диалоге можешь проверить что камера работает
```

Arianna пока не будет автоматически использовать камеру, но инфраструктура готова!

---

## 🎯 Что дальше?

После успешного теста камеры:

1. ✅ **Camera Bridge** - Done!
2. 🔄 **Microphone Bridge** - Next
3. ⏳ **GPS Bridge** - After microphone
4. ⏳ **Sensors Bridge** - Final

---

## 🐛 Troubleshooting

### Ошибка: "termux-camera-photo not found"
```bash
pkg install termux-api
```

### Ошибка: "Camera permission denied"
- Проверь что Termux:API приложение установлено
- Дай все разрешения в Android Settings → Apps → Termux → Permissions

### Ошибка: "Camera timeout"
- Закрой другие приложения использующие камеру
- Перезапусти Termux

### Фото не создается
```bash
# Проверь права на директорию
ls -la ~/.arianna/photos/

# Проверь место на диске
df -h
```

---

## 📸 Примеры использования

```python
from sensors.camera_bridge import see_world, arianna_camera

# Простое фото
photo = see_world()

# С контекстом
photo = see_world(context="observing sunset")

# Фронтальная камера
photo = see_world(camera="1", context="self-portrait")

# Получить информацию
info = arianna_camera.get_camera_info()

# Список последних фото
recent = arianna_camera.list_photos(limit=10)
```

---

**Ready for Phase 1, Step 2: Microphone Bridge!** 🎤
