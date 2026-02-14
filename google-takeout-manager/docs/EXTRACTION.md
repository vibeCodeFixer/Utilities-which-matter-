# Extraction Guide

Complete guide for extracting and merging Google Takeout ZIP files.

## Quick Start

```bash
python scripts/extract_takeout.py
```

The script will:
1. Find all ZIP files
2. Show a preview
3. Ask for confirmation
4. Extract and merge all files
5. Handle duplicates intelligently

## How It Works

Google Takeout splits your data across multiple ZIPs with duplicate folder names:

**Before extraction:**
```
takeout-...-018.zip
  └── Takeout/Google Photos/AlbumA/photo1.jpg

takeout-...-019.zip
  └── Takeout/Google Photos/AlbumA/photo2.jpg  ← Same folder!
```

**After extraction:**
```
E:\Takeout/
  └── Google Photos/
      └── AlbumA/
          ├── photo1.jpg  ← From ZIP 18
          └── photo2.jpg  ← From ZIP 19
```

## Configuration

Edit `scripts/extract_takeout.py`:

```python
# Lines ~15-17
ZIP_FOLDER = "google_takeout_downloads"  # Where your ZIPs are
OUTPUT_FOLDER = r"E:\Takeout"           # Where to extract (Windows)
# Or: OUTPUT_FOLDER = "/home/user/Takeout"  # Linux/Mac

# Line ~22
DUPLICATE_MODE = "skip"  # How to handle duplicate files
```

## Duplicate Handling Modes

### skip (Recommended)
- Skips files if same size
- **Fast**: No hash calculation
- **Use when**: Merging same Takeout export

### rename
- Keeps all files with _copy suffix
- **Fast**: No hash calculation
- **Use when**: Want to keep everything

### compare
- Compares file hashes
- **Slow**: Calculates MD5 for each duplicate
- **Use when**: Need 100% accuracy

### overwrite
- Replaces existing files
- **Fast**: No checks
- **Use when**: Starting fresh (be careful!)

## Usage Examples

### Example 1: Basic Extraction

```bash
python scripts/extract_takeout.py
```

Output:
```
======================================================================
📦 Google Takeout ZIP Extractor & Merger - ADVANCED
======================================================================

📁 ZIP folder: google_takeout_downloads
📂 Output folder: E:\Takeout
🔧 Duplicate mode: skip

🔍 Finding ZIP files...
✓ Found 91 ZIP file(s)

======================================================================
ZIP Files to Process:
======================================================================
[ 1] takeout-20260110T151158Z-3-000.zip (2048.0 MB)
[ 2] takeout-20260110T151158Z-3-001.zip (2048.0 MB)
...
[91] takeout-20260110T151158Z-3-090.zip (1456.0 MB)
======================================================================

Proceed with extraction? [Y/n]: y

[1/91] 📦 Processing: takeout-...-000.zip
   Files: 1523
   Mode: skip
   [████████████████████████████████████████] 100.0% (1523/1523)
   ✅ Extracted: 1523 files

[2/91] 📦 Processing: takeout-...-001.zip
   Files: 1498
   Mode: skip
   [████████████████████████████████████████] 100.0% (1498/1498)
   ✅ Extracted: 1456 files
   ⏭️  Skipped: 42 duplicates

...

======================================================================
📊 EXTRACTION COMPLETE!
======================================================================
✅ ZIPs processed: 91/91
📄 Files extracted: 138,542
⏭️  Files skipped: 1,234 (duplicates)
💾 Total extracted: 195.50 GB
⏱️  Time taken: 45.3 minutes

📂 All files extracted to: E:\Takeout
======================================================================
```

### Example 2: Keep All Files (with Renaming)

```python
# Edit scripts/extract_takeout.py
DUPLICATE_MODE = "rename"
```

Then run:
```bash
python scripts/extract_takeout.py
```

Result:
```
photo.jpg
photo_copy1.jpg
photo_copy2.jpg
```

### Example 3: Hash Comparison

```python
# Edit scripts/extract_takeout.py
DUPLICATE_MODE = "compare"
```

Slower but most accurate. Only keeps files with different content.

## Features

### Progress Bars

Shows real-time progress:
```
[████████████████████████████████████████] 100.0% (1523/1523)
```

### Smart Duplicate Detection

**By Size (skip/rename mode):**
```
Source: 2,147,483,648 bytes
Dest:   2,147,483,648 bytes
→ Skipped (same size)
```

**By Hash (compare mode):**
```
Source hash: 5d41402abc4b2a76b9719d911017c592
Dest hash:   5d41402abc4b2a76b9719d911017c592
→ Skipped (identical content)
```

### Error Handling

If errors occur:
```
⚠️  Errors: 3
   - Error extracting file1.jpg: Permission denied
   - Error extracting file2.mp4: Disk full
   - Error extracting file3.png: Corrupted ZIP
```

## Time Estimates

**For 91 ZIPs (~200 GB):**

| Mode | Time | Disk Type |
|------|------|-----------|
| skip | 30-45 min | SSD |
| skip | 60-90 min | HDD |
| rename | 30-45 min | SSD |
| compare | 2-4 hours | SSD |

**Factors affecting speed:**
- Disk type (SSD vs HDD)
- File count (more files = slower)
- Duplicate mode (compare is slowest)

## Disk Space Requirements

You need approximately **2x the ZIP size**:
- ZIPs: 200 GB
- Extracted: 200 GB
- **Total needed: 400 GB**

After extraction, you can delete ZIPs to free up space.

## Troubleshooting

### "No ZIP files found"
- **Check**: `ZIP_FOLDER` path is correct
- **Check**: Files are in the specified folder
- **Check**: Files have .zip extension

### "Permission denied"
- **Windows**: Run as Administrator
- **Linux/Mac**: Check folder permissions
- **Fix**: Choose a different output folder

### "Disk full" errors
- **Check**: Enough free space (2x ZIP size)
- **Fix**: Free up space or use different drive
- **Tip**: Extract in batches if needed

### Extraction is very slow
- **Cause**: Using HDD instead of SSD
- **Cause**: Many small files
- **Cause**: Using "compare" mode
- **Fix**: Use SSD for extraction
- **Fix**: Use "skip" mode instead

### Some files missing
- **Check**: Error messages in output
- **Check**: Extraction completed successfully
- **Fix**: Re-run script (skips existing files)

## After Extraction

### Verify File Count

```bash
# Count all files
# Windows
dir E:\Takeout /s /b | find /c ":"

# Linux/Mac
find /path/to/Takeout -type f | wc -l
```

### Check Total Size

```bash
# Windows
dir E:\Takeout

# Linux/Mac
du -sh /path/to/Takeout
```

### Delete ZIP Files (Optional)

After verifying extraction:

```bash
# Windows
del google_takeout_downloads\*.zip

# Linux/Mac
rm google_takeout_downloads/*.zip
```

**WARNING**: Only delete ZIPs after verifying all files extracted correctly!

## Next Steps

After extraction:
1. Verify all files are present
2. Proceed to [ORGANIZATION.md](ORGANIZATION.md)
3. Organize files by type (videos, photos, etc.)
4. Delete ZIPs to free up space

## Tips

1. **Use SSD**: 10x faster than HDD for extraction
2. **Skip Mode**: Best for most users (fast and reliable)
3. **Verify First**: Check a few extracted files before deleting ZIPs
4. **Free Space**: Ensure 2x ZIP size available
5. **Interrupt Safe**: Can stop and resume (skips existing files)
