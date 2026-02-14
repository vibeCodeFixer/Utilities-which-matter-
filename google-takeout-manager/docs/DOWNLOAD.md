# Download Guide

Complete guide for downloading Google Takeout files.

## Quick Start

```bash
# Download all files (indices 0-90)
python scripts/download_takeout.py 0 90

# Or download in batches (recommended)
python scripts/download_takeout.py 0 29
python scripts/download_takeout.py 30 59
python scripts/download_takeout.py 60 90
```

## How It Works

The script:
1. Opens Chrome browser
2. Navigates to your Google Takeout page
3. Waits for you to login
4. Clicks download buttons for selected range
5. Monitors downloads with 2-second delay between clicks

## Usage

### Interactive Mode

```bash
python scripts/download_takeout.py
```

You'll be prompted for:
- Start index (0-90)
- End index (0-90)
- Confirmation

### Command Line Mode

```bash
python scripts/download_takeout.py START END
```

Examples:
```bash
# Download all 91 files
python scripts/download_takeout.py 0 90

# Download first 30
python scripts/download_takeout.py 0 29

# Download single file
python scripts/download_takeout.py 5 5
```

## Index Explanation

Google Takeout uses **0-based indexing**:

| URL Index | Filename | Display |
|-----------|----------|---------|
| i=0 | ...-000.zip | Part 1 of 91 |
| i=1 | ...-001.zip | Part 2 of 91 |
| i=2 | ...-002.zip | Part 3 of 91 |
| ... | ... | ... |
| i=90 | ...-090.zip | Part 91 of 91 |

## Download Strategies

### Strategy 1: All at Once (Fast)

```bash
python scripts/download_takeout.py 0 90
```

**Pros:**
- Fastest if it works
- Single session

**Cons:**
- May overwhelm browser
- Higher chance of failures

**Recommended for:**
- Fast internet (100+ Mbps)
- Powerful computer (16GB+ RAM)
- Stable connection

### Strategy 2: Three Batches (Recommended)

```bash
# Batch 1
python scripts/download_takeout.py 0 29

# Batch 2
python scripts/download_takeout.py 30 59

# Batch 3
python scripts/download_takeout.py 60 90
```

**Pros:**
- More stable
- Easy to resume
- Works on most systems

**Cons:**
- Requires 3 sessions
- Slightly slower

**Recommended for:**
- Most users
- First-time downloaders
- Reliability over speed

### Strategy 3: Small Batches (Safest)

```bash
# Download 10 at a time
python scripts/download_takeout.py 0 9
python scripts/download_takeout.py 10 19
# ... continue
```

**Pros:**
- Very stable
- Easy to track
- Low system requirements

**Cons:**
- Many sessions
- Slower overall

**Recommended for:**
- Slow/unstable internet
- Older computers
- Testing first

## Features

### Automatic Duplicate Cleanup

The script automatically removes Chrome's duplicate downloads:
```
✓ vacation.mp4.crdownload (kept)
🗑️ vacation (1).mp4.crdownload (deleted)
🗑️ vacation (2).mp4.crdownload (deleted)
```

### Existing File Detection

Before downloading, checks if file exists:
```
Found existing file: takeout-...-025.zip
  [s] Skip - Don't download
  [r] Re-download - Delete and download again
  [S] Skip ALL existing files
  [R] Re-download ALL existing files
```

### Filename Pattern Recognition

Detects Google Takeout patterns:
```
takeout-20260110T151158Z-3-000.zip
takeout-20260110T151158Z-3-001.zip
...
```

## Progress Display

```
[25/91] 🎯 Download part 26 of 91
      🖱️  Clicking button... ✓
      ⏳ Waiting for download to start... ✓ Started
      📥 Downloading... ........ ✓ Complete (2,147,483,648 bytes)
      📊 Progress: 25 downloaded, 0 skipped | Est. remaining: 45.2 min
```

## Configuration

### Change Download Delay

Edit `scripts/download_takeout.py`:

```python
# Line ~195 (inside click_all_in_range method)
time.sleep(2)  # Change to 5 for 5-second delay
```

### Change Download Folder

Edit `scripts/download_takeout.py`:

```python
# Line ~20
DOWNLOAD_DIR = "google_takeout_downloads"  # Change this
```

### Change Archive Information

```python
# Lines ~17-19
ARCHIVE_ID = "your-archive-id"
USER_ID = "your-user-id"
TOTAL_PARTS = 91  # Your number of parts
```

## Troubleshooting

### Chrome Opens But Nothing Happens
- **Fix**: Make sure you're logged into Google
- **Fix**: Check you're on the correct Takeout page
- **Fix**: Press ENTER in terminal when ready

### "Allow Multiple Downloads" Popup
- **Fix**: Click "Allow" when Chrome asks
- This only appears once per session

### Downloads Don't Start
- **Fix**: Check Chrome downloads (Ctrl+J or Cmd+J)
- **Fix**: Verify download folder has write permissions
- **Fix**: Check disk space

### Script Crashes
- **Fix**: Reduce batch size (download fewer files)
- **Fix**: Increase delay between clicks
- **Fix**: Close other Chrome windows

### Some Files Missing After Download
- **Fix**: Re-run script with same range
- Script automatically skips existing files
- Check Chrome downloads for failures

## After Downloading

### Verify File Count

```bash
# Windows
dir google_takeout_downloads\*.zip | find /c ".zip"

# Linux/Mac
ls google_takeout_downloads/*.zip | wc -l
```

Should show your range size (e.g., 30 for 0-29).

### Check for Incomplete Downloads

```bash
# Check for .crdownload files
ls google_takeout_downloads/*.crdownload
```

Should be empty!

### Next Step

Proceed to [EXTRACTION.md](EXTRACTION.md) to extract your files.

## Tips

1. **Test First**: Download 2-3 files first to verify it works
2. **Stable Connection**: Use wired ethernet if possible
3. **Keep Computer Awake**: Disable sleep mode
4. **Monitor Downloads**: Check Chrome (Ctrl+J) periodically
5. **Free Disk Space**: Ensure you have enough space

## Performance

**Typical timing for 91 files (~200 GB):**
- Fast internet (100+ Mbps): 3-5 hours
- Medium internet (50 Mbps): 6-10 hours
- Slow internet (10 Mbps): 20+ hours

**Recommended:** Download overnight or during work hours.
