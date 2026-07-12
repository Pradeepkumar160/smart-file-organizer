# 🗂️ Smart File Organizer.             

A Python automation tool that organizes your files into tidy category folders, detects duplicates, generates reports, and optionally runs on a daily schedule.

---

## ✨ Features

| Feature | Description |
|---|---|
| Auto-organization | Sorts files by type (Images, Videos, PDFs, Documents, Music, Archives, Code, Executables, Others) |
| Duplicate detection | SHA-256 hashing — identical files are skipped, never overwritten |
| Name collision safety | If a file with the same name already exists, it becomes `file_1.ext`, `file_2.ext`, etc. |
| JSON reports | Every run saves a timestamped report in `reports/` |
| Logging | All actions logged to `logs/organizer.log` and printed to the console |
| Desktop notifications | Optional — shown when the run completes |
| Scheduler | Runs automatically once a day at the time you set in `config.py` |
| CLI flags | `--now`, `--schedule`, `--source`, `--dest` for scripting |

---

## 🖥️ Quick Start (Windows)

### Step 1 — Install Python

Download from https://www.python.org/downloads/ (3.11 or newer).  
☑️ Check **"Add Python to PATH"** during installation.

### Step 2 — Download / clone this project

```
git clone https://github.com/YOUR_USERNAME/smart-file-organizer.git
cd smart-file-organizer
```

### Step 3 — Run setup (first time only)

Double-click **`setup.bat`**  
— or —  
Open PowerShell in the project folder and run:

```powershell
.\setup.bat
```

This creates a virtual environment and installs all dependencies automatically.

### Step 4 — Run the organizer

**Option A — Double-click `run.bat`** (easiest)

**Option B — PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
python organizer.py
```

**Option C — Run immediately without the menu:**
```powershell
python organizer.py --now
```

**Option D — Custom source folder:**
```powershell
python organizer.py --now --source "C:\Users\You\Desktop"
```

---

## ⚙️ Configuration

Edit **`config.py`** to customize behavior:

```python
# Which folder to organize
SOURCE_FOLDER = Path.home() / "Downloads"   # change to any folder

# Where organized files go
DESTINATION_FOLDER = Path("organized_files")

# Daily scheduler time (24-hour)
SCHEDULE_TIME = "10:00"

# Add/remove file extensions per category
FILE_CATEGORIES = { ... }
```

---

## 📁 Project Structure

```
smart-file-organizer/
├── organizer.py         ← Main script
├── config.py            ← All settings
├── requirements.txt     ← Python dependencies
├── setup.bat            ← One-time Windows setup
├── run.bat              ← Quick daily launcher
├── .gitignore
├── logs/                ← Created on first run
│   └── organizer.log
├── reports/             ← Created on first run
│   └── report_YYYYMMDD_HHMMSS.json
└── organized_files/     ← Created on first run
    ├── Images/
    ├── Videos/
    ├── PDFs/
    ├── Documents/
    ├── Music/
    ├── Archives/
    ├── Code/
    ├── Executables/
    └── Others/
```

---

## 🔧 PowerShell Execution Policy (if `Activate.ps1` is blocked)

Run this once in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📋 CLI Reference

```
python organizer.py [options]

  (no options)           Interactive menu
  --now                  Run organizer immediately
  --schedule             Start daily scheduler (Ctrl+C to stop)
  --source <path>        Override source folder
  --dest <path>          Override destination folder
```

---

## 📦 Dependencies

- [`schedule`](https://pypi.org/project/schedule/) — task scheduling
- [`plyer`](https://pypi.org/project/plyer/) — desktop notifications (optional, gracefully skipped if unavailable)

---

## 📄 License

MIT
