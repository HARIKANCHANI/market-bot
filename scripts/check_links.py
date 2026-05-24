#!/usr/bin/env python3
"""
Script to check for broken links in markdown files.
Checks both relative file links and URLs.
"""
import os
import re
from pathlib import Path
from urllib.parse import urlparse
import requests

def find_markdown_files(root_dir):
    """Find all markdown files, excluding venv and archive."""
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip venv and archive directories
        dirs[:] = [d for d in dirs if d not in ['venv', 'archive', '__pycache__', '.git']]
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_links(content, filepath):
    """Extract all links from markdown content."""
    links = []
    
    # Markdown links: [text](url)
    markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    for text, url in markdown_links:
        links.append({'type': 'markdown', 'text': text, 'url': url, 'line': None})
    
    # Reference-style links: [text]: url
    ref_links = re.findall(r'^\[([^\]]+)\]:\s*(.+)$', content, re.MULTILINE)
    for text, url in ref_links:
        links.append({'type': 'reference', 'text': text, 'url': url, 'line': None})
    
    # Plain URLs (http/https)
    plain_urls = re.findall(r'https?://[^\s\)<>\'"]+', content)
    for url in plain_urls:
        # Skip if already captured in markdown links
        if not any(link['url'] == url for link in links):
            links.append({'type': 'plain', 'text': '', 'url': url, 'line': None})
    
    # Add line numbers
    lines = content.split('\n')
    for link in links:
        for i, line in enumerate(lines, 1):
            if link['url'] in line:
                link['line'] = i
                break
    
    return links

def check_file_link(link_path, source_file):
    """Check if a relative file link exists."""
    # Handle anchor links
    if '#' in link_path:
        link_path = link_path.split('#')[0]
    
    if not link_path or link_path.startswith('http'):
        return True
    
    # Resolve relative to source file
    source_dir = os.path.dirname(source_file)
    full_path = os.path.normpath(os.path.join(source_dir, link_path))
    
    return os.path.exists(full_path)

def check_url(url, timeout=5):
    """Check if URL is accessible (basic check)."""
    try:
        # Skip checking some common patterns that don't need validation
        if url.startswith('mailto:') or url.startswith('#'):
            return True
        
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except:
        return False

def main():
    root_dir = Path(__file__).parent.parent
    print(f"🔍 Scanning for markdown files in: {root_dir}\n")

    md_files = find_markdown_files(root_dir)
    print(f"Found {len(md_files)} markdown files")

    # Debug: show some files
    if md_files:
        print(f"Sample files:")
        for f in md_files[:5]:
            print(f"  - {os.path.relpath(f, root_dir)}")
    print()

    broken_links = []
    total_links = 0
    file_links = 0

    for md_file in md_files:
        rel_path = os.path.relpath(md_file, root_dir)
        try:
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Error reading {rel_path}: {e}")
            continue

        links = extract_links(content, md_file)
        total_links += len(links)

        if not links:
            continue

        print(f"📄 {rel_path}: {len(links)} links")

        for link in links:
            url = link['url'].strip()

            # Check relative file links only (skip URL checking for speed)
            if not url.startswith('http') and not url.startswith('mailto:') and not url.startswith('#'):
                file_links += 1
                if not check_file_link(url, md_file):
                    broken_links.append({
                        'file': rel_path,
                        'line': link['line'],
                        'type': 'file',
                        'url': url,
                        'text': link['text']
                    })
                    print(f"  ❌ Broken file link: {url} (line {link['line']})")
    
    print(f"\n{'='*80}")
    print(f"📊 SUMMARY")
    print(f"{'='*80}")
    print(f"Total markdown files: {len(md_files)}")
    print(f"Total links found: {total_links}")
    print(f"File links checked: {file_links}")
    print(f"Broken links: {len(broken_links)}")
    
    if broken_links:
        print(f"\n{'='*80}")
        print(f"🔧 BROKEN LINKS TO FIX")
        print(f"{'='*80}")
        for broken in broken_links:
            print(f"\nFile: {broken['file']}")
            print(f"  Line: {broken['line']}")
            print(f"  Type: {broken['type']}")
            print(f"  Link: {broken['url']}")
            if broken['text']:
                print(f"  Text: {broken['text']}")
    else:
        print("\n✅ No broken links found!")
    
    return broken_links

if __name__ == "__main__":
    broken_links = main()
    exit(0 if not broken_links else 1)
