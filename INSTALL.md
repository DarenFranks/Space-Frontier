# Installation Guide - Void Dominion

Quick and easy installation instructions for all platforms.

---

## For Recipients (Installing the Game)

### Step 1: Extract the Files

**Windows**:
- Right-click on `VoidDominion.zip` → "Extract All"
- Choose a location (e.g., Desktop or Documents)

**macOS**:
- Double-click `VoidDominion.zip` to extract

**Linux**:
```bash
unzip VoidDominion.zip
cd VoidDominion
```

### Step 2: Install Python (if needed)

**Check if you have Python**:
```bash
python3 --version
```

If you see `Python 3.7` or higher, skip to Step 3!

**If Python is not installed**:

**Windows**:
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 (or latest)
3. Run installer
4. ✅ **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"

**macOS**:
```bash
# If you have Homebrew installed:
brew install python3

# Or download from python.org
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

**Linux (Fedora/Red Hat)**:
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

### Step 3: Install Game Dependencies

Open a terminal/command prompt in the game folder and run:

```bash
pip3 install -r requirements.txt
```

Or manually install:
```bash
pip3 install pyyaml
```

That's it! Only one dependency needed.

### Step 4: Launch the Game!

**Graphical Interface** (Recommended):
```bash
python3 gui.py
```

**Command-Line Interface**:
```bash
python3 main.py
```

**Using the Launcher** (if included):
```bash
python3 launch.py
```

---

## Troubleshooting

### "python3: command not found"

**Windows**: Use `python` instead of `python3`:
```bash
python gui.py
```

**Linux/Mac**: Install Python (see Step 2 above)

### "No module named 'tkinter'"

**Linux**:
```bash
sudo apt install python3-tk      # Ubuntu/Debian
sudo dnf install python3-tkinter # Fedora
```

**macOS**: Reinstall Python from python.org (tkinter included)

**Windows**: Reinstall Python and make sure "tcl/tk" is checked

### "No module named 'yaml'"

Install the dependency:
```bash
pip3 install pyyaml
```

### "Permission denied" (Linux/Mac)

Make the script executable:
```bash
chmod +x gui.py
python3 gui.py
```

### Game window is too big/small

Edit `gui.py` line 40:
```python
self.root.geometry("1400x900")  # Change these numbers
```

---

## For Developers (Running from Source)

### Clone or Download

If you have the source code:

```bash
git clone <repository-url>
cd VoidDominion
```

Or just download/extract the files.

### Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Run the Game

**GUI version**:
```bash
python3 gui.py
```

**CLI version**:
```bash
python3 main.py
```

### Development Mode

Install in editable mode (optional):
```bash
pip3 install -e .
```

---

## System Requirements

**Minimum**:
- Python 3.7 or higher
- 50 MB disk space
- 128 MB RAM
- 1400x900 screen resolution
- Windows 7 / macOS 10.12 / any Linux

**Recommended**:
- Python 3.10 or higher
- 100 MB disk space
- 256 MB RAM
- 1920x1080 screen resolution

---

## What Gets Installed?

**Python packages**:
- `pyyaml==6.0.1` - For save game files

**Game files**:
- 22 Python source files (~1.5 MB)
- Documentation files (.md)
- Configuration (requirements.txt)

**No other dependencies!** The game uses only Python's standard library.

---

## Uninstalling

To remove the game:

1. Delete the game folder
2. (Optional) Uninstall pyyaml:
   ```bash
   pip3 uninstall pyyaml
   ```

That's it! No registry entries, no system files.

---

## Platform-Specific Notes

### Windows

- Use `python` instead of `python3`
- May need to add Python to PATH
- Antivirus might scan on first run (it's safe!)

### macOS

- Python 3 might need to be installed (not included by default)
- Use Terminal for command-line
- May need to allow in Security & Privacy settings

### Linux

- Most distros include Python 3
- Need to install python3-tk separately
- Works on all major distros (Ubuntu, Fedora, Debian, Arch, etc.)

---

## Quick Start After Installation

1. **Start a new game**
   - Enter your commander name
   - Choose "New Game"

2. **Learn the basics**
   - Read QUICKSTART.md
   - Try the tutorial contracts
   - Explore the interface

3. **Get help**
   - In-game: Type `help` (CLI) or check menus (GUI)
   - Documentation: See markdown files
   - Troubleshooting: TROUBLESHOOTING.md

---

## Advanced Installation

### Virtual Environment (Recommended for developers)

Create an isolated Python environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run game
python gui.py
```

### System-Wide Installation

Install for all users (requires admin):

```bash
sudo pip3 install pyyaml  # Linux/Mac
```

---

## Support

**Having issues?**
1. Check TROUBLESHOOTING.md
2. Check Python version: `python3 --version`
3. Reinstall dependencies: `pip3 install --force-reinstall pyyaml`
4. Try CLI version if GUI doesn't work: `python3 main.py`

**Still stuck?**
- Check the GitHub issues
- Create a new issue with error details

---

**Ready to play?** Launch with `python3 gui.py` and enjoy! 🚀
