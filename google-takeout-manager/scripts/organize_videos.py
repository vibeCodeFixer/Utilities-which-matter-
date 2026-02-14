#!/usr/bin/env python3
"""
Video Mover with Hash Comparison and Blanket Options
Set a global policy for identical files at the start
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

class VideoMoverWithBlanketOptions:
    def __init__(self, source_folder, dest_folder, mode="move"):
        self.source_folder = Path(source_folder)
        self.dest_folder = Path(dest_folder)
        self.mode = mode  # "move" or "copy"
        self.video_extensions = ['.mp4', '.mov', '.MP4', '.MOV']
        self.stats = {
            'found': 0,
            'moved': 0,
            'skipped': 0,
            'renamed': 0,
            'overwritten': 0,
            'errors': []
        }
        # Blanket policies
        self.identical_policy = None  # "skip", "rename", "overwrite", "ask"
        self.different_policy = None  # "skip", "rename", "overwrite", "ask"
    
    def calculate_hash(self, filepath, show_progress=False):
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        filename = os.path.basename(filepath)
        
        if show_progress:
            file_size = os.path.getsize(filepath)
            size_str = self.format_size(file_size)
            print(f"      Calculating hash: {filename} ({size_str})... ", end='', flush=True)
        
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    hash_md5.update(chunk)
            
            hash_value = hash_md5.hexdigest()
            if show_progress:
                print(f"✓")
            return hash_value
        except Exception as e:
            if show_progress:
                print(f"❌ Error: {e}")
            return None
    
    def format_size(self, size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def set_blanket_policies(self):
        """Ask user for blanket policies at the start"""
        print("\n" + "="*70)
        print("⚙️  BLANKET POLICY SETUP")
        print("="*70)
        print("\nSet default actions for duplicate filenames:")
        print("You can choose how to handle files BEFORE processing starts.\n")
        
        # Policy for identical files (same hash)
        print("=" * 70)
        print("📋 When files have SAME HASH (identical content):")
        print("="*70)
        print("  [1] Skip - Don't move (recommended, saves space)")
        print("  [2] Rename - Keep both (file and file_copy1)")
        print("  [3] Overwrite - Replace destination with source")
        print("  [4] Ask me each time")
        print("="*70)
        
        while True:
            choice = input("\nYour choice for IDENTICAL files [1/2/3/4]: ").strip()
            if choice == '1':
                self.identical_policy = "skip"
                print("✓ Will SKIP all identical files (same hash)\n")
                break
            elif choice == '2':
                self.identical_policy = "rename"
                print("✓ Will RENAME all identical files (same hash)\n")
                break
            elif choice == '3':
                self.identical_policy = "overwrite"
                print("✓ Will OVERWRITE all identical files (same hash)\n")
                break
            elif choice == '4':
                self.identical_policy = "ask"
                print("✓ Will ASK for each identical file\n")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4")
        
        # Policy for different files (different hash)
        print("=" * 70)
        print("📋 When files have DIFFERENT HASH (different content):")
        print("="*70)
        print("  [1] Rename - Keep both (recommended, preserves both versions)")
        print("  [2] Skip - Don't move source")
        print("  [3] Overwrite - Replace destination with source")
        print("  [4] Ask me each time")
        print("="*70)
        
        while True:
            choice = input("\nYour choice for DIFFERENT files [1/2/3/4]: ").strip()
            if choice == '1':
                self.different_policy = "rename"
                print("✓ Will RENAME all different files (different hash)\n")
                break
            elif choice == '2':
                self.different_policy = "skip"
                print("✓ Will SKIP all different files (different hash)\n")
                break
            elif choice == '3':
                self.different_policy = "overwrite"
                print("✓ Will OVERWRITE all different files (different hash)\n")
                break
            elif choice == '4':
                self.different_policy = "ask"
                print("✓ Will ASK for each different file\n")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4")
        
        # Show summary
        print("=" * 70)
        print("📊 POLICY SUMMARY")
        print("=" * 70)
        print(f"✅ Identical files (same hash):   {self.identical_policy.upper()}")
        print(f"⚠️  Different files (diff hash):   {self.different_policy.upper()}")
        print("=" * 70 + "\n")
    
    def compare_files(self, source_path, dest_path):
        """Compare two files and return decision based on policy"""
        source_name = os.path.basename(source_path)
        source_size = os.path.getsize(source_path)
        dest_size = os.path.getsize(dest_path)
        
        print(f"\n      ⚠️  Duplicate filename: {source_name}")
        print(f"      Size - Source: {self.format_size(source_size)} | Dest: {self.format_size(dest_size)}")
        
        # Calculate hashes
        print(f"      🔍 Calculating hashes...")
        source_hash = self.calculate_hash(source_path, show_progress=True)
        dest_hash = self.calculate_hash(dest_path, show_progress=True)
        
        if source_hash is None or dest_hash is None:
            print(f"      ❌ Error calculating hashes")
            return self.ask_user_decision(source_name, "error", source_hash, dest_hash)
        
        # Show hash comparison
        print(f"\n      🔐 HASH COMPARISON:")
        print(f"         Source: {source_hash}")
        print(f"         Dest:   {dest_hash}")
        
        # Determine if identical or different
        if source_hash == dest_hash:
            print(f"      ✅ IDENTICAL (hashes match)")
            
            # Apply policy
            if self.identical_policy == "ask":
                return self.ask_user_decision(source_name, "identical", source_hash, dest_hash)
            else:
                print(f"      → Policy: {self.identical_policy.upper()}")
                return self.identical_policy
        else:
            print(f"      ⚠️  DIFFERENT (hashes differ)")
            
            # Apply policy
            if self.different_policy == "ask":
                return self.ask_user_decision(source_name, "different", source_hash, dest_hash)
            else:
                print(f"      → Policy: {self.different_policy.upper()}")
                return self.different_policy
    
    def ask_user_decision(self, filename, file_status, source_hash, dest_hash):
        """Ask user what to do with this specific file"""
        print(f"\n      {'='*60}")
        print(f"      DECISION NEEDED: {filename}")
        print(f"      {'='*60}")
        
        if file_status == "identical":
            print(f"      Status: Files are IDENTICAL (same hash)")
            print(f"        [s] Skip - Don't move")
            print(f"        [r] Rename - Keep both")
            print(f"        [o] Overwrite - Replace destination")
        elif file_status == "different":
            print(f"      Status: Files are DIFFERENT (different hash)")
            print(f"        [r] Rename - Keep both [RECOMMENDED]")
            print(f"        [s] Skip - Don't move")
            print(f"        [o] Overwrite - Replace destination")
        else:  # error
            print(f"      Status: Error calculating hashes")
            print(f"        [s] Skip - Don't move")
            print(f"        [r] Rename - Keep both")
            print(f"        [o] Overwrite - Replace destination")
        
        print(f"      {'='*60}")
        
        while True:
            choice = input("      Your choice [s/r/o]: ").strip().lower()
            if choice in ['s', 'r', 'o']:
                decision_map = {'s': 'skip', 'r': 'rename', 'o': 'overwrite'}
                return decision_map[choice]
            else:
                print("      Invalid choice. Please enter s, r, or o")
    
    def get_renamed_path(self, dest_path):
        """Get a unique filename with _copy suffix"""
        stem = dest_path.stem
        suffix = dest_path.suffix
        parent = dest_path.parent
        counter = 1
        
        new_path = parent / f"{stem}_copy{counter}{suffix}"
        while new_path.exists():
            counter += 1
            new_path = parent / f"{stem}_copy{counter}{suffix}"
        
        return new_path
    
    def find_videos(self):
        """Find all video files in source folder and subfolders"""
        print("\n🔍 Searching for video files...")
        videos = []
        
        for root, dirs, files in os.walk(self.source_folder):
            for file in files:
                if any(file.endswith(ext) for ext in self.video_extensions):
                    full_path = Path(root) / file
                    videos.append(full_path)
        
        return videos
    
    def move_video(self, video_path):
        """Move or copy a single video file"""
        try:
            filename = video_path.name
            dest_path = self.dest_folder / filename
            
            # Check if file already exists
            if dest_path.exists():
                # Compare files and get decision based on policy
                decision = self.compare_files(video_path, dest_path)
                
                if decision == 'skip':
                    self.stats['skipped'] += 1
                    return 'skipped', filename
                
                elif decision == 'rename':
                    dest_path = self.get_renamed_path(dest_path)
                    self.stats['renamed'] += 1
                    
                elif decision == 'overwrite':
                    # Delete existing file first
                    dest_path.unlink()
                    self.stats['overwritten'] += 1
            
            # Move or copy the file
            if self.mode == "move":
                shutil.move(str(video_path), str(dest_path))
                action = 'moved'
            else:  # copy
                shutil.copy2(str(video_path), str(dest_path))
                action = 'copied'
            
            self.stats['moved'] += 1
            return action, dest_path.name
            
        except Exception as e:
            self.stats['errors'].append(f"{video_path.name}: {str(e)}")
            return 'error', str(e)
    
    def run(self):
        """Main process"""
        print("="*70)
        print(f"🎬 Video Mover with Hash Comparison & Blanket Options")
        print("="*70)
        print(f"\n📁 Source: {self.source_folder}")
        print(f"📂 Destination: {self.dest_folder}")
        print(f"🎯 Extensions: {', '.join(self.video_extensions)}")
        print(f"⚙️  Mode: {self.mode.upper()}")
        
        # Validate folders
        if not self.source_folder.exists():
            print(f"\n❌ Source folder does not exist: {self.source_folder}")
            return
        
        # Create destination folder
        self.dest_folder.mkdir(parents=True, exist_ok=True)
        
        # Find videos
        videos = self.find_videos()
        self.stats['found'] = len(videos)
        
        if not videos:
            print("\n❌ No video files found!")
            return
        
        print(f"✓ Found {len(videos)} video file(s)")
        
        # Set blanket policies BEFORE showing preview
        self.set_blanket_policies()
        
        # Show preview
        print("="*70)
        print("Files to process:")
        print("="*70)
        
        for i, video in enumerate(videos[:10], 1):
            size = video.stat().st_size
            rel_path = video.relative_to(self.source_folder)
            print(f"[{i:2d}] {rel_path} ({self.format_size(size)})")
        
        if len(videos) > 10:
            print(f"... and {len(videos) - 10} more files")
        
        print("="*70 + "\n")
        
        # Confirm
        action_word = "move" if self.mode == "move" else "copy"
        response = input(f"Proceed to {action_word} {len(videos)} file(s)? [Y/n]: ").strip().lower()
        if response and response not in ['y', 'yes']:
            print("Cancelled.")
            return
        
        # Process files
        print("\n" + "="*70)
        print(f"Processing files...")
        print("="*70)
        
        start_time = datetime.now()
        
        for i, video in enumerate(videos, 1):
            rel_path = video.relative_to(self.source_folder)
            print(f"\n[{i:3d}/{len(videos)}] {rel_path}")
            
            status, info = self.move_video(video)
            
            if status == 'moved':
                print(f"      ✅ Moved to: {info}")
            elif status == 'copied':
                print(f"      ✅ Copied to: {info}")
            elif status == 'skipped':
                print(f"      ⏭️  Skipped")
            elif status == 'error':
                print(f"      ❌ Error: {info}")
        
        # Summary
        elapsed = (datetime.now() - start_time).total_seconds()
        
        print("\n" + "="*70)
        print("📊 FINAL SUMMARY")
        print("="*70)
        print(f"🔍 Found: {self.stats['found']} video files")
        print(f"✅ Processed: {self.stats['moved']} files")
        print(f"⏭️  Skipped: {self.stats['skipped']} files")
        print(f"📝 Renamed: {self.stats['renamed']} files")
        if self.stats['overwritten'] > 0:
            print(f"🔄 Overwritten: {self.stats['overwritten']} files")
        
        if self.stats['errors']:
            print(f"❌ Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:
                print(f"   - {error}")
        
        print(f"\n⏱️  Time taken: {elapsed/60:.1f} minutes")
        print(f"📂 Files in: {self.dest_folder}")
        print("="*70 + "\n")

def main():
    print("="*70)
    print("🎬 Video Mover with Hash Comparison & Blanket Options")
    print("="*70)
    print("\nThis script lets you set a BLANKET POLICY for all duplicates")
    print("upfront, so you don't have to decide for each file.\n")
    
    # Get source folder
    while True:
        source = input("📁 Enter SOURCE folder path: ").strip().strip('"').strip("'")
        
        if not source:
            print("❌ Please enter a path")
            continue
        
        source_path = Path(source)
        if not source_path.exists():
            print(f"❌ Folder does not exist: {source}")
            continue
        
        if not source_path.is_dir():
            print(f"❌ Path is not a folder: {source}")
            continue
        
        break
    
    # Get destination folder
    while True:
        dest = input("📂 Enter DESTINATION folder path: ").strip().strip('"').strip("'")
        
        if not dest:
            print("❌ Please enter a path")
            continue
        
        dest_path = Path(dest)
        
        if dest_path.resolve() == source_path.resolve():
            print("❌ Destination cannot be the same as source!")
            continue
        
        break
    
    # Ask for mode
    print("\n" + "="*70)
    print("Mode:")
    print("="*70)
    print("  [1] MOVE - Remove from source")
    print("  [2] COPY - Keep in source")
    print("="*70)
    
    while True:
        mode_choice = input("\nSelect mode [1/2]: ").strip()
        if mode_choice == '1':
            mode = "move"
            break
        elif mode_choice == '2':
            mode = "copy"
            break
        else:
            print("Invalid choice. Please enter 1 or 2")
    
    # Create mover and run
    mover = VideoMoverWithBlanketOptions(source_path, dest_path, mode)
    mover.run()

if __name__ == "__main__":
    main()
