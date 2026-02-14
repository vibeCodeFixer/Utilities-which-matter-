# Troubleshooting Guide

Common issues and solutions for Google Takeout Manager.

## Installation Issues

### "python is not recognized" (Windows)

**Problem**: Python not in PATH

**Solutions**:
1. Reinstall Python with "Add Python to PATH" checked
2. Or add manually:
   - Right-click "This PC" → Properties
   - Advanced → Environment Variables
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3x\`

### "pip is not recognized"

**Problem**: pip not in PATH

**Solutions**:
```bash
# Use python -m pip instead
python -m pip install -r requirements.txt

# Or add Scripts folder to PATH
C:\Users\YourName\AppData\Local\Programs\Python\Python3x\Scripts\
```

### "selenium not found"

**Problem**: Selenium not installed

**Solutions**:
```bash
pip install selenium
# or
pip3 install selenium --break-system-packages
```

### ChromeDriver version mismatch

**Problem**: ChromeDriver doesn't match Chrome version

**Solutions**:
```bash
# Option 1: Use webdriver-manager (automatic)
pip install webdriver-manager

# Option 2: Download correct version
# 1. Check Chrome version: chrome://settings/help
# 2. Download from: https://chromedriver.chromium.org/
# 3. Place in PATH or project folder
```

## Download Issues

### Chrome opens but nothing happens

**Problem**: Not logged in or wrong page

**Solutions**:
1. Make sure you're logged into Google
2. Verify the Takeout page is correct
3. Wait for page to fully load
4. Press ENTER in terminal when ready

### "Allow multiple downloads" keeps appearing

**Problem**: Chrome security setting

**Solutions**:
1. Click "Allow" when prompted
2. Check "Remember my choice" if available
3. This only happens once per session

### Downloads don't start

**Problem**: Various causes

**Solutions**:
1. Check Chrome downloads (Ctrl+J or Cmd+J)
2. Verify download folder has write permissions
3. Check disk space available
4. Try reducing download range

### Script crashes with "stale element" error

**Problem**: DOM changed after finding elements

**Solutions**:
- This is already fixed in latest version
- Script re-finds elements before clicking
- If still occurs, reduce batch size

### Some files not downloading

**Problem**: Network issues or failures

**Solutions**:
1. Re-run script with same range
2. Script automatically skips completed files
3. Check Chrome downloads for errors
4. Try smaller batches

### Downloads are very slow

**Problem**: Network or server limitations

**Solutions**:
1. This is normal for large files
2. Be patient (91 files can take hours)
3. Download during off-peak hours
4. Consider downloading in batches

## Extraction Issues

### "No ZIP files found"

**Problem**: Incorrect path or no ZIPs

**Solutions**:
1. Verify `ZIP_FOLDER` path in script
2. Check files are in the specified folder
3. Ensure files have .zip extension
4. Use absolute paths

Example:
```python
# Windows
ZIP_FOLDER = r"C:\Users\YourName\google_takeout_downloads"

# Linux/Mac
ZIP_FOLDER = "/home/username/google_takeout_downloads"
```

### "Permission denied"

**Problem**: No write access

**Solutions**:
1. **Windows**: Run Command Prompt as Administrator
2. **Linux/Mac**: Use sudo or check permissions
3. Choose a different output folder
4. Check folder isn't read-only

### "Disk full" errors

**Problem**: Not enough space

**Solutions**:
1. Check free space: Need 2x ZIP size
2. Free up space on destination drive
3. Use a different drive
4. Extract in batches (manual)

### Extraction is very slow

**Problem**: Slow disk or many files

**Solutions**:
1. Use SSD instead of HDD (10x faster)
2. Use "skip" mode instead of "compare"
3. Close other programs
4. Be patient (45+ minutes is normal)

### Files appear corrupted after extraction

**Problem**: Bad ZIP or extraction error

**Solutions**:
1. Check if original ZIP is corrupted
2. Re-download that specific ZIP
3. Try extracting manually with WinRAR/7-Zip
4. Check extraction logs for errors

## Organization Issues

### "No video files found"

**Problem**: Wrong path or no videos

**Solutions**:
1. Verify source folder path
2. Check folder actually contains .mp4/.mov files
3. Try adding more extensions
4. Check subfolder searching is working

### Hash calculation is very slow

**Problem**: Normal for large files

**Solutions**:
1. Be patient (1GB file = 10-15 seconds)
2. Use SSD for faster calculation
3. For quicker results, edit script to skip hash
4. Use blanket policies to avoid repeated asks

### Duplicate files not detected

**Problem**: Different filenames

**Solutions**:
1. Script only compares files with **same filename**
2. For different names, use dedicated duplicate finder
3. Files with different names are not considered duplicates

### Script hangs during hash calculation

**Problem**: Very large file or disk issue

**Solutions**:
1. Wait (10GB file can take 2-3 minutes)
2. Check disk isn't failing
3. Close other programs
4. Try with smaller files first

## Dependency Issues

### urllib3 version conflict

**Problem**: Selenium requires newer urllib3

**Solutions**:
```bash
pip install --upgrade urllib3
pip install --upgrade selenium
```

### Multiple Python versions conflict

**Problem**: Wrong Python version used

**Solutions**:
```bash
# Use specific version
python3 -m pip install -r requirements.txt
python3 scripts/download_takeout.py

# Or create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### ChromeDriver platform mismatch

**Problem**: Wrong ChromeDriver for OS

**Solutions**:
1. Download correct version for your OS
2. Windows: chromedriver.exe
3. Linux/Mac: chromedriver (no extension)

## Performance Issues

### Computer is very slow during processing

**Problem**: High resource usage

**Solutions**:
1. Close other programs
2. Reduce batch size for downloads
3. Use lower duplicate mode for extraction
4. Restart computer before starting

### Downloads/extraction taking too long

**Problem**: Various causes

**Expected times:**
- Download 91 files: 3-12 hours
- Extract 91 ZIPs: 30-90 minutes
- Organize 1000 videos: 5-15 minutes

**Solutions**:
1. Use wired connection for downloads
2. Use SSD for extraction
3. Be patient - this is normal!

## Platform-Specific Issues

### Windows: "Access Denied"

**Solutions**:
1. Run Command Prompt as Administrator
2. Check antivirus isn't blocking
3. Disable Windows Defender temporarily
4. Use a different folder

### Linux: "Permission denied"

**Solutions**:
```bash
# Fix permissions
chmod +x scripts/*.py

# Or use sudo
sudo python3 scripts/extract_takeout.py

# Better: change ownership
sudo chown -R $USER:$USER google_takeout_downloads/
```

### macOS: "chromedriver cannot be opened"

**Solutions**:
```bash
# Allow unsigned drivers
xattr -d com.apple.quarantine /path/to/chromedriver

# Or use webdriver-manager
pip install webdriver-manager
```

## Error Messages

### "Index out of range"

**Problem**: Trying to download non-existent index

**Solutions**:
1. Check TOTAL_PARTS in script
2. Maximum index is TOTAL_PARTS - 1
3. For 91 files, use 0-90 (not 0-91)

### "Connection refused" or "Network error"

**Problem**: Internet connection issue

**Solutions**:
1. Check internet connection
2. Restart router
3. Try again later
4. Check if Google is blocking

### "Element not found"

**Problem**: Page structure changed or not loaded

**Solutions**:
1. Wait longer before pressing ENTER
2. Refresh page and try again
3. Check you're on correct page
4. Google might have changed layout

## Getting Help

If your issue isn't listed here:

1. **Check Documentation**:
   - [SETUP.md](SETUP.md)
   - [DOWNLOAD.md](DOWNLOAD.md)
   - [EXTRACTION.md](EXTRACTION.md)
   - [ORGANIZATION.md](ORGANIZATION.md)

2. **Search Issues**:
   - GitHub Issues page
   - Existing solutions

3. **Create New Issue**:
   - Describe the problem
   - Include error messages
   - Specify OS and Python version
   - Share relevant logs

4. **Provide Details**:
   ```
   - OS: Windows 10 / Ubuntu 22.04 / macOS 13
   - Python version: python --version
   - Selenium version: pip show selenium
   - Chrome version: chrome://settings/help
   - Error message: [copy full error]
   ```

## Prevention Tips

1. **Test First**: Try with small batch before full run
2. **Backup**: Keep original ZIPs until verified
3. **Space**: Ensure 2-3x space needed
4. **Stable**: Use wired connection
5. **Updates**: Keep Python and dependencies updated

## Quick Diagnostics

Run these to check your setup:

```bash
# Check Python
python --version

# Check Selenium
python -c "import selenium; print(selenium.__version__)"

# Check disk space
# Windows: dir
# Linux/Mac: df -h

# Test ChromeDriver
chromedriver --version
```

All should run without errors!
