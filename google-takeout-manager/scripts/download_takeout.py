#!/usr/bin/env python3
"""
Google Takeout Downloader - PARALLEL Download with Range Selection
Clicks all buttons in your range at once - all files download simultaneously!
"""

import os
import time
from pathlib import Path
import glob
from datetime import datetime
import re
import sys

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("❌ Selenium not installed!")
    print("\nInstall with:")
    print("  pip install selenium")
    exit(1)

# Configuration
ARCHIVE_ID = "6dba9630-cc98-4507-aa5f-6376563d25c0"
USER_ID = "113508548453534889343"
TOTAL_PARTS = 91
DOWNLOAD_DIR = os.path.abspath("google_takeout_downloads")
MANAGE_URL = f"https://takeout.google.com/manage/archive/{ARCHIVE_ID}"

class DownloadMonitor:
    """Monitor download directory"""
    
    def __init__(self, download_dir):
        self.download_dir = download_dir
    
    def get_zip_files(self):
        """Get list of completed zip files"""
        pattern = os.path.join(self.download_dir, "*.zip")
        return glob.glob(pattern)
    
    def find_existing_file_by_index(self, index):
        """Find if a file for this index already exists"""
        index_str = f"{index:03d}"
        all_zips = self.get_zip_files()
        
        for zip_file in all_zips:
            basename = os.path.basename(zip_file)
            pattern = rf'takeout-.*-{index_str}(?:\s*\(\d+\))?\.zip$'
            
            if re.search(pattern, basename):
                return zip_file
        
        return None
    
    def get_file_info(self, filepath):
        """Get information about a file"""
        if not os.path.exists(filepath):
            return None
        
        size = os.path.getsize(filepath)
        mod_time = os.path.getmtime(filepath)
        mod_datetime = datetime.fromtimestamp(mod_time)
        
        return {
            'size': size,
            'size_mb': size / (1024**2),
            'size_gb': size / (1024**3),
            'modified': mod_datetime,
            'modified_str': mod_datetime.strftime('%Y-%m-%d %H:%M:%S')
        }

class TakeoutDownloader:
    def __init__(self, start_index=None, end_index=None):
        self.download_dir = DOWNLOAD_DIR
        self.driver = None
        self.monitor = DownloadMonitor(DOWNLOAD_DIR)
        self.skip_all_existing = False
        self.start_index = start_index
        self.end_index = end_index
        
    def setup_driver(self):
        """Setup Chrome with download preferences"""
        os.makedirs(self.download_dir, exist_ok=True)
        
        chrome_options = Options()
        
        # Download preferences
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Browser settings
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"\n❌ Error starting Chrome: {e}")
            print("\nMake sure Chrome and ChromeDriver are installed:")
            print("  Windows: Download from https://chromedriver.chromium.org/")
            print("  Linux: sudo apt install chromium-chromedriver")
            print("  macOS: brew install chromedriver")
            return False
    
    def get_index_range(self):
        """Get index range from user if not provided"""
        if self.start_index is not None and self.end_index is not None:
            return self.start_index, self.end_index
        
        print("\n" + "="*70)
        print("📝 INDEX RANGE SELECTION")
        print("="*70)
        print(f"\nTotal files available: {TOTAL_PARTS} (indices 0-{TOTAL_PARTS-1})")
        print("\nExamples:")
        print("  • Download all:        From: 0   To: 90")
        print("  • First 10 files:      From: 0   To: 9")
        print("  • Files 20-30:         From: 20  To: 30")
        print("  • Last 10 files:       From: 81  To: 90")
        print("\n⚡ NOTE: All files in range will download SIMULTANEOUSLY!")
        print("="*70 + "\n")
        
        while True:
            try:
                start = input(f"Enter START index (0-{TOTAL_PARTS-1}): ").strip()
                if not start:
                    print("❌ Please enter a number")
                    continue
                start = int(start)
                
                if start < 0 or start >= TOTAL_PARTS:
                    print(f"❌ Start index must be between 0 and {TOTAL_PARTS-1}")
                    continue
                
                end = input(f"Enter END index ({start}-{TOTAL_PARTS-1}): ").strip()
                if not end:
                    print("❌ Please enter a number")
                    continue
                end = int(end)
                
                if end < start or end >= TOTAL_PARTS:
                    print(f"❌ End index must be between {start} and {TOTAL_PARTS-1}")
                    continue
                
                count = end - start + 1
                print(f"\n⚡ Will start downloading {count} file(s) SIMULTANEOUSLY!")
                print(f"   Indices {start} to {end} will all download at once.\n")
                
                confirm = input("Proceed? [Y/n]: ").strip().lower()
                if confirm in ['', 'y', 'yes']:
                    return start, end
                else:
                    print("Cancelled. Please enter new range.\n")
                    
            except ValueError:
                print("❌ Please enter valid numbers")
            except KeyboardInterrupt:
                print("\n\nCancelled by user")
                sys.exit(0)
    
    def wait_for_login(self, start_index, end_index):
        """Interactive wait for user login"""
        count = end_index - start_index + 1
        
        print("\n" + "="*70)
        print("🔐 PLEASE LOGIN")
        print("="*70)
        print("\n📌 STEPS:")
        print("  1. Chrome browser has opened")
        print("  2. Login to your Google account (if needed)")
        print("  3. You should see the Takeout archive page")
        print("  4. When ready, press ENTER here to start")
        print(f"\n⚡ DOWNLOAD MODE: PARALLEL (ALL AT ONCE)")
        print(f"   • Range: Index {start_index} to {end_index}")
        print(f"   • Count: {count} file(s)")
        print(f"   • All {count} files will start downloading simultaneously!")
        print("\n💡 TIP: Make sure you have enough bandwidth and disk space!")
        print("="*70 + "\n")
        
        input("⏎ Press ENTER when logged in and ready...")
        print(f"\n✓ Starting {count} parallel downloads!\n")
        time.sleep(2)
    
    def check_existing_files(self, start_index, end_index):
        """Check which files in range already exist"""
        existing = []
        missing = []
        
        for i in range(start_index, end_index + 1):
            existing_file = self.monitor.find_existing_file_by_index(i)
            if existing_file:
                existing.append((i, existing_file))
            else:
                missing.append(i)
        
        return existing, missing
    
    def ask_about_existing_files(self, existing_files, start_index, end_index):
        """Ask user what to do with existing files"""
        if not existing_files:
            return []  # No existing files
        
        count = len(existing_files)
        total = end_index - start_index + 1
        
        print(f"\n{'='*70}")
        print(f"⚠️  FOUND {count} EXISTING FILE(S)")
        print(f"{'='*70}")
        print(f"\nRange: {start_index} to {end_index} ({total} files)")
        print(f"Existing: {count} files")
        print(f"Missing: {total - count} files")
        print("\nExisting files:")
        
        for i, (index, filepath) in enumerate(existing_files[:5], 1):
            filename = os.path.basename(filepath)
            file_info = self.monitor.get_file_info(filepath)
            size_str = f"{file_info['size_gb']:.2f} GB" if file_info and file_info['size_gb'] >= 1 else f"{file_info['size_mb']:.2f} MB" if file_info else "Unknown"
            print(f"  [{index}] Index {index}: {filename} ({size_str})")
        
        if count > 5:
            print(f"  ... and {count - 5} more")
        
        print(f"\n{'='*70}")
        print("What would you like to do?")
        print("  [s] Skip existing files (download only missing ones)")
        print("  [r] Re-download ALL files (delete existing and download all)")
        print(f"{'='*70}\n")
        
        while True:
            choice = input("Your choice [s/r]: ").strip().lower()
            
            if choice == 's':
                print(f"\n✓ Will skip {count} existing file(s)")
                print(f"  Will download {total - count} missing file(s)\n")
                return []  # Return empty list = skip existing
            elif choice == 'r':
                print(f"\n✓ Will re-download ALL {total} files")
                print("  Deleting existing files...\n")
                
                deleted = 0
                for index, filepath in existing_files:
                    try:
                        os.remove(filepath)
                        print(f"  🗑️  Deleted: {os.path.basename(filepath)}")
                        deleted += 1
                    except Exception as e:
                        print(f"  ⚠️  Could not delete {os.path.basename(filepath)}: {e}")
                
                print(f"\n✓ Deleted {deleted} file(s)\n")
                return list(range(start_index, end_index + 1))  # Download all
            else:
                print("Invalid choice. Please enter 's' or 'r'")
    
    def find_download_buttons(self):
        """Find all download links/buttons"""
        try:
            selectors = [
                "a[href*='takeout/download']",
                "a[aria-label*='Download']",
            ]
            
            all_links = []
            for selector in selectors:
                links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                all_links.extend(links)
            
            # Remove duplicates
            seen = set()
            unique_links = []
            for link in all_links:
                href = link.get_attribute('href')
                if href and href not in seen:
                    seen.add(href)
                    unique_links.append(link)
            
            return unique_links
        except Exception as e:
            print(f"❌ Error finding buttons: {e}")
            return []
    
    def click_all_in_range(self, start_index, end_index, indices_to_download):
        """Click all download buttons in the specified range"""
        links = self.find_download_buttons()
        
        if not links:
            print("❌ No download buttons found!")
            return 0
        
        total = len(links)
        clicked = 0
        failed = []
        
        print("="*70)
        print("🚀 CLICKING ALL DOWNLOAD BUTTONS...")
        print("="*70 + "\n")
        
        for i in indices_to_download:
            if i >= total:
                print(f"[{i:2d}] ⚠️  Index out of range (only {total} buttons found)")
                failed.append(i)
                continue
            
            try:
                link = links[i]
                
                # Get label
                label = (link.get_attribute("aria-label") or 
                        link.get_attribute("title") or 
                        f"Index {i}")
                
                # Scroll into view
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", 
                    link
                )
                time.sleep(0.1)
                
                # Click
                print(f"[{i:2d}] 🖱️  Clicking: {label}... ", end='', flush=True)
                link.click()
                print("✓")
                clicked += 1
                
                # Small delay to avoid overwhelming the browser
                time.sleep(0.3)
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}")
                failed.append(i)
        
        print("\n" + "="*70)
        print(f"✅ Clicked {clicked} download buttons")
        if failed:
            print(f"❌ Failed: {len(failed)} buttons - Indices: {failed}")
        print("="*70 + "\n")
        
        return clicked
    
    def run(self):
        """Main download process"""
        print("="*70)
        print("🚀 Google Takeout Downloader - PARALLEL MODE")
        print("="*70)
        print(f"\n📦 Archive ID: {ARCHIVE_ID}")
        print(f"📁 Download folder: {DOWNLOAD_DIR}")
        print(f"🎯 Total available: {TOTAL_PARTS} files (indices 0-{TOTAL_PARTS-1})")
        print(f"\n⚡ MODE: PARALLEL - All files download at once!")
        
        # Get index range
        start_index, end_index = self.get_index_range()
        count = end_index - start_index + 1
        
        # Check existing files
        existing_files, missing_indices = self.check_existing_files(start_index, end_index)
        
        if existing_files:
            print(f"\nℹ️  Found {len(existing_files)} existing file(s) in your range")
            indices_to_download = self.ask_about_existing_files(existing_files, start_index, end_index)
            
            if not indices_to_download:
                # User chose to skip existing files
                indices_to_download = missing_indices
        else:
            # No existing files, download all in range
            indices_to_download = list(range(start_index, end_index + 1))
        
        if not indices_to_download:
            print("\n✓ All files in range already exist. Nothing to download!")
            print(f"📁 Files in: {DOWNLOAD_DIR}\n")
            return
        
        print("\n" + "="*70 + "\n")
        
        # Setup browser
        print("🌐 Starting Chrome browser...")
        if not self.setup_driver():
            return
        
        try:
            # Navigate
            print(f"🔗 Navigating to archive page...\n")
            self.driver.get(MANAGE_URL)
            time.sleep(3)
            
            # Wait for login
            self.wait_for_login(start_index, end_index)
            
            # Find and click all buttons
            print("🔍 Finding download buttons...")
            links = self.find_download_buttons()
            
            if not links:
                print("❌ No download buttons found!")
                return
            
            print(f"✓ Found {len(links)} download buttons\n")
            
            # Click all buttons in range
            start_time = time.time()
            clicked = self.click_all_in_range(start_index, end_index, indices_to_download)
            
            if clicked > 0:
                print(f"⚡ Started {clicked} parallel downloads!")
                print(f"\n💡 TIPS:")
                print(f"   • Check Chrome downloads: Press Ctrl+J (Windows/Linux) or Cmd+J (Mac)")
                print(f"   • Downloads folder: {DOWNLOAD_DIR}")
                print(f"   • All {clicked} files are downloading simultaneously")
                print(f"   • This may take a while depending on file sizes and your internet speed")
                print("\n" + "="*70 + "\n")
            
            # Keep browser open
            print("⏸️  Browser will stay open to monitor downloads.")
            print("   Press ENTER when all downloads are complete to close browser...")
            input()
            
            # Final summary
            elapsed = time.time() - start_time
            completed = len(self.monitor.get_zip_files())
            
            print("\n" + "="*70)
            print("📊 SUMMARY")
            print("="*70)
            print(f"🖱️  Clicked: {clicked} buttons")
            print(f"📁 Files in folder: {completed} .zip files")
            print(f"⏱️  Session time: {elapsed/60:.1f} minutes")
            print(f"\n📁 Files in: {DOWNLOAD_DIR}")
            print("="*70 + "\n")
            
            print("💡 TIP: Check Chrome downloads (Ctrl+J) to verify all completed!")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                print("\n🔒 Closing browser...")
                self.driver.quit()
                print("✓ Done!\n")

def main():
    # Check for command line arguments
    start_index = None
    end_index = None
    
    if len(sys.argv) == 3:
        try:
            start_index = int(sys.argv[1])
            end_index = int(sys.argv[2])
            print(f"Using command line arguments: {start_index} to {end_index}")
        except ValueError:
            print("Invalid arguments. Usage: python script.py [start_index] [end_index]")
            sys.exit(1)
    
    downloader = TakeoutDownloader(start_index, end_index)
    downloader.run()

if __name__ == "__main__":
    main()
