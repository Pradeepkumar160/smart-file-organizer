from pathlib import Path

# ============================================================
# Smart File Organizer - Configuration
# Edit these paths to match your system
# ============================================================

# Folder to organize (source). Defaults to your Downloads folder.
SOURCE_FOLDER = Path.home() / "Downloads"

# Where organized files will go. Relative to where you run the script.
DESTINATION_FOLDER = Path("organized_files")

# Time for daily auto-scheduler (24-hour format "HH:MM")
SCHEDULE_TIME = "10:00"

# File type mapping — add/remove extensions as needed
FILE_CATEGORIES = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".ico", ".tiff"],
    "Videos":    [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm"],
    "PDFs":      [".pdf"],
    "Documents": [".docx", ".doc", ".txt", ".pptx", ".ppt", ".xlsx", ".xls", ".odt", ".rtf", ".csv"],
    "Music":     [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives":  [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code":      [".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".html", ".css", ".json",
                  ".xml", ".sh", ".bat", ".ps1", ".rb", ".go", ".rs", ".php"],
    "Executables": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
}
