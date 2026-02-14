# Google Takeout Manager

Complete toolkit for downloading, extracting, and organizing your Google Takeout data.

## 🎯 What This Does

This toolkit helps you:
1. **Download** all 91 parts of your Google Takeout archive automatically
2. **Extract** and merge all ZIP files into one organized folder structure
3. **Organize** files by type (e.g., move all videos to one folder)

## 🚀 Quick Start

### 1. Download Google Takeout Files

```bash
# Install dependencies
pip install selenium

# Download files in parallel with range selection
python scripts/download_takeout.py

# Example: Download first 30 files
python scripts/download_takeout.py 0 29
```

### 2. Extract and Merge ZIP Files

```bash
# Extract all ZIPs and merge folders automatically
python scripts/extract_takeout.py
```

### 3. Organize Files

```bash
# Move all videos to one folder
python scripts/organize_videos.py
```

## 📦 Features

### Download Manager
- ✅ Parallel or sequential downloads
- ✅ Range selection (download specific parts)
- ✅ Duplicate detection and cleanup
- ✅ Auto-retry and resume capability
- ✅ Cross-platform (Windows, Linux, macOS)

### Extraction Manager
- ✅ Extracts all ZIPs automatically
- ✅ Merges duplicate folders intelligently
- ✅ Multiple duplicate handling modes
- ✅ Progress tracking with progress bars
- ✅ Error handling and reporting

### File Organizer
- ✅ Find files by type across all folders
- ✅ Hash-based duplicate detection
- ✅ Blanket policies (set rules once)
- ✅ Move or copy options
- ✅ Detailed statistics

## 📋 Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver (for downloads)
- ~200+ GB free disk space (for typical Takeout)

## 🛠️ Installation

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/google-takeout-manager.git
cd google-takeout-manager

# Install dependencies
pip install -r requirements.txt

# Install ChromeDriver
# Ubuntu/Debian:
sudo apt install chromium-chromedriver

# macOS:
brew install chromedriver

# Windows:
# Download from https://chromedriver.chromium.org/
```

### Detailed Setup

See [docs/SETUP.md](docs/SETUP.md) for platform-specific installation instructions.

## 📖 Documentation

- **[Setup Guide](docs/SETUP.md)** - Installation for Windows, Linux, macOS
- **[Download Guide](docs/DOWNLOAD.md)** - Downloading Google Takeout files
- **[Extraction Guide](docs/EXTRACTION.md)** - Extracting and merging ZIPs
- **[Organization Guide](docs/ORGANIZATION.md)** - Organizing extracted files
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🎬 Usage Examples

### Example 1: Download Everything in Batches

```bash
# Download in 3 batches (recommended)
python scripts/download_takeout.py 0 29   # Batch 1: 30 files
python scripts/download_takeout.py 30 59  # Batch 2: 30 files
python scripts/download_takeout.py 60 90  # Batch 3: 31 files
```

### Example 2: Complete Workflow

```bash
# Step 1: Download all files
python scripts/download_takeout.py 0 90

# Step 2: Extract and merge
python scripts/extract_takeout.py

# Step 3: Organize videos
python scripts/organize_videos.py
```

### Example 3: Resume Interrupted Download

```bash
# Script automatically skips already downloaded files
python scripts/download_takeout.py 0 90
```

## 🗂️ Repository Structure

```
google-takeout-manager/
├── scripts/
│   ├── download_takeout.py       # Download Takeout files
│   ├── extract_takeout.py        # Extract and merge ZIPs
│   └── organize_videos.py        # Organize files by type
├── docs/
│   ├── SETUP.md                  # Installation guide
│   ├── DOWNLOAD.md               # Download documentation
│   ├── EXTRACTION.md             # Extraction documentation
│   ├── ORGANIZATION.md           # Organization documentation
│   └── TROUBLESHOOTING.md        # Common issues
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore file
├── LICENSE                       # MIT License
└── README.md                     # This file
```

## ⚙️ Configuration

Edit the scripts to customize:

```python
# In download_takeout.py
ARCHIVE_ID = "your-archive-id"
USER_ID = "your-user-id"
DOWNLOAD_DIR = "google_takeout_downloads"

# In extract_takeout.py
ZIP_FOLDER = "google_takeout_downloads"
OUTPUT_FOLDER = r"E:\Takeout"  # or "/path/to/Takeout" on Linux/Mac
DUPLICATE_MODE = "skip"  # "skip", "rename", "compare", "overwrite"

# In organize_videos.py
# Set policies when prompted at runtime
```

## 🎯 Common Use Cases

### Use Case 1: First Time Download
1. Download all files: `python scripts/download_takeout.py 0 90`
2. Extract: `python scripts/extract_takeout.py`
3. Organize: `python scripts/organize_videos.py`

### Use Case 2: Resume After Interruption
1. Re-run download (skips existing): `python scripts/download_takeout.py 0 90`
2. Continue extraction: `python scripts/extract_takeout.py`

### Use Case 3: Download in Batches
1. Batch 1: `python scripts/download_takeout.py 0 29`
2. Batch 2: `python scripts/download_takeout.py 30 59`
3. Batch 3: `python scripts/download_takeout.py 60 90`
4. Extract all: `python scripts/extract_takeout.py`

## 🔧 Advanced Features

### Download Manager
- **Range Selection**: Download specific file ranges
- **Parallel Downloads**: Click all buttons at once
- **Duplicate Cleanup**: Auto-removes Chrome's duplicate .crdownload files
- **Pattern Recognition**: Detects Google Takeout filename patterns

### Extraction Manager
- **Smart Merging**: Combines folders with same name
- **Duplicate Modes**: Skip, rename, compare hashes, or overwrite
- **Progress Bars**: Real-time extraction progress
- **Resume Capable**: Skip already extracted files

### File Organizer
- **Hash Comparison**: MD5 hash verification for duplicates
- **Blanket Policies**: Set rules once for all files
- **Flexible Actions**: Skip, rename, or overwrite
- **Statistics**: Detailed reports on operations

## 📊 Performance

**Typical 91-file Takeout (~200 GB):**
- Download time: 3-12 hours (depends on internet speed)
- Extraction time: 30-90 minutes (depends on disk speed)
- Organization time: 5-30 minutes (depends on file count)

**Tips for best performance:**
- Use SSD for extraction (10x faster than HDD)
- Stable internet connection for downloads
- Download in batches for reliability

## 🛡️ Safety Features

- ✅ Never overwrites without confirmation
- ✅ Duplicate detection prevents data loss
- ✅ Resume capability for interrupted operations
- ✅ Detailed logs and error reporting
- ✅ Dry-run mode for testing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for personal use to manage your own Google Takeout data. Make sure you have the rights to download and process the data you're working with.

## 🙏 Acknowledgments

- Google Takeout for providing data export
- Selenium project for browser automation
- Community contributors and testers

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/google-takeout-manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/google-takeout-manager/discussions)
- **Documentation**: [docs/](docs/)

## 🗺️ Roadmap

- [ ] GUI version
- [ ] Multi-threaded extraction
- [ ] Cloud storage integration
- [ ] More file type organizers (photos, documents)
- [ ] Automatic cleanup of empty folders

---

**Happy organizing your Google Takeout data! 🎉**
