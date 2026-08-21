# MIMICRIA

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyQt-6-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge" alt="License">
</p>

**English** | [Русский](#русский)

---

## English

**MIMICRIA** is a Python application designed to inspect Roblox avatar profiles, extract equipped asset IDs, and generate executable commands to mimic their outfit in-game.

Works seamlessly on both **Windows** and **Linux**.

### 🚀 Features
* 🔍 **Avatar Inspection:** Instantly fetch equipped items from any user by Username or UserID.
* ⚡ **Command Generation:** Automatically builds ready-to-use in-game wear commands.
* 🖥️ **GUI:** Clean and simple interface powered by PyQt6.
* 🎨 **Themes:** Dark/Light built-in, custom themes via `themes.json`.
* 🐧 **Cross-Platform:** Full support for Windows and Linux systems.

### 🛠️ Installation & Setup

**1. Install Python**
Make sure Python 3.8+ is installed.
- **Windows:** download from [python.org](https://www.python.org/downloads/) — during install, check **"Add python.exe to PATH"**.
- **Linux:** usually preinstalled. If not: `sudo apt install python3 python3-pip` (Debian/Ubuntu).

**2. Get the files**
Download `Mimicria[0.3].py` and `themes.json` from this repo into the same folder (use the green **Code → Download ZIP** button, or download the files individually).

**3. Run the script**

**Windows (PowerShell / CMD):**
```bash
py -m pip install PyQt6
py "Mimicria[0.3].py"
```

**Linux:**
```bash
pip install PyQt6 --break-system-packages
python3 "Mimicria[0.3].py"
```

PyQt6 will also try to install itself automatically on first run if it's missing — the manual `pip install` step above is a fallback in case that fails.

---

## Русский

**MIMICRIA** — приложение на Python для анализа профилей аватаров Roblox: извлекает ID надетых предметов и генерирует готовые команды, чтобы повторить чужой образ прямо в игре.

Полностью работает на **Windows** и **Linux**.

### 🚀 Возможности
* 🔍 **Анализ аватара:** мгновенно получает список надетых вещей по никнейму или UserID.
* ⚡ **Генерация команд:** автоматически собирает готовые команды для надевания в игре.
* 🖥️ **GUI:** простой и чистый интерфейс на PyQt6.
* 🎨 **Темы:** встроенные Dark/Light, кастомные темы через `themes.json`.
* 🐧 **Кроссплатформенность:** полная поддержка Windows и Linux.

### 🛠️ Установка и запуск

**1. Установите Python**
Нужен Python 3.8 или новее.
- **Windows:** скачайте с [python.org](https://www.python.org/downloads/) — при установке обязательно поставьте галочку **"Add python.exe to PATH"**.
- **Linux:** обычно уже есть. Если нет: `sudo apt install python3 python3-pip` (Debian/Ubuntu).

**2. Скачайте файлы**
Скачайте `Mimicria[0.3].py` и `themes.json` из репозитория в одну папку (кнопка **Code → Download ZIP**, либо файлы по отдельности).

**3. Запустите скрипт**

**Windows (PowerShell / CMD):**
```bash
py -m pip install PyQt6
py "Mimicria[0.3].py"
```

**Linux:**
```bash
pip install PyQt6 --break-system-packages
python3 "Mimicria[0.3].py"
```

PyQt6 также попытается установиться автоматически при первом запуске, если его нет — ручная установка выше нужна на случай, если автоустановка не сработает.
