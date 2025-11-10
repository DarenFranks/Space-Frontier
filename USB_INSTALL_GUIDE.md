# Void Dominion - USB Drive Installation Guide

## Overview
This guide will help you install and run Void Dominion from a USB drive on any computer running Windows, Linux, or macOS.

---

## What You'll Need

- USB drive (minimum 100 MB free space)
- Computer with Python 3.6 or higher installed
- Internet connection (for initial Python installation only)

---

## Part 1: Preparing the USB Drive

### Step 1: Copy Game Files to USB

1. **Insert your USB drive** into your computer
2. **Copy the entire Space_Frontier folder** to your USB drive
3. Your USB drive should now contain:
   ```
   USB:/
   └── Space_Frontier/
       ├── *.py (all Python game files)
       ├── requirements.txt
       ├── install.sh (Linux/Mac)
       ├── play.sh (Linux/Mac)
       ├── launch.py (cross-platform)
       ├── main.py
       ├── README.md
       ├── QUICKSTART.md
       └── INSTALL.md
   ```

4. **Safely eject your USB drive**

---

## Part 2: Installing on a New Computer

### For Windows Users

#### Step 1: Install Python (if not already installed)

1. Go to https://www.python.org/downloads/
2. Download Python 3.6 or higher
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Complete the installation

#### Step 2: Install Game Dependencies

1. Insert your USB drive
2. Open Command Prompt (press Win+R, type `cmd`, press Enter)
3. Navigate to the game folder:
   ```cmd
   cd /d E:\Space_Frontier
   ```
   (Replace `E:` with your USB drive letter)

4. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

#### Step 3: Run the Game

**Option A - GUI Mode (Recommended):**
```cmd
python launch.py
```

**Option B - CLI Mode:**
```cmd
python main.py
```

**Option C - Direct GUI:**
```cmd
python gui.py
```

---

### For Linux Users

#### Step 1: Install Python (usually pre-installed)

Most Linux distributions come with Python 3. Check your version:
```bash
python3 --version
```

If not installed, use your package manager:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk

# Fedora/RHEL
sudo dnf install python3 python3-pip python3-tkinter

# Arch
sudo pacman -S python python-pip tk
```

#### Step 2: Install Game Dependencies

1. Insert your USB drive
2. Open terminal
3. Navigate to the game folder:
   ```bash
   cd /media/yourusername/USBNAME/Space_Frontier
   ```
   (Replace `/media/yourusername/USBNAME` with your actual USB mount point)

4. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   Or manually install:
   ```bash
   pip3 install -r requirements.txt
   ```

#### Step 3: Run the Game

**Quick Launch:**
```bash
chmod +x play.sh
./play.sh
```

**Or manually:**
```bash
python3 launch.py
```

---

### For macOS Users

#### Step 1: Install Python (if not already installed)

1. Install Homebrew if you don't have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Python:
   ```bash
   brew install python3 python-tk
   ```

#### Step 2: Install Game Dependencies

1. Insert your USB drive
2. Open Terminal
3. Navigate to the game folder:
   ```bash
   cd /Volumes/USBNAME/Space_Frontier
   ```
   (Replace `USBNAME` with your USB drive name)

4. Run installation:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   Or manually:
   ```bash
   pip3 install -r requirements.txt
   ```

#### Step 3: Run the Game

**Quick Launch:**
```bash
chmod +x play.sh
./play.sh
```

**Or manually:**
```bash
python3 launch.py
```

---

## Part 3: Portable Play

### Running from USB Without Installation

If the target computer already has Python and dependencies installed, you can run directly from USB:

**Windows:**
```cmd
cd /d E:\Space_Frontier
python launch.py
```

**Linux/Mac:**
```bash
cd /path/to/usb/Space_Frontier
python3 launch.py
```

### Save Files

Your game progress is saved in `save_game.yaml` in the game folder. This means:

- ✅ Your saves travel with the USB drive
- ✅ You can play on different computers with the same character
- ✅ Each USB drive can have different save games

---

## Part 4: Troubleshooting

### "Python not found" Error

**Windows:**
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Python39\python.exe launch.py`

**Linux/Mac:**
- Try `python3` instead of `python`
- Check if Python is installed: `which python3`

### "No module named 'yaml'" Error

You need to install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pyyaml
```

### GUI Doesn't Open

Make sure tkinter is installed:

**Windows:** Included with Python

**Linux:**
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
```

**Mac:**
```bash
brew install python-tk
```

### USB Drive Letter Changes (Windows)

Create a batch file `play.bat` in the game folder:
```batch
@echo off
cd /d %~dp0
python launch.py
pause
```

Then just double-click `play.bat` to run the game!

### Permission Denied (Linux/Mac)

Make scripts executable:
```bash
chmod +x install.sh play.sh launch.py
```

---

## Part 5: Multiple Computers Setup

### Best Practice for Multiple PCs

1. **First Time on Each Computer:**
   - Install Python (if needed)
   - Run `install.sh` / `pip install -r requirements.txt`
   - This only needs to be done once per computer

2. **Every Time You Play:**
   - Insert USB
   - Navigate to game folder
   - Run `./play.sh` or `python launch.py`

3. **Your saves go with you!**
   - The `save_game.yaml` file is on your USB
   - Your progress is preserved across computers

---

## Part 6: Quick Reference Card

### Essential Commands

| Platform | Navigate to USB | Install Deps | Play Game |
|----------|----------------|--------------|-----------|
| Windows  | `cd /d E:\Space_Frontier` | `pip install -r requirements.txt` | `python launch.py` |
| Linux    | `cd /media/user/USB/Space_Frontier` | `./install.sh` | `./play.sh` |
| macOS    | `cd /Volumes/USB/Space_Frontier` | `./install.sh` | `./play.sh` |

### Game Modes

- **GUI Mode:** `python launch.py` or `python gui.py`
- **CLI Mode:** `python main.py`
- **Help:** `python main.py --help`

---

## Part 7: Sharing Your USB

Want to share the game with friends?

1. Copy the entire `Space_Frontier` folder to their USB
2. Have them follow Part 2 of this guide
3. They'll have their own separate save file
4. You can compare progress and trade tips!

---

## Part 8: Updating the Game

If you receive an updated version:

1. **Backup your save:** Copy `save_game.yaml` somewhere safe
2. **Replace game files:** Copy new Python files to USB
3. **Restore your save:** Copy `save_game.yaml` back
4. **Run the game:** Your progress is preserved!

---

## Need More Help?

- **Quick Start Guide:** See `QUICKSTART.md` for how to play
- **Installation Help:** See `INSTALL.md` for detailed setup
- **Game Manual:** See `README.md` for game features

---

## Summary Checklist

- [ ] USB drive ready with game files
- [ ] Python 3.6+ installed on target computer
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Game launches successfully
- [ ] Save file created after first play

**Happy exploring, Commander!** 🚀

---

**Void Dominion** - A space exploration and trading game
Version 1.0 | Portable USB Edition
