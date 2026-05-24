#!/usr/bin/env python3
"""Quick link checker for markdown files"""
import os
import re
import glob

def check_links_in_file(filepath):
    """Check all file links in a markdown file"""
    broken = []
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all markdown links [text](url)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    
    for text, url in links:
        url = url.strip()
        
        # Skip URLs, mailto, and anchors
        if url.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        
        # Handle anchor in file link
        if '#' in url:
            url = url.split('#')[0]
        
        if not url:  # Pure anchor link
            continue
        
        # Resolve relative to file location
        file_dir = os.path.dirname(filepath)
        full_path = os.path.normpath(os.path.join(file_dir, url))
        
        if not os.path.exists(full_path):
            broken.append((text, url, full_path))
    
    return broken

def main():
    print("🔍 Checking all markdown files for broken links...\n")
    
    # Find all markdown files
    md_files = []
    for root, dirs, files in os.walk('.'):
        # Skip venv, archive, node_modules, etc.
        dirs[:] = [d for d in dirs if d not in ['venv', 'archive', '__pycache__', '.git', 'node_modules']]
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    print(f"Found {len(md_files)} markdown files\n")
    
    all_broken = {}
    total_checked = 0
    
    for md_file in sorted(md_files):
        rel_path = os.path.relpath(md_file)
        broken = check_links_in_file(md_file)
        
        if broken:
            all_broken[rel_path] = broken
            total_checked += 1
            print(f"❌ {rel_path}")
            for text, url, full_path in broken:
                print(f"   → Broken: {url}")
                print(f"      (resolves to: {full_path})")
        else:
            total_checked += 1
    
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"Total files checked: {total_checked}")
    print(f"Files with broken links: {len(all_broken)}")
    
    if all_broken:
        print(f"\n{'='*60}")
        print(f"🔧 DETAILED BROKEN LINKS")
        print(f"{'='*60}\n")
        for filepath, broken_links in all_broken.items():
            print(f"\n📄 {filepath}")
            for text, url, full_path in broken_links:
                print(f"  ❌ [{text}]({url})")
                print(f"     Expected: {full_path}")
    else:
        print("\n✅ No broken file links found!")
    
    return len(all_broken)

if __name__ == "__main__":
    exit_code = main()
    exit(0 if exit_code == 0 else 1)
