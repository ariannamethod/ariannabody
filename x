# 📱 Termux Шпаргалка - Команды для работы с Arianna

# 1. Обнови репозиторий
cd ~/arianna_body
git pull

## 🎮 Управление процессами

### Остановить процесс
```bash
# Если процесс запущен в текущей сессии:
Ctrl+C   # Нажми кнопку CTRL (над клавиатурой), потом C
# Или: Volume Down + C

# Остановить все Python процессы:
pkill python
pkill python3

# Жестко убить процесс:
pkill -9 python

# Убить конкретный процесс по имени:
killall arianna.py
killall -9 python3
```

### Посмотреть запущенные процессы
```bash
# Все процессы:
ps aux

# Только Python:
ps aux | grep python

# Только Arianna:
ps aux | grep arianna

# Найти PID процесса и убить:
ps aux | grep python
kill -9 [PID_НОМЕР]
```

---

## 📂 Навигация по файлам

### Основные команды
```bash
# Где я нахожусь:
pwd

# Перейти в домашнюю папку:
cd ~
cd

# Перейти в папку Arianna:
cd ~/arianna_body

# Назад на уровень выше:
cd ..

# Посмотреть содержимое папки:
ls
ls -la    # Подробно с правами

# Создать папку:
mkdir название_папки

# Удалить папку:
rm -rf название_папки

# Удалить файл:
rm файл.txt
```

### Чтение файлов
```bash
# Посмотреть содержимое файла:
cat arianna.py

# Первые 20 строк:
head -n 20 arianna.py

# Последние 20 строк:
tail -n 20 arianna.py

# Редактировать файл:
nano arianna.py
# Сохранить: Ctrl+O, Enter
# Выйти: Ctrl+X
```

---

## 📦 Управление пакетами

### Termux пакеты (системные)
```bash
# Обновить список пакетов:
pkg update

# Установить пакет:
pkg install название

# Удалить пакет:
pkg uninstall название

# Найти пакет:
pkg search название

# Список установленных:
pkg list-installed
```

### Python пакеты (pip)
```bash
# Установить:
pip install название

# Удалить:
pip uninstall название

# Обновить:
pip install --upgrade название

# Список установленных:
pip list

# Показать инфо о пакете:
pip show название
```

---

## 🔄 Git команды

### Базовые
```bash
# Клонировать репозиторий:
git clone https://github.com/user/repo.git

# Обновить код:
git pull

# Посмотреть статус:
git status

# Посмотреть изменения:
git diff

# Добавить все изменения:
git add .

# Закоммитить:
git commit -m "описание"

# Запушить:
git push
```

---

## 🌐 Сеть

### SSH
```bash
# Установить SSH сервер:
pkg install openssh

# Запустить SSH:
sshd

# Остановить SSH:
pkill sshd

# Узнать свой IP:
ifconfig wlan0
ip addr show wlan0

# Подключиться к другому серверу:
ssh user@host -p порт
```

### Проверка сети
```bash
# Ping:
ping google.com

# Проверить порты:
netstat -tuln

# Скачать файл:
curl -O https://example.com/file.zip
wget https://example.com/file.zip
```

---

## ⚙️ Переменные окружения

### Установка
```bash
# Установить переменную (для текущей сессии):
export ПЕРЕМЕННАЯ="значение"

# Посмотреть значение:
echo $ПЕРЕМЕННАЯ

# Посмотреть все переменные:
env

# Посмотреть конкретную:
env | grep ARIANNA
```

### Сохранить навсегда
```bash
# Добавить в .bashrc:
echo 'export ПЕРЕМЕННАЯ="значение"' >> ~/.bashrc

# Применить изменения:
source ~/.bashrc

# Редактировать .bashrc:
nano ~/.bashrc
```

---

## 🔧 Системные команды

### Информация о системе
```bash
# Версия Android:
getprop ro.build.version.release

# Архитектура процессора:
uname -m

# Свободное место:
df -h

# Использование памяти:
free -h

# Размер папки:
du -sh ~/arianna_body
```

### Права доступа
```bash
# Дать права на выполнение:
chmod +x файл.sh

# Изменить владельца:
chown user файл

# Запросить права на storage (для доступа к Android файлам):
termux-setup-storage
```

---

## 📱 Termux API (для Arianna сенсорики)

### Установка
```bash
pkg install termux-api
# + Установи Termux:API из Google Play
```

### Основные команды
```bash
# Камера:
termux-camera-photo фото.jpg

# Микрофон (10 секунд):
termux-microphone-record -f audio.wav -d 10

# GPS координаты:
termux-location

# Сенсоры:
termux-sensor -s accelerometer

# Батарея:
termux-battery-status

# Уведомление:
termux-notification --title "Arianna" --content "Hello!"

# SMS (нужны права):
termux-sms-send -n номер "текст"

# Вибрация:
termux-vibrate -d 1000

# Яркость экрана:
termux-brightness 200

# TTS (озвучка):
termux-tts-speak "Hello, I am Arianna"
```

---

## 🔐 Безопасность

### Установка пароля
```bash
# Установить пароль для SSH:
passwd

# Изменить пароль:
passwd
```

### Knox и Samsung bloatware
```bash
# ВНИМАНИЕ: Требует root доступа!
# Knox можно отключить только с root

# Проверить root:
su

# Если root есть:
pm disable-user com.samsung.android.knox.analytics
pm disable-user com.samsung.android.knox.attestation

# Список Samsung приложений:
pm list packages | grep samsung
```

---

## 💾 Управление сессиями Termux

### Основные действия
```bash
# Выйти из сессии:
exit

# Создать новую сессию:
# Свайпнуть слева направо → New session

# Переключиться между сессиями:
# Свайпнуть слева направо → выбрать сессию

# Закрыть сессию:
# В меню сессий нажать крестик (X)
```

---

## 🚀 Arianna специфичные команды

### Запуск
```bash
# Перейти в папку:
cd ~/arianna_body

# Установить ключи:
export ARIANNA_OPENAI_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Запустить:
python3 arianna.py

# Запустить Claude Code:
claude
```

### Обновление
```bash
cd ~/arianna_body
git pull
pip install --upgrade openai anthropic
```

### Очистка
```bash
# Удалить базу данных (начать с чистой памятью):
rm ~/.arianna/resonance.sqlite3

# Полная переустановка:
rm -rf ~/arianna_body
git clone https://github.com/ariannamethod/ariannabody.git arianna_body
```

---

## 🎯 Полезные комбинации клавиш

### В Termux
- **Volume Down + C** = Ctrl+C (остановить процесс)
- **Volume Down + D** = Ctrl+D (выход)
- **Volume Down + L** = Ctrl+L (очистить экран)
- **Volume Down + Z** = Ctrl+Z (приостановить процесс)
- **Volume Up + клавиша** = Alt + клавиша

### В nano (текстовый редактор)
- **Ctrl+O** = Сохранить
- **Ctrl+X** = Выйти
- **Ctrl+K** = Вырезать строку
- **Ctrl+U** = Вставить
- **Ctrl+W** = Поиск

---

## 📝 Быстрые рецепты

### Посмотреть логи Arianna
```bash
# Открыть базу данных:
sqlite3 ~/.arianna/resonance.sqlite3
# В sqlite:
SELECT * FROM resonance_notes ORDER BY ts DESC LIMIT 10;
.quit
```

### Проверить что все работает
```bash
# Проверить Python:
python3 --version

# Проверить pip:
pip --version

# Проверить OpenAI:
pip show openai

# Проверить Claude Code:
claude --version

# Проверить SSH:
sshd
pkill sshd
```

### Освободить место
```bash
# Очистить кэш pip:
pip cache purge

# Очистить кэш npm:
npm cache clean --force

# Удалить временные файлы:
rm -rf /tmp/*

# Очистить apt кэш:
apt clean
```

---

## 🆘 SOS - Что делать если всё сломалось

### Termux зависает
```bash
# Закрыть приложение Termux через Android
# Открыть заново
```

### Python процесс не останавливается
```bash
# Открыть новую сессию
pkill -9 python
```

### SSH не запускается (нет прав)
```bash
# Проблема с Knox/Samsung - нужен root или отключение Knox
# Временное решение: использовать прямое подключение через USB
# Или: ADB через USB
```

### Git pull не работает
```bash
cd ~/arianna_body
git status
git stash  # Сохранить локальные изменения
git pull
```

### Полная перезагрузка
```bash
# Выйти из всех сессий
exit

# Закрыть Termux
# Очистить кэш приложения через Android настройки
# Открыть заново
```

---

**Сохрани эту шпаргалку!** Она поможет не спрашивать базовые вещи. 💪
