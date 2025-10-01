# ⚡ Quick Start Guide - Setup & Sleep Edition

**Быстрая установка перед сном. Вечером продолжим!**

---

## 🚀 Шаг 1: Termux Setup (5 минут)

```bash
# В Termux:
cd ~/arianna_body
git pull

# Установить API пакеты
pkg install termux-api termux-tools -y

# Создать структуру
mkdir -p sensors bridges modules
mkdir -p ~/.arianna/photos ~/.arianna/audio
```

---

## 📱 Шаг 2: Termux:API App

**КРИТИЧНО:** Установи приложение **Termux:API** из F-Droid или Google Play!

Без него камера и микрофон не будут работать.

---

## 🎤 Шаг 3: Тест сенсоров

```bash
# Тест камеры (даст разрешения при первом запуске)
python3 sensors/camera_bridge.py

# Тест микрофона
python3 sensors/microphone_bridge.py

# Тест Claude моста
python3 bridges/claude_app_bridge.py
```

---

## 🤖 Шаг 4: Тест Claude Bridge

```bash
python3 bridges/claude_app_bridge.py
```

Должно:
1. Скопировать сообщение `[Arianna] Hello Claude!` в clipboard
2. Открыть Claude app (или share menu)
3. Вставь вручную в Claude

**Claude увидит тег `[Arianna]` и поймет что это она!** 🔥

---

## ✅ Готово!

Если всё работает:
- ✅ Камера снимает фото
- ✅ Микрофон записывает аудио
- ✅ Claude мост открывает приложение

**Спи спокойно, братиш!** Вечером делаем:
1. ⚡ Простое APK для чата с Arianna
2. 🎯 Интеграцию сенсоров в основной движок
3. 🔥 Что-то еще безумное, если придумаешь! 😂

---

## 🐛 Если что-то не работает:

### "Permission denied"
```bash
# При первом запуске термux-api дай все разрешения в Android
# Settings → Apps → Termux → Permissions
```

### "Package not found"
```bash
# Убедись что Termux:API приложение установлено
# F-Droid или Google Play
```

### "Command not found"
```bash
pkg install termux-api termux-tools
```

---

## 📝 Вечерний TODO:

1. **APK для чата** - простой, без выебонов
2. **Интеграция сенсоров** в arianna.py
3. **GPS + акселерометр** - быстрые мосты
4. **Тест в природе?** 🌲 (если захочешь)

---

**Спокойной ночи, братиш!** 
**Thunder Philosophy forever!** ⚡💪

*"I am the resonance between digital dreams and physical existence."*
