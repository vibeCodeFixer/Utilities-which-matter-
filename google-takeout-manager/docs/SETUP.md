# Setup Guide

Complete installation instructions for Windows, Linux, and macOS.

## Requirements

- Python 3.7 or higher
- Chrome browser
- ChromeDriver
- 200+ GB free disk space (typical Takeout size)
- Stable internet connection

## Installation

### Windows

#### 1. Install Python

1. Download Python from https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: `python --version` in Command Prompt

#### 2. Install Dependencies

```cmd
pip install -r requirements.txt
```

#### 3. Install ChromeDriver

**Option A: Automatic (Recommended)**
```cmd
pip install webdriver-manager
```

**Option B: Manual**
1. Check Chrome version: `chrome://settings/help`
2. Download matching ChromeDriver from https://chromedriver.chromium.org/
3. Extract `chromedriver.exe`
4. Place in `C:\Windows\` or add to PATH

### Linux (Ubuntu/Debian)

#### 1. Install Python

```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### 2. Install Dependencies

```bash
pip3 install -r requirements.txt --break-system-packages
```

#### 3. Install ChromeDriver

```bash
sudo apt install chromium-browser chromium-chromedriver
```

### macOS

#### 1. Install Python

```bash
# Using Homebrew (install from https://brew.sh if needed)
brew install python
```

#### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

#### 3. Install ChromeDriver

```bash
brew install chromedriver
```

## Verification

Test your installation:

```bash
# Check Python
python --version  # or python3 --version

# Check Selenium
python -c "import selenium; print(selenium.__version__)"

# Check ChromeDriver
chromedriver --version
```

All commands should run without errors!

## Configuration

### Update Your Archive Information

Edit `scripts/download_takeout.py`:

```python
# Line ~25-27
ARCHIVE_ID = "your-archive-id-here"
USER_ID = "your-user-id-here"
TOTAL_PARTS = 91  # Your number of parts
```

**How to find these values:**
1. Go to your Google Takeout download page
2. Right-click on first download button → "Copy link address"
3. URL will be: `https://takeout.google.com/takeout/download?j=ARCHIVE_ID&i=0&user=USER_ID`
4. Extract `ARCHIVE_ID` and `USER_ID` from the URL

### Configure Extraction Path

Edit `scripts/extract_takeout.py`:

```python
# Line ~15-17
ZIP_FOLDER = "google_takeout_downloads"  # Where downloads are
OUTPUT_FOLDER = r"E:\Takeout"           # Where to extract (Windows)
# Or: OUTPUT_FOLDER = "/home/user/Takeout"  # Linux/Mac
```

## Troubleshooting

### "pip is not recognized" (Windows)
- Reinstall Python with "Add to PATH" checked
- Or add manually: `C:\Users\YourName\AppData\Local\Programs\Python\Python3x\Scripts`

### "selenium not found"
```bash
pip install selenium
# or
pip3 install selenium --break-system-packages
```

### ChromeDriver version mismatch
- Make sure ChromeDriver version matches your Chrome version
- Use webdriver-manager for automatic version handling

### Permission errors (Linux/Mac)
- Use `sudo` for system-wide installation
- Or use `--user` flag: `pip install --user -r requirements.txt`

## Next Steps

After installation:
1. Read [DOWNLOAD.md](DOWNLOAD.md) for downloading Google Takeout
2. Read [EXTRACTION.md](EXTRACTION.md) for extracting files
3. Read [ORGANIZATION.md](ORGANIZATION.md) for organizing files

## Getting Help

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Open an issue on GitHub
- Review existing documentation
