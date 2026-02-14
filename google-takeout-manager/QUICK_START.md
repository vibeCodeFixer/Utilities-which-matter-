# Quick Reference Guide

## 🚀 Installation (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install ChromeDriver
# Ubuntu: sudo apt install chromium-chromedriver
# macOS: brew install chromedriver
# Windows: Download from https://chromedriver.chromium.org/

# 3. Configure your archive ID
# Edit scripts/download_takeout.py lines 17-19
```

## 📥 Download (One Command)

```bash
# Download all files
python scripts/download_takeout.py 0 90

# Or in batches (recommended)
python scripts/download_takeout.py 0 29
python scripts/download_takeout.py 30 59
python scripts/download_takeout.py 60 90
```

## 📦 Extract (One Command)

```bash
# Edit OUTPUT_FOLDER in scripts/extract_takeout.py first
python scripts/extract_takeout.py
```

## 🎬 Organize (One Command)

```bash
python scripts/organize_videos.py
```

## 📋 Complete Workflow

```bash
# 1. Download
python scripts/download_takeout.py 0 90

# 2. Extract
python scripts/extract_takeout.py

# 3. Organize
python scripts/organize_videos.py
```

## ⚙️ Configuration Cheat Sheet

### download_takeout.py
```python
ARCHIVE_ID = "6dba9630-cc98-4507-aa5f-6376563d25c0"  # Get from download URL
USER_ID = "113508548453534889343"                    # Get from download URL
DOWNLOAD_DIR = "google_takeout_downloads"            # Where to save ZIPs
```

### extract_takeout.py
```python
ZIP_FOLDER = "google_takeout_downloads"  # Where ZIPs are
OUTPUT_FOLDER = r"E:\Takeout"           # Where to extract (Windows)
DUPLICATE_MODE = "skip"                  # skip/rename/compare/overwrite
```

### organize_videos.py
```python
# Set policies when prompted:
# Identical files: [1] SKIP (recommended)
# Different files: [1] RENAME (recommended)
```

## 🎯 Recommended Settings

**For Most Users:**
- Download: Batches of 30 files
- Extract: DUPLICATE_MODE = "skip"
- Organize: SKIP identical, RENAME different

**For Safety:**
- Download: COPY mode first
- Extract: DUPLICATE_MODE = "rename"
- Organize: ASK for each decision

**For Speed:**
- Download: All at once
- Extract: DUPLICATE_MODE = "skip"
- Organize: Blanket policies

## 📊 Time Estimates

| Task | Typical Time |
|------|--------------|
| Download 91 files | 3-12 hours |
| Extract 91 ZIPs | 30-90 min |
| Organize 1000 videos | 5-15 min |

## 🔧 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| ChromeDriver error | `pip install webdriver-manager` |
| Permission denied | Run as admin / use sudo |
| Disk full | Need 2x ZIP size |
| Very slow | Use SSD, close other programs |
| No files found | Check paths in scripts |

## 📖 Full Documentation

- [SETUP.md](docs/SETUP.md) - Detailed installation
- [DOWNLOAD.md](docs/DOWNLOAD.md) - Download guide
- [EXTRACTION.md](docs/EXTRACTION.md) - Extraction guide
- [ORGANIZATION.md](docs/ORGANIZATION.md) - Organization guide
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues

## 💡 Pro Tips

1. **Test first** with small batch (0-9)
2. **Use SSD** for extraction (10x faster)
3. **Set blanket policies** to save time
4. **Keep ZIPs** until verified
5. **Download overnight** for best results

## 🎯 Common Commands

```bash
# Check what you downloaded
ls google_takeout_downloads/*.zip | wc -l

# Verify extraction
find Takeout -type f | wc -l

# Get help
python scripts/download_takeout.py --help
```

## 📁 File Structure

```
google-takeout-manager/
├── scripts/
│   ├── download_takeout.py    # Download files
│   ├── extract_takeout.py     # Extract ZIPs
│   └── organize_videos.py     # Organize files
├── docs/                       # Full documentation
├── requirements.txt            # Dependencies
└── README.md                   # Main readme
```

## 🚨 Important Notes

- **Indices are 0-based**: 91 files = indices 0-90
- **Need 2x space**: ZIPs + extracted files
- **Keep browser open**: During downloads
- **Verify before deleting**: Check extraction before removing ZIPs

---

**That's it! Simple as 1-2-3: Download → Extract → Organize** 🎉
