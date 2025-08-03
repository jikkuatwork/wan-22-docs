#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path
import html

def parse_markdown_content():
    """Parse the markdown file and extract structured content"""
    with open('../wan-2.2-auto-mapped.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract main sections
    sections = {}
    
    # Extract video table entries
    table_pattern = r'\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\|\s*\[([^]]+)\]\(([^)]+)\)\s*\|'
    video_matches = re.findall(table_pattern, content, re.MULTILINE | re.DOTALL)
    
    # Group videos by category type
    categories = {
        'lighting': [],
        'time': [],
        'shots': [],
        'composition': [],
        'lens': [],
        'colors': [],
        'motion': [],
        'emotions': [],
        'camera': [],
        'styles': [],
        'effects': []
    }
    
    for match in video_matches:
        category = match[0].strip()
        description = match[1].strip()
        link_text = match[2].strip()
        video_path = match[3].strip()
        
        # Categorize based on keywords
        category_lower = category.lower()
        if 'lighting' in category_lower or 'light' in category_lower:
            categories['lighting'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        elif 'time' in category_lower or 'sunrise' in category_lower or 'sunset' in category_lower or 'dawn' in category_lower or 'dusk' in category_lower or 'night' in category_lower:
            categories['time'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        elif 'shot' in category_lower or 'close' in category_lower or 'wide' in category_lower or 'extreme' in category_lower:
            categories['shots'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        elif 'composition' in category_lower or 'heavy' in category_lower or 'center' in category_lower:
            categories['composition'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        elif 'lens' in category_lower or 'focal' in category_lower:
            categories['lens'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        elif 'color' in category_lower or 'saturated' in category_lower or 'desaturated' in category_lower:
            categories['colors'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        elif any(word in category_lower for word in ['running', 'walking', 'jumping', 'dancing', 'swimming', 'tennis', 'basketball', 'football', 'rugby', 'soccer', 'cartwheel']):
            categories['motion'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        elif any(word in category_lower for word in ['angrily', 'fear', 'happy', 'sadly', 'surprised']):
            categories['emotions'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        elif 'camera' in category_lower or 'pushes' in category_lower or 'pulls' in category_lower or 'pans' in category_lower or 'tilts' in category_lower or 'handheld' in category_lower or 'tracking' in category_lower or 'arc' in category_lower:
            categories['camera'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        elif 'style' in category_lower or 'animation' in category_lower or 'cartoon' in category_lower or 'pixel' in category_lower or 'puppet' in category_lower or 'claymation' in category_lower or 'anime' in category_lower or 'painting' in category_lower:
            categories['styles'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
        else:
            categories['effects'].append({
                'name': category,
                'description': description,
                'video_path': video_path,
                'safe_name': re.sub(r'[^a-zA-Z0-9]', '_', category).lower()
            })
    
    return categories

def create_base_css():
    """Create beautiful CSS styles"""
    return """
    :root {
        --primary-color: #2563eb;
        --secondary-color: #1e40af;
        --accent-color: #f59e0b;
        --text-color: #1f2937;
        --text-light: #6b7280;
        --bg-color: #ffffff;
        --bg-secondary: #f8fafc;
        --border-color: #e5e7eb;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.6;
        color: var(--text-color);
        background-color: var(--bg-color);
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }

    header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }

    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        font-size: 1.125rem;
        opacity: 0.9;
        font-weight: 300;
    }

    nav {
        background: var(--bg-secondary);
        border-bottom: 1px solid var(--border-color);
        padding: 1rem 0;
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .nav-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .nav-links {
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .nav-links a {
        color: var(--text-color);
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        transition: all 0.2s;
    }

    .nav-links a:hover,
    .nav-links a.active {
        background: var(--primary-color);
        color: white;
    }

    .search-container {
        position: relative;
        min-width: 300px;
    }

    .search-input {
        width: 100%;
        padding: 0.75rem 1rem;
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        font-size: 1rem;
        outline: none;
        transition: border-color 0.2s;
    }

    .search-input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }

    .search-results {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        max-height: 300px;
        overflow-y: auto;
        z-index: 200;
        display: none;
        box-shadow: var(--shadow-lg);
    }

    .search-result {
        padding: 0.75rem 1rem;
        cursor: pointer;
        border-bottom: 1px solid var(--border-color);
        transition: background-color 0.2s;
    }

    .search-result:hover {
        background: var(--bg-secondary);
    }

    .search-result:last-child {
        border-bottom: none;
    }

    .content {
        padding: 2rem 0;
    }

    .video-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
    }

    .video-card {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: var(--shadow);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .video-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }

    .video-container {
        position: relative;
        width: 100%;
        height: 200px;
        background: var(--bg-secondary);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .video-container video {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .video-placeholder {
        color: var(--text-light);
        font-size: 0.875rem;
        text-align: center;
        padding: 1rem;
    }

    .card-content {
        padding: 1.5rem;
    }

    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: var(--primary-color);
    }

    .card-description {
        color: var(--text-light);
        line-height: 1.6;
    }

    .category-header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .category-title {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--primary-color);
    }

    .category-count {
        color: var(--text-light);
        font-size: 1rem;
    }

    .home-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }

    .category-preview {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        text-decoration: none;
        color: var(--text-color);
        transition: all 0.2s;
    }

    .category-preview:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        text-decoration: none;
        color: var(--text-color);
    }

    .category-preview h3 {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--primary-color);
    }

    .category-preview .count {
        color: var(--text-light);
        font-size: 0.875rem;
    }

    .warning {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 2rem;
    }

    .warning h4 {
        color: #92400e;
        margin-bottom: 0.5rem;
    }

    .warning p {
        color: #92400e;
        font-size: 0.875rem;
    }

    footer {
        background: var(--bg-secondary);
        border-top: 1px solid var(--border-color);
        padding: 2rem 0;
        margin-top: 4rem;
        text-align: center;
        color: var(--text-light);
    }

    @media (max-width: 768px) {
        .nav-container {
            flex-direction: column;
            align-items: stretch;
        }

        .nav-links {
            justify-content: center;
        }

        .search-container {
            min-width: auto;
        }

        h1 {
            font-size: 2rem;
        }

        .video-grid {
            grid-template-columns: 1fr;
        }
    }
    """

def create_base_js():
    """Create JavaScript for search functionality"""
    return """
    // Search functionality
    let searchData = [];
    
    // Initialize search
    function initSearch() {
        fetch('search-data.json')
            .then(response => response.json())
            .then(data => {
                searchData = data;
            })
            .catch(error => console.error('Error loading search data:', error));
        
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        
        if (searchInput) {
            searchInput.addEventListener('input', handleSearch);
            searchInput.addEventListener('focus', handleSearch);
            
            // Hide results when clicking outside
            document.addEventListener('click', (e) => {
                if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                    searchResults.style.display = 'none';
                }
            });
        }
    }
    
    function handleSearch(e) {
        const query = e.target.value.toLowerCase().trim();
        const searchResults = document.getElementById('searchResults');
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        const results = searchData.filter(item => 
            item.name.toLowerCase().includes(query) ||
            item.description.toLowerCase().includes(query) ||
            item.category.toLowerCase().includes(query)
        ).slice(0, 10);
        
        displaySearchResults(results, searchResults);
    }
    
    function displaySearchResults(results, container) {
        if (results.length === 0) {
            container.innerHTML = '<div class="search-result">No results found</div>';
        } else {
            container.innerHTML = results.map(result => `
                <div class="search-result" onclick="window.location.href='${result.url}'">
                    <strong>${escapeHtml(result.name)}</strong>
                    <br>
                    <small>${escapeHtml(result.category)} - ${escapeHtml(result.description.substring(0, 100))}...</small>
                </div>
            `).join('');
        }
        container.style.display = 'block';
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Initialize when DOM is loaded
    document.addEventListener('DOMContentLoaded', initSearch);
    
    // Video lazy loading
    function initVideoLazyLoading() {
        const videos = document.querySelectorAll('video[data-src]');
        
        const videoObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const video = entry.target;
                    video.src = video.dataset.src;
                    video.load();
                    videoObserver.unobserve(video);
                }
            });
        });
        
        videos.forEach(video => videoObserver.observe(video));
    }
    
    document.addEventListener('DOMContentLoaded', initVideoLazyLoading);
    """

def create_html_template(title, content, current_page=""):
    """Create HTML template with consistent structure"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} - WAN 2.2 Documentation</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>WAN 2.2 Documentation</h1>
            <p class="subtitle">AI Video Generation - Cinematic Controls & Examples</p>
        </div>
    </header>
    
    <nav>
        <div class="container nav-container">
            <div class="nav-links">
                <a href="index.html" {"class='active'" if current_page == "home" else ""}>Home</a>
                <a href="lighting.html" {"class='active'" if current_page == "lighting" else ""}>Lighting</a>
                <a href="time.html" {"class='active'" if current_page == "time" else ""}>Time of Day</a>
                <a href="shots.html" {"class='active'" if current_page == "shots" else ""}>Shot Types</a>
                <a href="composition.html" {"class='active'" if current_page == "composition" else ""}>Composition</a>
                <a href="lens.html" {"class='active'" if current_page == "lens" else ""}>Lens</a>
                <a href="colors.html" {"class='active'" if current_page == "colors" else ""}>Colors</a>
                <a href="motion.html" {"class='active'" if current_page == "motion" else ""}>Motion</a>
                <a href="emotions.html" {"class='active'" if current_page == "emotions" else ""}>Emotions</a>
                <a href="camera.html" {"class='active'" if current_page == "camera" else ""}>Camera</a>
                <a href="styles.html" {"class='active'" if current_page == "styles" else ""}>Styles</a>
                <a href="effects.html" {"class='active'" if current_page == "effects" else ""}>Effects</a>
            </div>
            <div class="search-container">
                <input type="text" id="searchInput" class="search-input" placeholder="Search videos...">
                <div id="searchResults" class="search-results"></div>
            </div>
        </div>
    </nav>
    
    <main class="container content">
        {content}
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; 2024 WAN 2.2 Documentation. Generated from video examples.</p>
            <p><small>⚠️ Video mappings are based on sequential order assumptions. Please verify content matches descriptions.</small></p>
        </div>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>"""

def generate_category_page(category_name, videos, page_key):
    """Generate HTML page for a video category"""
    
    video_cards = []
    for video in videos:
        video_cards.append(f"""
        <div class="video-card">
            <div class="video-container">
                <video data-src="{video['video_path']}" controls preload="none">
                    Your browser does not support the video tag.
                </video>
            </div>
            <div class="card-content">
                <h3 class="card-title">{html.escape(video['name'])}</h3>
                <p class="card-description">{html.escape(video['description'][:200])}{"..." if len(video['description']) > 200 else ""}</p>
            </div>
        </div>
        """)
    
    content = f"""
    <div class="warning">
        <h4>⚠️ Important Note</h4>
        <p>These video mappings are based on sequential order assumptions. Please verify that each video matches its description before using in production.</p>
    </div>
    
    <div class="category-header">
        <h2 class="category-title">{html.escape(category_name)}</h2>
        <p class="category-count">{len(videos)} video examples</p>
    </div>
    
    <div class="video-grid">
        {"".join(video_cards)}
    </div>
    """
    
    return create_html_template(category_name, content, page_key)

def generate_home_page(categories):
    """Generate the home page with category overview"""
    
    category_cards = []
    category_names = {
        'lighting': 'Lighting Types',
        'time': 'Time of Day',
        'shots': 'Shot Types',
        'composition': 'Composition',
        'lens': 'Lens Types',
        'colors': 'Color Tones',
        'motion': 'Motion & Actions',
        'emotions': 'Character Emotions',
        'camera': 'Camera Movement',
        'styles': 'Visual Styles',
        'effects': 'Special Effects'
    }
    
    for key, videos in categories.items():
        if videos:  # Only show categories with videos
            category_cards.append(f"""
            <a href="{key}.html" class="category-preview">
                <h3>{category_names.get(key, key.title())}</h3>
                <p class="count">{len(videos)} examples</p>
            </a>
            """)
    
    content = f"""
    <div class="warning">
        <h4>⚠️ Important Note About Video Mappings</h4>
        <p>This documentation maps videos based on sequential order assumptions from the source data. The first video in the JSON array is mapped to the first table entry in the documentation, and so on. This may not be accurate - please verify that each video matches its description before using in production.</p>
    </div>
    
    <div class="category-header">
        <h2 class="category-title">WAN 2.2 Video Examples</h2>
        <p>Explore cinematic controls and video generation examples by category</p>
    </div>
    
    <div class="home-grid">
        {"".join(category_cards)}
    </div>
    
    <div style="margin-top: 3rem;">
        <h3>About WAN 2.2</h3>
        <p>WAN 2.2 is an advanced AI video generation model that offers comprehensive cinematic controls including lighting, composition, camera movement, and visual styles. This documentation provides examples of each control type to help you create professional-quality videos.</p>
        
        <h4 style="margin-top: 2rem;">Key Features:</h4>
        <ul style="margin-left: 2rem; margin-top: 1rem;">
            <li><strong>Cinematic Lighting Control:</strong> From natural sunlight to artificial studio lighting</li>
            <li><strong>Professional Shot Types:</strong> Close-ups, wide shots, and everything in between</li>
            <li><strong>Dynamic Camera Movement:</strong> Pans, tilts, tracking shots, and more</li>
            <li><strong>Visual Styles:</strong> Animation styles, artistic effects, and visual treatments</li>
            <li><strong>Motion Control:</strong> Precise control over character actions and scene dynamics</li>
        </ul>
    </div>
    """
    
    return create_html_template("Home", content, "home")

def create_search_data(categories):
    """Create JSON search data"""
    search_items = []
    
    category_names = {
        'lighting': 'Lighting Types',
        'time': 'Time of Day', 
        'shots': 'Shot Types',
        'composition': 'Composition',
        'lens': 'Lens Types',
        'colors': 'Color Tones',
        'motion': 'Motion & Actions',
        'emotions': 'Character Emotions',
        'camera': 'Camera Movement',
        'styles': 'Visual Styles',
        'effects': 'Special Effects'
    }
    
    for category_key, videos in categories.items():
        category_name = category_names.get(category_key, category_key.title())
        for video in videos:
            search_items.append({
                'name': video['name'],
                'description': video['description'],
                'category': category_name,
                'url': f'{category_key}.html#{video["safe_name"]}'
            })
    
    return json.dumps(search_items, indent=2)

def main():
    """Generate the complete HTML documentation site"""
    
    # Create docs directory
    docs_dir = Path("../docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Parse markdown content
    print("Parsing markdown content...")
    categories = parse_markdown_content()
    
    # Create CSS file
    print("Creating CSS file...")
    with open(docs_dir / "styles.css", "w") as f:
        f.write(create_base_css())
    
    # Create JavaScript file  
    print("Creating JavaScript file...")
    with open(docs_dir / "script.js", "w") as f:
        f.write(create_base_js())
    
    # Create search data
    print("Creating search data...")
    with open(docs_dir / "search-data.json", "w") as f:
        f.write(create_search_data(categories))
    
    # Generate home page
    print("Generating home page...")
    with open(docs_dir / "index.html", "w") as f:
        f.write(generate_home_page(categories))
    
    # Generate category pages
    category_names = {
        'lighting': 'Lighting Types',
        'time': 'Time of Day',
        'shots': 'Shot Types', 
        'composition': 'Composition',
        'lens': 'Lens Types',
        'colors': 'Color Tones',
        'motion': 'Motion & Actions',
        'emotions': 'Character Emotions',
        'camera': 'Camera Movement',
        'styles': 'Visual Styles',
        'effects': 'Special Effects'
    }
    
    for category_key, videos in categories.items():
        if videos:  # Only create pages for categories with videos
            category_name = category_names.get(category_key, category_key.title())
            print(f"Generating {category_name} page...")
            
            with open(docs_dir / f"{category_key}.html", "w") as f:
                f.write(generate_category_page(category_name, videos, category_key))
    
    print(f"\n✅ HTML documentation generated successfully!")
    print(f"📁 Output directory: {docs_dir.absolute()}")
    print(f"🌐 Open docs/index.html in your browser to view the documentation")
    
    # Print statistics
    total_videos = sum(len(videos) for videos in categories.values())
    categories_with_content = sum(1 for videos in categories.values() if videos)
    
    print(f"\n📊 Statistics:")
    print(f"   Total videos: {total_videos}")
    print(f"   Categories with content: {categories_with_content}")
    
    for category_key, videos in categories.items():
        if videos:
            category_name = category_names.get(category_key, category_key.title())
            print(f"   {category_name}: {len(videos)} videos")

if __name__ == "__main__":
    main()