# Void Dominion - USB Drive Installation Guide

## Overview
This guide explains how to run Void Dominion directly from a USB drive on any computer with Python installed.

---

## Requirements

### Required Software:
- **Python 3.10 or higher** (must be installed on the computer)
- USB drive with at least **100 MB** free space

### Checking Python Installation:
Open a terminal/command prompt and type:
```bash
python3 --version
```
or on Windows:
```bash
python --version
```

If Python is not installed, download it from: https://www.python.org/downloads/

---

## Installation Steps

### 1. Copy Game to USB Drive

Copy the entire `Space_Frontier` folder to your USB drive:

```
USB Drive Root/
└── Space_Frontier/
    ├── *.py (all game files)
    ├── play.sh (Linux/Mac launcher)
    ├── play.bat (Windows launcher)
    ├── requirements.txt
    └── README.md
```

### 2. Running the Game

#### On Linux/Mac:

```bash
# Navigate to the game folder on USB
cd /path/to/usb/Space_Frontier

# Make launcher executable (first time only)
chmod +x play.sh

# Run the game
./play.sh
```

Or run directly:
```bash
cd /path/to/usb/Space_Frontier
python3 gui.py
```

#### On Windows:

Double-click `play.bat` in the Space_Frontier folder

Or via Command Prompt:
```bash
cd E:\Space_Frontier
python gui.py
```
(Replace `E:` with your USB drive letter)

---

## Portable Save Files

All save files are stored in the game directory, making them fully portable:

- `savegame.json` - Your game save
- Save files travel with the USB drive automatically
- Works on any computer without setup

---

## Troubleshooting

### "Python not found" Error
**Problem**: Python is not installed on the computer
**Solution**: Install Python 3.10+ from python.org

### "tkinter not found" Error
**Problem**: Python's tkinter library is missing
**Linux Solution**:
```bash
sudo apt-get install python3-tk
```
**Mac Solution**: Included with standard Python installation
**Windows Solution**: Included with standard Python installation

### Game Runs Slowly
**Problem**: USB drive has slow read/write speeds
**Solution**:
- Use a USB 3.0 drive for better performance
- Consider copying game to computer's local drive temporarily

### Save File Issues
**Problem**: Cannot save game
**Solution**:
- Ensure USB drive is not write-protected
- Check that you have write permissions on the USB drive

---

## First Time Setup on New Computer

1. **Plug in USB drive**
2. **Open terminal/command prompt**
3. **Navigate to game folder**:
   ```bash
   cd /path/to/usb/Space_Frontier
   ```
4. **Run the game**:
   ```bash
   python3 gui.py
   ```

That's it! No installation needed.

---

## Performance Tips

### For Best Performance:
1. Use a **USB 3.0** or **USB-C** drive
2. Close other applications while playing
3. If USB is slow, temporarily copy to local drive:
   ```bash
   # Copy to local drive
   cp -r /usb/Space_Frontier ~/Space_Frontier

   # Play from local drive
   cd ~/Space_Frontier
   python3 gui.py

   # Copy saves back to USB when done
   cp ~/Space_Frontier/savegame.json /usb/Space_Frontier/
   ```

---

## Quick Reference

| Action | Linux/Mac | Windows |
|--------|-----------|---------|
| Launch Game | `./play.sh` | Double-click `play.bat` |
| Manual Launch | `python3 gui.py` | `python gui.py` |
| Check Python | `python3 --version` | `python --version` |
| Game Saves | `./savegame.json` | `.\savegame.json` |

---

## Features That Work from USB

✓ All game features fully functional
✓ Save/Load games
✓ Multiple save files
✓ Full graphics and sound
✓ All game systems (combat, trading, manufacturing, etc.)
✓ Portable between computers
✓ No installation required on host computer

---

## Security Notes

- Game only reads/writes to its own directory
- No system modifications
- No admin/root privileges needed
- Safe to run on any computer with Python
- All data stays on USB drive

---

## Support

If you encounter issues:
1. Verify Python 3.10+ is installed
2. Check USB drive is not write-protected
3. Ensure you have sufficient USB space (~100 MB)
4. Try running from local drive temporarily

---

## Game Controls

See `README.md` for full game documentation and controls.

Enjoy Void Dominion on the go! 🚀
