# Release Guide for Space Frontier

This document explains how to create releases for Space Frontier.

## 🎯 Quick Overview

**Current Setup:**
- ✅ Automated releases via GitHub Actions (when you push tags)
- ✅ Manual release scripts (for local testing)
- ✅ Automatic zip file creation
- ✅ Release notes generation

---

## 🤖 Option 1: Automated Releases (RECOMMENDED)

### How It Works

1. Push a version tag to GitHub
2. GitHub Actions automatically:
   - Creates a release package
   - Zips all necessary files
   - Creates a GitHub Release
   - Attaches the zip file
   - Generates release notes

### Steps to Create a Release

```bash
# 1. Make sure all changes are committed and pushed
git add .
git commit -m "Your changes"
git push

# 2. Create and push a version tag
git tag v2.0.0
git push origin v2.0.0

# That's it! GitHub Actions handles the rest.
```

### Check Release Status

1. Go to: `https://github.com/DarenFranks/Space-Frontier/actions`
2. Look for "Create Release" workflow
3. Once complete, release appears at: `https://github.com/DarenFranks/Space-Frontier/releases`

---

## 🔧 Option 2: Manual Releases

### Windows

```batch
REM Run the release script
create_release.bat

REM This creates: releases\Space-Frontier-v2.0.0\
REM Then manually zip and upload to GitHub
```

### Linux/Mac

```bash
# Run the release script
chmod +x create_release.sh
./create_release.sh

# This creates: releases/Space-Frontier-v2.0.0.zip
# Then manually upload to GitHub
```

### Manual GitHub Release

1. Go to: `https://github.com/DarenFranks/Space-Frontier/releases/new`
2. Fill in:
   - **Tag**: v2.0.0 (create new tag)
   - **Title**: Space Frontier 2.0.0
   - **Description**: Release notes
3. Attach the zip file
4. Click "Publish release"

---

## 📋 Version Numbering

Use **Semantic Versioning**: `MAJOR.MINOR.PATCH`

### Examples:
- `v2.0.0` - Major release (big features)
- `v2.1.0` - Minor release (new features)
- `v2.1.1` - Patch release (bug fixes)

### When to Bump:

**MAJOR (x.0.0):**
- Complete system overhauls
- Breaking changes
- Major feature additions

**MINOR (2.x.0):**
- New features
- New locations/factions
- Non-breaking enhancements

**PATCH (2.1.x):**
- Bug fixes
- Performance improvements
- Minor tweaks

---

## 🎬 Example Release Workflow

### Scenario: You've added new features

```bash
# 1. Update version in relevant files (if any)
# (Currently version is only in README.md)

# 2. Commit all changes
git add .
git commit -m "Add new faction territory with 10 locations"
git push

# 3. Decide version (new features = minor bump)
# Current: v2.0.0 → New: v2.1.0

# 4. Create and push tag
git tag v2.1.0 -m "Added new faction territory"
git push origin v2.1.0

# 5. Wait ~2 minutes for GitHub Actions

# 6. Check release page
# https://github.com/DarenFranks/Space-Frontier/releases
```

Done! Users can now download Space-Frontier-v2.1.0.zip

---

## 📦 What Gets Included in Releases

### Python Files (all .py):
- gui.py
- game_engine.py
- player.py
- vessels.py
- combat.py
- economy.py
- manufacturing.py
- factions.py
- travel_system.py
- (all other .py files)

### Documentation (all .md and .txt):
- README.md
- INSTALL.md
- QUICKSTART.md
- GALAXY_EXPANSION.md
- (all other docs)

### Launch Scripts:
- play.bat (Windows)
- play.sh (Linux/Mac)
- install.bat
- install.sh

### Requirements:
- requirements.txt

### Generated:
- RELEASE_NOTES.txt (auto-created)

---

## 🔍 Verifying Releases

### After Creating a Release:

1. **Check GitHub Releases Page**
   - Should show new version
   - Zip file attached
   - Release notes visible

2. **Download and Test**
   ```bash
   # Download the zip
   # Extract it
   cd Space-Frontier-v2.1.0
   pip install -r requirements.txt
   python gui.py
   ```

3. **Verify Contents**
   - All .py files present
   - Documentation included
   - Scripts executable
   - Game launches correctly

---

## ⚠️ Important Notes

### DO create releases for:
- ✅ Major feature completions
- ✅ Significant bug fix batches
- ✅ Milestone achievements
- ✅ User-requested builds

### DON'T create releases for:
- ❌ Every single commit
- ❌ Work-in-progress features
- ❌ Experimental changes
- ❌ Documentation-only updates

### Best Practices:
- 📝 Write clear release notes
- 🏷️ Use consistent version tags
- 📅 Space releases reasonably (not daily)
- ✅ Test before tagging
- 📊 Track major versions in README.md

---

## 🆘 Troubleshooting

### "Release workflow failed"
- Check Actions tab for error details
- Usually missing files or wrong paths
- Verify all files exist before tagging

### "Zip file is too large"
- Remove __pycache__ folders
- Remove save_game.yaml
- Check for unnecessary files

### "Release not appearing"
- Wait 2-3 minutes for workflow
- Check Actions tab for progress
- Verify tag was pushed correctly

### "Can't download release"
- Ensure release isn't draft
- Check file uploaded successfully
- Try different browser

---

## 📈 Release History Tracking

Keep track of releases in a CHANGELOG.md (optional):

```markdown
# Changelog

## [2.1.0] - 2024-XX-XX
### Added
- New faction territory
- 10 additional locations
- Enhanced travel system

### Fixed
- Combat balance issues
- UI display bugs

## [2.0.0] - 2024-XX-XX
### Added
- Complete game rewrite
- 56 locations
- Faction loyalty system
```

---

## 🎯 Quick Reference

| Action | Command |
|--------|---------|
| Create minor release | `git tag v2.1.0 && git push origin v2.1.0` |
| Create major release | `git tag v3.0.0 && git push origin v3.0.0` |
| Delete tag (oops!) | `git tag -d v2.1.0 && git push origin :refs/tags/v2.1.0` |
| List all tags | `git tag -l` |
| View release | Visit releases page |

---

**Questions?** Check GitHub Actions logs or test with manual release scripts first!
