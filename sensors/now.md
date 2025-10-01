📋 ЧТО ДЕЛАТЬ СЕЙЧАС:
cd ~/arianna_body
git pull

# Установка
pkg install termux-api termux-tools -y
mkdir -p sensors bridges ~/.arianna/photos ~/.arianna/audio

# Тесты
python3 sensors/camera_bridge.py
python3 sensors/microphone_bridge.py
python3 bridges/claude_app_bridge.py

НЕТ, БРАТИШ! Это дополнительное приложение к основному Termux!
📱 Как это работает:
Termux (основной)
Твой терминал, где работает Arianna
Уже установлен у тебя
Termux:API (addon)
Маленькое приложение-компаньон
Дает Termux доступ к Android сенсорам
Ставится ОТДЕЛЬНО из F-Droid или Google Play
🔧 Схема:
└──────────────────┘
✅ Что нужно сделать:
1. В Termux (уже есть):
api
Это ставит команды типа termux-camera-photo
2. В F-Droid или Google Play:
Найти и установить отдельное приложение "Termux:API"
🎯 Где скачать Termux:API:
F-Droid (рекомендую):
Открой F-Droid app
Поиск: "Termux:API"
Install
Google Play:
Play Store
Поиск: "Termux:API"
Install
⚠️ ВАЖНО: Версия Termux:API должна совпадать с версией основного Termux!
🔍 Как проверить что всё работает:
!
Короче:
Termux = терминал (уже есть)
Termux:API = addon для сенсоров (нужно поставить отдельно)
Работают вместе! 💪
Понятно теперь, братиш? 🔥
