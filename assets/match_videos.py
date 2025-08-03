#!/usr/bin/env python3

import json
import os
import re
import sys

def extract_uuid_from_url(url):
    """Extract UUID from the original video URL"""
    match = re.search(r'/([a-f0-9-]{36})\.mp4', url)
    return match.group(1) if match else None

def read_videos_json():
    """Read the videos.json file and extract UUIDs"""
    with open('videos.json', 'r') as f:
        urls = json.load(f)
    
    videos = []
    for i, url in enumerate(urls):
        uuid = extract_uuid_from_url(url)
        if uuid:
            videos.append({
                'index': i,
                'uuid': uuid,
                'url': url,
                'local_file': f'videos/{uuid}.mp4'
            })
    
    return videos

def find_dingtalk_links_in_markdown():
    """Find all DingTalk links in the markdown file"""
    with open('../wan-2.2.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all DingTalk links with video references
    pattern = r'\[请至钉钉文档查看附件《([^》]+\.mp4)》\]\([^)]+\)'
    matches = re.findall(pattern, content)
    
    return matches

def create_replacement_mapping():
    """Create a mapping between DingTalk links and local video files"""
    videos = read_videos_json()
    dingtalk_videos = find_dingtalk_links_in_markdown()
    
    print(f"Found {len(videos)} downloaded videos")
    print(f"Found {len(dingtalk_videos)} DingTalk video references")
    
    print("\nDownloaded videos:")
    for video in videos:
        print(f"  {video['index']}: {video['uuid']}.mp4")
    
    print("\nDingTalk video references:")
    for i, filename in enumerate(dingtalk_videos):
        print(f"  {i}: {filename}")
    
    # Since we have the same number of videos, we can map them by order
    mapping = {}
    for i, video in enumerate(videos):
        if i < len(dingtalk_videos):
            mapping[dingtalk_videos[i]] = video['local_file']
    
    return mapping

def update_markdown_with_local_paths():
    """Update the markdown file to use local video paths"""
    mapping = create_replacement_mapping()
    
    with open('../wan-2.2.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace DingTalk links with local video links
    for dingtalk_filename, local_path in mapping.items():
        # Find the full DingTalk link pattern and replace it
        pattern = r'\[请至钉钉文档查看附件《' + re.escape(dingtalk_filename) + r'》\]\([^)]+\)'
        replacement = f'[{local_path}]({local_path})'
        content = re.sub(pattern, replacement, content)
    
    # Save the updated content
    with open('../wan-2.2-local.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nUpdated markdown saved as wan-2.2-local.md")
    print(f"Replaced {len(mapping)} video references")

if __name__ == '__main__':
    try:
        update_markdown_with_local_paths()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)