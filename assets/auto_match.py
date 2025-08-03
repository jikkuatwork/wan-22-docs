#!/usr/bin/env python3

import json
import os
import re
import sys
from urllib.parse import unquote

def extract_uuid_from_url(url):
    """Extract UUID from video URL"""
    match = re.search(r'/([a-f0-9-]{36})\.mp4', url)
    return match.group(1) if match else None

def get_available_videos():
    """Get list of locally downloaded videos"""
    video_dir = "videos"
    if not os.path.exists(video_dir):
        return []
    
    videos = []
    for filename in os.listdir(video_dir):
        if filename.endswith('.mp4'):
            uuid = filename.replace('.mp4', '')
            videos.append(uuid)
    
    return videos

def load_video_urls():
    """Load all video URLs from JSON"""
    with open('videos.json', 'r') as f:
        urls = json.load(f)
    
    url_to_uuid = {}
    for url in urls:
        uuid = extract_uuid_from_url(url)
        if uuid:
            url_to_uuid[uuid] = url
    
    return url_to_uuid

def extract_markdown_video_info():
    """Extract video information from markdown with context"""
    with open('../wan-2.2.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find table rows with video references
    video_entries = []
    
    # Pattern to match table rows with DingTalk video links
    table_pattern = r'\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\|\s*\[([^]]+)\]\(([^)]+)\)\s*\|'
    matches = re.findall(table_pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        category = match[0].strip()
        description = match[1].strip()
        link_text = match[2].strip()
        link_url = match[3].strip()
        
        # Extract filename from Chinese link text
        filename_match = re.search(r'《([^》]+\.mp4)》', link_text)
        if filename_match:
            filename = filename_match.group(1)
            video_entries.append({
                'category': category,
                'description': description[:100] + '...' if len(description) > 100 else description,
                'filename': filename,
                'link_url': link_url,
                'full_match': match
            })
    
    return video_entries

def create_smart_mapping():
    """Create mapping with order-based assumptions but explicit warnings"""
    available_videos = get_available_videos()
    all_video_urls = load_video_urls()
    markdown_entries = extract_markdown_video_info()
    
    # Get list of downloaded UUIDs in the same order as videos.json
    with open('videos.json', 'r') as f:
        urls = json.load(f)
    
    downloaded_uuids = []
    for url in urls:  # Preserve order from JSON
        uuid = extract_uuid_from_url(url)
        if uuid and uuid in available_videos:
            downloaded_uuids.append(uuid)
    
    print(f"Creating mapping based on SEQUENTIAL ORDER assumption:")
    print(f"- Available local videos: {len(available_videos)}")
    print(f"- Video entries in markdown: {len(markdown_entries)}")
    print(f"- Ordered UUIDs from JSON: {len(downloaded_uuids)}")
    
    # Create mapping based on sequential order
    mapping = {}
    for i, entry in enumerate(markdown_entries):
        if i < len(downloaded_uuids):
            uuid = downloaded_uuids[i]
            mapping[entry['filename']] = {
                'uuid': uuid,
                'local_path': f'videos/{uuid}.mp4',
                'category': entry['category'],
                'index': i
            }
    
    return mapping

def update_markdown_with_smart_mapping():
    """Update markdown with explicit warnings about assumptions"""
    mapping = create_smart_mapping()
    
    with open('../wan-2.2.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements_made = 0
    for filename, info in mapping.items():
        # Find and replace the DingTalk link pattern for this filename
        pattern = r'\[请至钉钉文档查看附件《' + re.escape(filename) + r'》\]\([^)]+\)'
        replacement = f'[{info["local_path"]}]({info["local_path"]})'
        
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            replacements_made += count
    
    # Add warning header
    warning_header = """<!-- 
⚠️  IMPORTANT: VIDEO MAPPING ASSUMPTIONS
⚠️  This document maps videos based on the SEQUENTIAL ORDER assumption:
⚠️  - Video #1 in videos.json → First video entry in markdown table
⚠️  - Video #2 in videos.json → Second video entry in markdown table
⚠️  - And so on...
⚠️  
⚠️  This may NOT be correct! Please verify each video matches its description.
⚠️  The original videos.json order may not correspond to the markdown table order.
-->\n\n"""
    
    with open('../wan-2.2-auto-mapped.md', 'w', encoding='utf-8') as f:
        f.write(warning_header + content)
    
    print(f"\n✅ Updated markdown saved as 'wan-2.2-auto-mapped.md'")
    print(f"📝 Made {replacements_made} replacements")
    print(f"📋 Mapped {len(mapping)} videos to local paths")
    print("\n⚠️  CRITICAL: This mapping assumes sequential order!")
    print("⚠️  Please manually verify video content matches descriptions!")

if __name__ == '__main__':
    try:
        update_markdown_with_smart_mapping()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)