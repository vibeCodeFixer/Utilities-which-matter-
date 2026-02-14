# Organization Guide

Complete guide for organizing extracted Google Takeout files.

## Quick Start

```bash
python scripts/organize_videos.py
```

The script will:
1. Ask for source and destination folders
2. Let you set blanket policies for duplicates
3. Find all .mp4 and .mov files
4. Move/copy them with hash verification
5. Show detailed statistics

## What It Does

Finds ALL videos in nested folders and moves them to one location:

**Before:**
```
E:\Takeout\
├── Google Photos\
│   ├── 2020\January\video1.mp4
│   ├── 2020\February\video2.mov
│   └── 2021\video3.mp4
└── Drive\
    └── Videos\video4.mov
```

**After:**
```
E:\My Videos\
├── video1.mp4
├── video2.mov
├── video3.mp4
└── video4.mov
```

## Usage

### Basic Usage

```bash
python scripts/organize_videos.py
```

You'll be asked:
1. **Source folder**: Where to search for videos
2. **Destination folder**: Where to move videos
3. **Mode**: Move (remove from source) or Copy (keep in source)
4. **Blanket policies**: How to handle duplicates

### Setting Blanket Policies

#### Policy 1: For IDENTICAL files (same hash)

```
======================================================================
📋 When files have SAME HASH (identical content):
======================================================================
  [1] Skip - Don't move (recommended, saves space)
  [2] Rename - Keep both (file and file_copy1)
  [3] Overwrite - Replace destination with source
  [4] Ask me each time
======================================================================

Your choice for IDENTICAL files [1/2/3/4]: 1
```

#### Policy 2: For DIFFERENT files (different hash)

```
======================================================================
📋 When files have DIFFERENT HASH (different content):
======================================================================
  [1] Rename - Keep both (recommended, preserves both versions)
  [2] Skip - Don't move source
  [3] Overwrite - Replace destination with source
  [4] Ask me each time
======================================================================

Your choice for DIFFERENT files [1/2/3/4]: 1
```

## Recommended Policies

### Scenario 1: Merging Backups (Most Common)

**Goal**: Skip duplicates, keep different versions

```
Identical files (same hash):   [1] SKIP
Different files (diff hash):   [1] RENAME
```

**Result:**
- Identical files → Skipped (saves space)
- Different files → Both kept (vacation.mp4 and vacation_copy1.mp4)

### Scenario 2: Keep Everything

**Goal**: Don't lose anything

```
Identical files (same hash):   [2] RENAME
Different files (diff hash):   [1] RENAME
```

**Result:**
- All files kept (even exact duplicates)

### Scenario 3: Manual Control

**Goal**: Decide for each file

```
Identical files (same hash):   [4] ASK
Different files (diff hash):   [4] ASK
```

**Result:**
- Script asks for each duplicate

## Features

### Hash-Based Duplicate Detection

When duplicate filenames are found:

```
[5/25] vacation.mp4
      ⚠️  Duplicate filename: vacation.mp4
      Size - Source: 234.56 MB | Dest: 234.56 MB
      🔍 Calculating hashes...
         Calculating hash: vacation.mp4 (234.56 MB)... ✓
         Calculating hash: vacation.mp4 (234.56 MB)... ✓
      
      🔐 HASH COMPARISON:
         Source: 5d41402abc4b2a76b9719d911017c592
         Dest:   5d41402abc4b2a76b9719d911017c592
      ✅ IDENTICAL (hashes match)
      → Policy: SKIP
      ⏭️  Skipped
```

### Supported File Types

Default extensions:
- `.mp4`
- `.mov`
- `.MP4` (uppercase)
- `.MOV` (uppercase)

To add more formats, edit `scripts/organize_videos.py`:

```python
# Line ~23
self.video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.MP4', '.MOV']
```

### Statistics

```
======================================================================
📊 FINAL SUMMARY
======================================================================
🔍 Found: 142 video files
✅ Processed: 118 files
⏭️  Skipped: 18 files (identical hash)
📝 Renamed: 6 files (different hash, same name)

⏱️  Time taken: 3.2 minutes
📂 Files in: E:\My Videos
======================================================================
```

## Examples

### Example 1: Move All Videos

```bash
$ python scripts/organize_videos.py

📁 Enter SOURCE folder path: E:\Takeout\Google Photos
📂 Enter DESTINATION folder path: E:\My Videos

Mode:
  [1] MOVE - Remove from source
  [2] COPY - Keep in source
Select mode [1/2]: 1

# Set policies...
Identical: [1] SKIP
Different: [1] RENAME

# Processing...
✓ Processed 142 videos
```

### Example 2: Copy (Keep Originals)

```bash
$ python scripts/organize_videos.py

📁 Enter SOURCE folder path: E:\Takeout
📂 Enter DESTINATION folder path: F:\Video Backup

Mode: [2] COPY

# Processing...
✓ Copied 142 videos (originals kept in source)
```

### Example 3: Handle Duplicates Manually

```bash
# Set policies to ASK
Identical: [4] ASK
Different: [4] ASK

# For each duplicate:
      ======================================================
      DECISION NEEDED: vacation.mp4
      ======================================================
      Status: Files are IDENTICAL (same hash)
        [s] Skip - Don't move
        [r] Rename - Keep both
        [o] Overwrite - Replace destination
      ======================================================
      
Your choice [s/r/o]: s
```

## Understanding Hashes

### What is a Hash?

A unique "fingerprint" of a file. Even tiny changes create different hashes.

```
File 1: "Hello"     → Hash: 8b1a9953c4611296a827abf8c47804d7
File 2: "Hello!"    → Hash: 952d2c56d0485958336747bcdd98590d
                              ↑ Completely different!
```

### Hash Comparison

**Same hash = Identical files:**
```
Source: 5d41402abc4b2a76b9719d911017c592
Dest:   5d41402abc4b2a76b9719d911017c592
✅ Files are exactly the same
```

**Different hash = Different files:**
```
Source: 5d41402abc4b2a76b9719d911017c592
Dest:   a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
⚠️ Different files with same name!
```

## Time Estimates

**For 150 videos (~50 GB):**
- Finding files: 10-30 seconds
- Moving/copying: 2-5 minutes
- Hash calculation (per duplicate): 1-10 seconds each

**Total time depends on:**
- Number of duplicates
- File sizes
- Disk speed (SSD vs HDD)

## Troubleshooting

### "No video files found"
- **Check**: Source path is correct
- **Check**: Folder contains .mp4 or .mov files
- **Tip**: Add more extensions if needed

### Hash calculation is slow
- **Normal**: Large files (1GB+) take 10-20 seconds
- **Faster**: Use SSD instead of HDD
- **Alternative**: Use size-based comparison (edit script to skip hash)

### "Permission denied"
- **Windows**: Run as Administrator
- **Linux/Mac**: Check file permissions
- **Fix**: Choose different destination folder

### Duplicates not detected
- **Cause**: Files have different names
- **Note**: Script only compares files with same filename
- **Solution**: Use dedicated duplicate finder for different names

## Advanced Customization

### Add More File Types

Edit `scripts/organize_videos.py`:

```python
# Line ~23
self.video_extensions = [
    '.mp4', '.mov',   # Video
    '.jpg', '.png',   # Images
    '.pdf', '.docx'   # Documents
]
```

### Skip Hash Calculation

For faster processing (less accurate):

```python
# In compare_files method, comment out hash calculation
# Line ~85-95
# source_hash = self.calculate_hash(source_path)
# dest_hash = self.calculate_hash(dest_path)
# Just compare sizes instead
```

### Change Hash Algorithm

```python
# Line ~40
hash_md5 = hashlib.md5()  # Change to sha256 for more security
# hash_sha256 = hashlib.sha256()
```

## Tips

1. **Test First**: Use COPY mode first to test
2. **Small Batch**: Test on one subfolder first
3. **Verify After**: Check destination folder
4. **Blanket Policies**: Save time with automatic decisions
5. **Free Space**: Ensure enough space in destination

## Next Steps

After organizing:
1. Review organized files in destination
2. Delete empty source folders if desired
3. Repeat for other file types (photos, documents)
4. Back up your organized collection

## Creating Custom Organizers

You can create similar scripts for other file types:

```python
# For photos
self.photo_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.heic']

# For documents
self.doc_extensions = ['.pdf', '.docx', '.xlsx', '.txt']

# For music
self.music_extensions = ['.mp3', '.flac', '.wav', '.m4a']
```

Just copy and modify `scripts/organize_videos.py`!
