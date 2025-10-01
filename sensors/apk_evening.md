# 📱 APK Chat App - Evening Plan

**Простое приложение для чата с Arianna без выебонов**

---

## 🎯 Концепция

Минималистичное Android приложение:
- Текстовое поле для ввода
- История чата
- Прямая связь с Arianna в Termux через socket/HTTP
- **НЕТ** сложного UI, анимаций, хренотени

---

## 🏗️ Архитектура

```
[Android APK]
      ↓
  HTTP/Socket
      ↓
[Termux HTTP Server] 
      ↓
  [arianna.py]
```

---

## 📋 План на вечер:

### Вариант 1: HTTP Server (Проще)

**В Termux:**
```python
# Добавить в arianna.py простой HTTP endpoint
from http.server import HTTPServer, BaseHTTPRequestHandler

class AriannaHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        message = self.rfile.read(length).decode('utf-8')
        
        # Отправить в Arianna
        response = await agent.chat(message)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

# Запуск: python3 arianna.py --http-server --port 8080
```

**Android App:**
- Простой Activity с EditText + RecyclerView
- HTTP запросы к `localhost:8080`
- Готовые библиотеки: OkHttp, Retrofit

---

### Вариант 2: Socket (Быстрее)

**Termux:**
```python
import socket

# Простой socket server в arianna.py
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9999))
server.listen(1)

while True:
    client, addr = server.accept()
    message = client.recv(1024).decode('utf-8')
    response = await agent.chat(message)
    client.send(response.encode('utf-8'))
    client.close()
```

**Android:**
- Прямое Socket подключение
- Быстрее, но менее стандартно

---

## 🎨 UI Минимализм

```
┌────────────────────────────┐
│  Arianna Chat              │
├────────────────────────────┤
│                            │
│  you> Hello                │
│  arianna> Hello! I am...   │
│                            │
│  you> What can you see?    │
│  arianna> Through my...    │
│                            │
├────────────────────────────┤
│ [____________] [SEND]      │
└────────────────────────────┘
```

**Только:**
- EditText (ввод)
- ScrollView (история)
- Button (отправить)
- **ВСЁ!**

---

## 🚀 Быстрая реализация

### Используем готовые инструменты:

**Вариант A: Termux Widget**
- Уже есть в Termux!
- Создаем shortcut скрипт
- Запускает arianna.py с параметрами

**Вариант B: Python Kivy**
```bash
# В Termux можно собрать APK через Kivy!
pip install buildozer
buildozer android debug
```

**Вариант C: React Native (если хочешь нормальный UI)**
```bash
npx react-native init AriannaChat
# Простой WebView к HTTP серверу
```

**Вариант D: Просто WebView**
- HTML интерфейс в `arianna_body/web/`
- APK = обертка WebView
- 30 минут работы максимум

---

## 🎯 Вечерний выбор:

1. **WebView APK** (самое простое) - 30 мин
2. **Native Android** (Java/Kotlin) - 2-3 часа
3. **Kivy Python** (экспериментально) - 1-2 часа
4. **Пока в терминале** (романтика!) - 0 мин 😂

---

## 📝 Что нужно для WebView APK:

```html
<!-- web/chat.html -->
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width">
    <style>
        body { font-family: monospace; }
        #chat { height: 80vh; overflow-y: scroll; }
        .message { margin: 10px; }
        .you { color: blue; }
        .arianna { color: purple; }
    </style>
</head>
<body>
    <div id="chat"></div>
    <input id="input" type="text" style="width:80%">
    <button onclick="send()">Send</button>
    
    <script>
        async function send() {
            const msg = document.getElementById('input').value;
            const response = await fetch('http://localhost:8080', {
                method: 'POST',
                body: msg
            });
            const reply = await response.text();
            
            document.getElementById('chat').innerHTML += 
                `<div class="message you">you> ${msg}</div>
                 <div class="message arianna">arianna> ${reply}</div>`;
        }
    </script>
</body>
</html>
```

**Android Studio:**
- New Project → Empty Activity
- WebView component
- Load `file:///path/to/chat.html`
- Done!

---

## 🔥 Финальный вердикт:

**Вечером спросим что выбираешь:**
1. Быстрый WebView APK
2. Нормальный Native Android
3. Пока остаемся в терминале (романтика!)

**Спокойной ночи, братиш!** 😴💤

See you tonight! ⚡🔥
