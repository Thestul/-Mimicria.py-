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
PyQt6 is needed to run it.

Works seamlessly on both **Windows** and **Linux**.

### 🚀 Features
* 🔍 **Avatar Inspection:** Instantly fetch equipped items from any user by Username or UserID.
* ⚡ **Command Generation:** Automatically builds ready-to-use in-game wear commands.
* 🖥️ **GUI:** Clean and simple interface powered by PyQt6.
* 🐧 **Cross-Platform:** Full support for Windows and Linux systems.

### 🛠️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/MIMICRIA.git
cd MIMICRIA
```

**2. Run the script**
PyQt6 will be installed automatically on first run if it's missing:
```bash
python MIMICRIA.py
```
On Linux, if your system requires `--break-system-packages`, install the dependency manually beforehand:
```bash
pip install PyQt6 --break-system-packages
python3 MIMICRIA.py
```

---

## Русский

**MIMICRIA** — приложение на Python для анализа профилей аватаров Roblox: извлекает ID надетых предметов и генерирует готовые команды, чтобы повторить чужой образ прямо в игре.
Для запуска нужен PyQt6.

Полностью работает на **Windows** и **Linux**.

### 🚀 Возможности
* 🔍 **Анализ аватара:** мгновенно получает список надетых вещей по никнейму или UserID.
* ⚡ **Генерация команд:** автоматически собирает готовые команды для надевания в игре.
* 🖥️ **GUI:** простой и чистый интерфейс на PyQt6.
* 🐧 **Кроссплатформенность:** полная поддержка Windows и Linux.

### 🛠️ Установка и запуск

**1. Клонируйте репозиторий**
```bash
git clone https://github.com/YOUR_USERNAME/MIMICRIA.git
cd MIMICRIA
```

**2. Запустите скрипт**
PyQt6 установится автоматически при первом запуске, если его нет:
```bash
python MIMICRIA.py
```
На Linux, если система требует `--break-system-packages`, установите зависимость вручную заранее:
```bash
pip install PyQt6 --break-system-packages
python3 MIMICRIA.py
```
