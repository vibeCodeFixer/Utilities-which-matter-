#!/usr/bin/env python3
"""
Google Takeout ZIP Extractor and Merger - ADVANCED
Smart duplicate handling, progress bars, verification
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

# Configuration
ZIP_FOLDER = "google_takeout_downloads"  # Folder containing your ZIP files
OUTPUT_FOLDER = r"E:\Takeout"  # Where to extract (Windows path)

# Duplicate handling mode:
# "skip" - Skip if file exists with same size
# "rename" - Rename duplicates (file_copy1.jpg, file_copy2.jpg)
# "compare" - Compare file hashes, only extract if different
# "overwrite" - Overwrite existing files (not recommended)
DUPLICATE_MODE = "skip"

class TakeoutExtractor:
    def __init__(self, zip_folder, output_folder, duplicate_mode="skip"):
        self.zip_folder = Path(zip_folder)
        self.output_folder = Path(output_folder)
        self.duplicate_mode = duplicate_mode
        self.stats = {
            'zips_processed': 0,
            'files_extracted': 0,
            'files_skipped': 0,
            'files_renamed': 0,
            'total_size': 0,
            'errors': []
        }
    
    def find_zip_files(self):
        """Find all ZIP files in the folder"""
        zip_files = sorted(self.zip_folder.glob("*.zip"))
        return zip_files
    
    def get_file_hash(self, filepath):
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def get_zip_member_hash(self, zf, member):
        """Calculate MD5 hash of a ZIP member"""
        hash_md5 = hashlib.md5()
        with zf.open(member) as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def handle_duplicate(self, target_path, zf, member):
        """Handle duplicate file based on mode"""
        if self.duplicate_mode == "skip":
            # Check size
            if target_path.stat().st_size == member.file_size:
                return "skipped", target_path
            else:
                # Different size, rename
                return self.get_renamed_path(target_path, zf, member)
        
        elif self.duplicate_mode == "rename":
            return self.get_renamed_path(target_path, zf, member)
        
        elif self.duplicate_mode == "compare":
            # Compare hashes
            existing_hash = self.get_file_hash(target_path)
            new_hash = self.get_zip_member_hash(zf, member)
            
            if existing_hash == new_hash:
                return "skipped", target_path
            else:
                # Different content, rename
                return self.get_renamed_path(target_path, zf, member)
        
        elif self.duplicate_mode == "overwrite":
            return "overwrite", target_path
        
        return "skipped", target_path
    
    def get_renamed_path(self, target_path, zf, member):
        """Get a new path with suffix for duplicate file"""
        stem = target_path.stem
        suffix = target_path.suffix
        parent = target_path.parent
        counter = 1
        
        new_path = parent / f"{stem}_copy{counter}{suffix}"
        while new_path.exists():
            counter += 1
            new_path = parent / f"{stem}_copy{counter}{suffix}"
        
        return "renamed", new_path
    
    def extract_file(self, zf, member, target_path):
        """Extract a single file from ZIP"""
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as source, open(target_path, 'wb') as target:
                shutil.copyfileobj(source, target)
            return True
        except Exception as e:
            self.stats['errors'].append(f"Error extracting {member.filename}: {e}")
            return False
    
    def extract_with_merge(self, zip_path):
        """Extract ZIP file and merge with existing content"""
        print(f"\n📦 Processing: {zip_path.name}")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                members = [m for m in zf.filelist if not m.is_dir()]
                total = len(members)
                extracted = 0
                skipped = 0
                renamed = 0
                
                print(f"   Files: {total}")
                print(f"   Mode: {self.duplicate_mode}")
                
                # Progress bar
                bar_length = 50
                
                for i, member in enumerate(members):
                    # Calculate progress
                    progress = (i + 1) / total
                    filled = int(bar_length * progress)
                    bar = '█' * filled + '░' * (bar_length - filled)
                    percent = progress * 100
                    
                    # Show progress bar
                    print(f"\r   [{bar}] {percent:.1f}% ({i+1}/{total})", end='', flush=True)
                    
                    # Get target path
                    target_path = self.output_folder / member.filename
                    
                    # Handle file
                    if target_path.exists():
                        action, final_path = self.handle_duplicate(target_path, zf, member)
                        
                        if action == "skipped":
                            skipped += 1
                        elif action == "renamed":
                            if self.extract_file(zf, member, final_path):
                                renamed += 1
                                extracted += 1
                                self.stats['total_size'] += member.file_size
                        elif action == "overwrite":
                            if self.extract_file(zf, member, final_path):
                                extracted += 1
                                self.stats['total_size'] += member.file_size
                    else:
                        # New file, extract
                        if self.extract_file(zf, member, target_path):
                            extracted += 1
                            self.stats['total_size'] += member.file_size
                
                print()  # New line after progress bar
                print(f"   ✅ Extracted: {extracted} files")
                if skipped > 0:
                    print(f"   ⏭️  Skipped: {skipped} duplicates")
                if renamed > 0:
                    print(f"   📝 Renamed: {renamed} files")
                
                self.stats['zips_processed'] += 1
                self.stats['files_extracted'] += extracted
                self.stats['files_skipped'] += skipped
                self.stats['files_renamed'] += renamed
                
                return True
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.stats['errors'].append(f"Error processing {zip_path.name}: {e}")
            return False
    
    def run(self):
        """Main extraction process"""
        print("="*70)
        print("📦 Google Takeout ZIP Extractor & Merger - ADVANCED")
        print("="*70)
        print(f"\n📁 ZIP folder: {self.zip_folder}")
        print(f"📂 Output folder: {self.output_folder}")
        print(f"🔧 Duplicate mode: {self.duplicate_mode}")
        
        # Explain duplicate modes
        print("\n💡 Duplicate handling modes:")
        print("   • skip: Skip files with same size (fastest)")
        print("   • rename: Keep all versions with _copy suffix")
        print("   • compare: Compare file hashes, skip identical (slower)")
        print("   • overwrite: Replace existing files (not recommended)")
        print(f"\n   Current mode: {self.duplicate_mode}")
        
        # Create output folder
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # Find ZIP files
        print("\n🔍 Finding ZIP files...")
        zip_files = self.find_zip_files()
        
        if not zip_files:
            print(f"❌ No ZIP files found in {self.zip_folder}")
            return
        
        print(f"✓ Found {len(zip_files)} ZIP file(s)")
        
        # Show summary
        print("\n" + "="*70)
        print("ZIP Files to Process:")
        print("="*70)
        
        for i, zip_file in enumerate(zip_files, 1):
            size_mb = zip_file.stat().st_size / (1024**2)
            print(f"[{i:2d}] {zip_file.name} ({size_mb:.1f} MB)")
        
        print("="*70 + "\n")
        
        # Confirm
        response = input("Proceed with extraction? [Y/n]: ").strip().lower()
        if response and response not in ['y', 'yes']:
            print("Cancelled.")
            return
        
        # Process each ZIP
        print("\n" + "="*70)
        print("Starting extraction...")
        print("="*70)
        
        start_time = datetime.now()
        
        for i, zip_file in enumerate(zip_files, 1):
            print(f"\n[{i}/{len(zip_files)}]", end=' ')
            self.extract_with_merge(zip_file)
        
        # Final summary
        elapsed = (datetime.now() - start_time).total_seconds()
        
        print("\n" + "="*70)
        print("📊 EXTRACTION COMPLETE!")
        print("="*70)
        print(f"✅ ZIPs processed: {self.stats['zips_processed']}/{len(zip_files)}")
        print(f"📄 Files extracted: {self.stats['files_extracted']}")
        print(f"⏭️  Files skipped: {self.stats['files_skipped']} (duplicates)")
        if self.stats['files_renamed'] > 0:
            print(f"📝 Files renamed: {self.stats['files_renamed']}")
        print(f"💾 Total extracted: {self.stats['total_size'] / (1024**3):.2f} GB")
        print(f"⏱️  Time taken: {elapsed/60:.1f} minutes")
        
        if self.stats['errors']:
            print(f"\n⚠️  Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:
                print(f"   - {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... and {len(self.stats['errors']) - 5} more")
        
        print(f"\n📂 All files extracted to: {self.output_folder}")
        print("="*70 + "\n")

def main():
    print("="*70)
    print("Configuration")
    print("="*70)
    print(f"ZIP folder: {ZIP_FOLDER}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    print(f"Duplicate mode: {DUPLICATE_MODE}")
    print("="*70 + "\n")
    
    # Create extractor
    extractor = TakeoutExtractor(ZIP_FOLDER, OUTPUT_FOLDER, DUPLICATE_MODE)
    
    # Run extraction
    extractor.run()

if __name__ == "__main__":
    main()
