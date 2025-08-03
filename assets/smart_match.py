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

def create_uuid_mapping():
    """Try to create intelligent mapping between UUIDs and video entries"""
    available_videos = get_available_videos()
    all_video_urls = load_video_urls()
    markdown_entries = extract_markdown_video_info()
    
    print(f"Available local videos: {len(available_videos)}")
    print(f"Total video URLs in JSON: {len(all_video_urls)}")
    print(f"Video entries in markdown: {len(markdown_entries)}")
    
    # Check which UUIDs from JSON are actually downloaded
    downloaded_uuids = []
    for uuid in all_video_urls.keys():
        if uuid in available_videos:
            downloaded_uuids.append(uuid)
    
    print(f"Downloaded UUIDs that match JSON: {len(downloaded_uuids)}")
    
    # Since we can't reliably match content to UUIDs, we'll create a mapping
    # based on the assumption that the first N markdown entries correspond
    # to the first N downloaded videos, but we'll be explicit about this assumption
    
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
    
    return mapping, markdown_entries

def generate_mapping_report():
    """Generate a report showing the mapping assumptions"""
    mapping, entries = create_uuid_mapping()
    
    print("\n" + "="*80)
    print("VIDEO MAPPING REPORT")
    print("="*80)
    print("⚠️  WARNING: This mapping is based on ASSUMPTIONS about order!")
    print("⚠️  The videos.json array order may not match the markdown table order!")
    print("="*80)
    
    print(f"\nMapped {len(mapping)} videos:")
    for i, (filename, info) in enumerate(mapping.items()):
        print(f"{i+1:2d}. {info['category']:<20} -> {info['uuid']}.mp4")
        print(f"    Original: {filename[:80]}...")
        print()
    
    unmapped_count = len(entries) - len(mapping)
    if unmapped_count > 0:
        print(f"⚠️  {unmapped_count} markdown entries remain unmapped (no local videos)")
    
    return mapping

def update_markdown_with_mapping(mapping):
    """Update markdown with the mapping (with warnings)"""
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
    
    # Save updated content with warning header
    warning_header = """<!-- 
⚠️  WARNING: Video mappings are based on assumptions!
⚠️  The order of videos in videos.json may not match the order in this document.
⚠️  Please verify that each video matches its description before using.
-->\n\n"""
    
    with open('../wan-2.2-smart-local.md', 'w', encoding='utf-8') as f:
        f.write(warning_header + content)
    
    print(f"\n✅ Updated markdown saved as 'wan-2.2-smart-local.md'")
    print(f"📝 Made {replacements_made} replacements")
    print("⚠️  Please manually verify the video-description matches!")

if __name__ == '__main__':
    try:
        mapping = generate_mapping_report()
        
        response = input(f"\nProceed with updating markdown based on these assumptions? (y/N): ")
        if response.lower() == 'y':
            update_markdown_with_mapping(mapping)
        else:
            print("Mapping cancelled. No files were modified.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)