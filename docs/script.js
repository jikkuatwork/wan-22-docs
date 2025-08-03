
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
    