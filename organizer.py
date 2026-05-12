"""
Smart File Organizer
====================
Automatically organizes files into categorized folders,
detects duplicates, generates reports, and supports scheduling.

Usage:
    python organizer.py          -> interactive menu
    python organizer.py --now    -> run immediately (no prompt)
    python organizer.py --schedule -> start scheduler
    python organizer.py --source "C:/Users/You/Desktop" -> custom source
"""

import os
import sys
import argparse
import shutil
import hashlib
import json
import logging
import time
from pathlib import Path
from datetime import datetime

import schedule

try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except Exception:
    NOTIFICATIONS_AVAILABLE = False

from config import SOURCE_FOLDER, DESTINATION_FOLDER, FILE_CATEGORIES, SCHEDULE_TIME

# ============================================================
# Logging
# ============================================================
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    handlers=[
        logging.FileHandler("logs/organizer.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),       # also print to console
    ],
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ============================================================
# Folder Setup
# ============================================================
def create_folders(destination: Path):
    destination.mkdir(parents=True, exist_ok=True)
    for category in FILE_CATEGORIES:
        (destination / category).mkdir(parents=True, exist_ok=True)
    (destination / "Others").mkdir(parents=True, exist_ok=True)
    log.info("Category folders ready inside: %s", destination)


# ============================================================
# Hashing & Duplicate Detection
# ============================================================
def get_file_hash(file_path: Path) -> str | None:
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except OSError as e:
        log.error("Cannot hash %s: %s", file_path.name, e)
        return None


def detect_duplicates(files: list[Path]) -> set[Path]:
    """Return the set of files that are duplicates (same hash seen before)."""
    seen: dict[str, Path] = {}
    duplicates: set[Path] = set()
    for file in files:
        h = get_file_hash(file)
        if h is None:
            continue
        if h in seen:
            duplicates.add(file)
            log.info("Duplicate detected: %s  (same as %s)", file.name, seen[h].name)
        else:
            seen[h] = file
    return duplicates


# ============================================================
# Categorization
# ============================================================
def categorize_file(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


# ============================================================
# Safe Move (handle name collisions)
# ============================================================
def safe_destination(destination: Path) -> Path:
    """If destination exists, append _1, _2 … until unique."""
    if not destination.exists():
        return destination
    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 1
    while True:
        new_dest = parent / f"{stem}_{counter}{suffix}"
        if not new_dest.exists():
            return new_dest
        counter += 1


# ============================================================
# Core Organizer
# ============================================================
def organize_files(source: Path = SOURCE_FOLDER, destination: Path = DESTINATION_FOLDER):
    if not source.exists():
        log.error("Source folder does not exist: %s", source)
        print(f"\n❌  Source folder not found: {source}")
        print("    Edit SOURCE_FOLDER in config.py to point to an existing folder.")
        return

    log.info("=" * 60)
    log.info("Organizer started  |  source: %s", source)
    start_time = time.time()

    create_folders(destination)

    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "source": str(source),
        "destination": str(destination),
        "files_moved": [],
        "duplicates_skipped": [],
        "errors": [],
    }

    # Collect only top-level files (not sub-directories)
    files = [f for f in source.iterdir() if f.is_file()]
    if not files:
        log.info("No files found in source folder.")
        print("ℹ️  No files found to organize.")
        return

    log.info("Found %d file(s) to process.", len(files))
    duplicates = detect_duplicates(files)

    moved = 0
    skipped = 0
    errors = 0

    for file in files:
        if file in duplicates:
            log.info("Skipping duplicate: %s", file.name)
            report["duplicates_skipped"].append(file.name)
            skipped += 1
            continue

        try:
            category = categorize_file(file.suffix)
            dest = safe_destination(destination / category / file.name)
            shutil.move(str(file), str(dest))
            log.info("Moved  %-40s  →  %s/", file.name, category)
            report["files_moved"].append({"file": file.name, "category": category, "destination": str(dest)})
            moved += 1
        except Exception as e:
            log.error("Error moving %s: %s", file.name, e)
            report["errors"].append({"file": file.name, "error": str(e)})
            errors += 1

    elapsed = round(time.time() - start_time, 2)
    report["execution_time_seconds"] = elapsed
    report["summary"] = {"moved": moved, "duplicates_skipped": skipped, "errors": errors}

    # Save report
    Path("reports").mkdir(exist_ok=True)
    report_path = Path(f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    log.info("Report saved → %s", report_path)
    log.info("Done in %.2fs  |  moved=%d  skipped=%d  errors=%d", elapsed, moved, skipped, errors)

    # Summary banner
    print("\n" + "=" * 50)
    print("  ✅  Smart File Organizer — Done!")
    print(f"      Moved:    {moved} file(s)")
    print(f"      Skipped:  {skipped} duplicate(s)")
    print(f"      Errors:   {errors}")
    print(f"      Time:     {elapsed}s")
    print(f"      Report:   {report_path}")
    print("=" * 50 + "\n")

    # Desktop notification (optional, may not work on all systems)
    if NOTIFICATIONS_AVAILABLE:
        try:
            notification.notify(
                title="Smart File Organizer",
                message=f"Done! Moved {moved} files in {elapsed}s",
                timeout=5,
            )
        except Exception as e:
            log.debug("Notification skipped: %s", e)


# ============================================================
# Scheduler
# ============================================================
def run_scheduler(source: Path = SOURCE_FOLDER, destination: Path = DESTINATION_FOLDER):
    schedule.every().day.at(SCHEDULE_TIME).do(organize_files, source=source, destination=destination)
    print(f"\n🕐  Scheduler active — will run daily at {SCHEDULE_TIME}")
    print("    Press Ctrl+C to stop.\n")
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")


# ============================================================
# CLI Entry Point
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Smart File Organizer — organize your files automatically"
    )
    parser.add_argument("--now", action="store_true", help="Run organizer immediately")
    parser.add_argument("--schedule", action="store_true", help="Start daily scheduler")
    parser.add_argument("--source", type=str, help="Override source folder path")
    parser.add_argument("--dest", type=str, help="Override destination folder path")
    args = parser.parse_args()

    source = Path(args.source) if args.source else SOURCE_FOLDER
    dest = Path(args.dest) if args.dest else DESTINATION_FOLDER

    if args.now:
        organize_files(source, dest)
        return

    if args.schedule:
        run_scheduler(source, dest)
        return

    # Interactive menu
    print("\n====================================")
    print("   Smart File Organizer")
    print("====================================")
    print(f"  Source:  {source}")
    print(f"  Dest:    {dest}")
    print("------------------------------------")
    print("  1. Run Organizer Now")
    print("  2. Start Daily Scheduler")
    print("  3. Exit")
    print("====================================")

    choice = input("Choose option (1/2/3): ").strip()
    if choice == "1":
        organize_files(source, dest)
    elif choice == "2":
        run_scheduler(source, dest)
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice. Run again and enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
