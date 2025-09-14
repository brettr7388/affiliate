/**
 * Eco Pet Guide Homepage JavaScript
 * Handles data fetching, A/B testing, tracking, and interactions
 */

// Global state
let currentOffset = 0;
let currentLimit = 24;
let currentTab = 'trending';
let currentCategory = null;
let isLoading = false;
let abVariant = 'A';
let lastShuffleTime = 0;
let shuffleInterval = 30 * 60 * 1000; // 30 minutes in milliseconds
let scrollObserver = null;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    init();
    loadProductComparisons();
});

/**
 * Initialize the homepage
 */
function init() {
    // Set up A/B testing
    initABTesting();
    
    // Load initial data
    loadFeaturedRoutes();
    loadArticles('trending');
    loadFooterStats();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize scroll animations
    initScrollAnimations();
    
    // Update structured data with actual articles
    updateStructuredData();
    
    // Set up periodic refresh for dynamic content
    setupPeriodicRefresh();
}

/**
 * A/B Testing Setup
 */
function initABTesting() {
    // Get or set A/B variant (persistent for session)
    const storedVariant = localStorage.getItem('ab_hero_variant');
    if (storedVariant) {
        abVariant = storedVariant;
    } else {
        abVariant = Math.random() < 0.5 ? 'A' : 'B';
        localStorage.setItem('ab_hero_variant', abVariant);
    }
    
    // Update hero content based on variant
    const heroHeadline = document.getElementById('hero-headline');
    const heroCTA = document.getElementById('hero-primary-cta');
    
    if (abVariant === 'B') {
        heroHeadline.textContent = 'Greener Dog Essentials: Trusted Picks That Actually Last';
        heroCTA.textContent = 'See Editor\'s Picks';
    }
    
    // Track impression
    trackABTest('hero', abVariant, 'impression');
}

/**
 * Event Listeners Setup
 */
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', handleTabClick);
    });
    
    // Category dropdown
    const categoryButton = document.querySelector('[data-tab="categories"]');
    const categoryDropdown = document.getElementById('category-dropdown');
    
    if (categoryButton && categoryDropdown) {
        categoryButton.addEventListener('click', (e) => {
            e.stopPropagation();
            categoryDropdown.classList.toggle('hidden');
        });
    }
    
    // Category selection
    document.querySelectorAll('[data-category]').forEach(button => {
        button.addEventListener('click', handleCategoryClick);
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        if (categoryDropdown) {
            categoryDropdown.classList.add('hidden');
        }
    });
    
    // Load more button
    const loadMoreBtn = document.getElementById('load-more');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', loadMoreArticles);
    }
    
    // Hero CTA
    const heroCTA = document.getElementById('hero-primary-cta');
    if (heroCTA) {
        heroCTA.addEventListener('click', handleHeroCTA);
    }
    
    // Newsletter form
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleNewsletterSubmit);
    }
    

}

/**
 * Handle tab clicks
 */
function handleTabClick(e) {
    const tab = e.target.dataset.tab;
    if (tab === 'categories') return; // Handled separately
    
    // Update active state
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    e.target.classList.add('active');
    
    // Reset pagination
    currentOffset = 0;
    currentTab = tab;
    currentCategory = null;
    
    // Load articles
    loadArticles(tab);
    
    // Track tab change
    trackEvent('tab_change', { tab });
}

/**
 * Handle category clicks
 */
function handleCategoryClick(e) {
    const category = e.target.dataset.category;
    
    // Update active state
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    const categoriesBtn = document.querySelector('[data-tab="categories"]');
    if (categoriesBtn) {
        categoriesBtn.classList.add('active');
    }
    
    // Hide dropdown
    const categoryDropdown = document.getElementById('category-dropdown');
    if (categoryDropdown) {
        categoryDropdown.classList.add('hidden');
    }
    
    // Reset pagination
    currentOffset = 0;
    currentTab = 'categories';
    currentCategory = category;
    
    // Load articles
    loadArticles('categories', category);
    
    // Track category change
    trackEvent('tab_change', { tab: 'categories', category });
}



/**
 * Load featured routes
 */
async function loadFeaturedRoutes() {
    try {
        const response = await fetch('/api/routes/featured?limit=6');
        const routes = await response.json();
        
        renderFeaturedRoutes(routes);
    } catch (error) {
        console.error('Failed to load featured routes:', error);
        // Show fallback content
        renderFeaturedRoutesFallback();
    }
}

/**
 * Render featured routes
 */
function renderFeaturedRoutes(routes) {
    const container = document.getElementById('top-picks-grid');
    if (!container) return;
    
    if (routes.length === 0) {
        container.innerHTML = '<div class="col-span-full text-center py-12 text-gray-500">No featured products available yet.</div>';
        return;
    }
    
    container.innerHTML = routes.map(route => `
        <div class="card-animate bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 overflow-hidden">
            <div class="relative">
                <img src="${route.image}?v=${Date.now()}" alt="${route.label}" class="w-full h-56 object-contain bg-gray-50 p-2" loading="lazy" decoding="async" onerror="this.src='/images/library/placeholder-product.jpg?v=${Date.now()}'">
                <div class="absolute top-4 left-4 bg-eco-green-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                    Featured
                </div>
            </div>
            <div class="p-6">
                <h3 class="font-semibold text-lg mb-2 text-gray-900">${route.label}</h3>
                <a href="${route.dest_url}" 
                   class="inline-block w-full bg-eco-green-600 hover:bg-eco-green-700 text-white font-semibold py-3 px-6 rounded-lg text-center transition-colors duration-200"
                   data-track="affiliate"
                   data-slug="${route.slug}"
                   onclick="handleAffiliateClick(event, '${route.slug}', '${route.dest_url}')">
                    View Deal
                </a>
            </div>
        </div>
    `).join('');
    
    // Observe the new cards for scroll animations
    observeCards(container);
}

/**
 * Fallback for featured routes
 */
function renderFeaturedRoutesFallback() {
    const container = document.getElementById('top-picks-grid');
    if (!container) return;
    
    container.innerHTML = `
        <div class="col-span-full text-center py-12">
            <div class="text-gray-500 mb-4">
                <span class="text-4xl">🐕</span>
            </div>
            <p class="text-gray-600">Featured products will appear here once routes are configured.</p>
        </div>
    `;
}

/**
 * Set up periodic refresh for dynamic content
 */
function setupPeriodicRefresh() {
    // Check for refresh every 5 minutes
    setInterval(checkForRefresh, 5 * 60 * 1000);
    
    // Also check when user returns to tab (visibility change)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            checkForRefresh();
        }
    });
    
    // Initial timestamp
    lastShuffleTime = Date.now();
}

/**
 * Check if content should be refreshed
 */
function checkForRefresh() {
    const now = Date.now();
    const timeSinceLastShuffle = now - lastShuffleTime;
    
    // Only refresh if on trending or categories tab (not latest)
    const shouldRefresh = (
        timeSinceLastShuffle > shuffleInterval && 
        (currentTab === 'trending' || currentTab === 'categories') &&
        !isLoading
    );
    
    if (shouldRefresh) {
        console.log('🔄 Refreshing content for fresh article order...');
        refreshCurrentView();
        lastShuffleTime = now;
        
        // Show subtle notification
        showRefreshNotification();
    }
}

/**
 * Refresh current view with new article order
 */
function refreshCurrentView() {
    // Reset offset for fresh load
    currentOffset = 0;
    
    // Reload current tab
    loadArticles(currentTab, currentCategory);
}

/**
 * Show subtle refresh notification
 */
function showRefreshNotification() {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'refresh-notification';
    notification.innerHTML = '✨ Fresh content loaded!';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
        z-index: 1000;
        opacity: 0;
        transform: translateX(100px);
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

/**
 * Load articles
 */
async function loadArticles(tab, category = null) {
    if (isLoading) return;
    isLoading = true;
    
    try {
        let url = `/api/articles?limit=${currentLimit}&offset=${currentOffset}`;
        
        if (tab === 'trending') {
            // Use shuffled sorting for trending to keep content fresh
            url += `&sort=shuffled`;
        } else if (tab === 'categories' && category) {
            url += `&tag=${encodeURIComponent(category)}&sort=shuffled`;
        } else {
            // Latest tab uses chronological order
            url += `&sort=new`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (currentOffset === 0) {
            // First load - replace content
            renderArticles(data.items, true);
        } else {
            // Load more - append content
            renderArticles(data.items, false);
        }
        
        // Update load more button
        const loadMoreBtn = document.getElementById('load-more');
        if (loadMoreBtn) {
            if (data.items.length < currentLimit || currentOffset + data.items.length >= data.total) {
                loadMoreBtn.style.display = 'none';
            } else {
                loadMoreBtn.style.display = 'block';
            }
        }
        
        // Update structured data
        if (currentOffset === 0) {
            updateStructuredData(data.items.slice(0, 10));
        }
        
    } catch (error) {
        console.error('Failed to load articles:', error);
        if (currentOffset === 0) {
            renderArticlesFallback();
        }
    } finally {
        isLoading = false;
    }
}

/**
 * Render articles
 */
function renderArticles(articles, replace = true) {
    const container = document.getElementById('article-grid');
    if (!container) return;
    
    if (articles.length === 0) {
        if (replace) {
            container.innerHTML = '<div class="col-span-full text-center py-12 text-gray-500">No articles found.</div>';
        }
        return;
    }
    
    // Add category detection for each article
    const articlesHTML = articles.map(article => {
        // Detect category from title and slug
        const title_lower = article.title.toLowerCase();
        const slug_lower = article.slug.toLowerCase();
        let category = 'all';
        
        if (title_lower.includes('toy') || title_lower.includes('play') || title_lower.includes('kong') || title_lower.includes('west paw') || slug_lower.includes('toy')) {
            category = 'toy';
        } else if (title_lower.includes('poop bag') || title_lower.includes('biodegradable') || title_lower.includes('waste') || title_lower.includes('bag') || slug_lower.includes('bag')) {
            category = 'bag';
        } else if (title_lower.includes('bowl') || title_lower.includes('feeding') || title_lower.includes('dish') || slug_lower.includes('bowl')) {
            category = 'bowl';
        } else if (title_lower.includes('leash') || title_lower.includes('walking') || title_lower.includes('lead') || slug_lower.includes('leash')) {
            category = 'leash';
        } else if (title_lower.includes('bed') || title_lower.includes('sleep') || title_lower.includes('comfort') || title_lower.includes('orthopedic') || slug_lower.includes('bed')) {
            category = 'bed';
        } else if (title_lower.includes('treat') || title_lower.includes('snack') || title_lower.includes('food') || slug_lower.includes('treat')) {
            category = 'treat';
        }
        
        return `
        <article class="card-animate bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 overflow-hidden cursor-pointer"
                 data-track="article"
                 data-slug="${article.slug}"
                 onclick="handleArticleClick(event, '${article.slug}')">
            <div class="relative">
                <div data-product-category="${article.category || 'all'}"><img src="${article.heroImage}" alt="${article.title}" class="w-full h-56 object-contain bg-gray-50 p-2" loading="lazy" decoding="async" onerror="this.src='/images/library/placeholder-article.jpg'"></div>
                ${article.tags.length > 0 ? `
                    <div class="absolute top-4 left-4">
                        <span class="bg-eco-green-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                            ${article.tags[0]}
                        </span>
                    </div>
                ` : ''}
            </div>
            <div class="p-6">
                <h3 class="font-semibold text-lg mb-2 text-gray-900 line-clamp-2">${article.title}</h3>
                <p class="text-gray-600 text-sm mb-4 line-clamp-3">${article.excerpt}</p>
                <div class="flex items-center justify-between text-xs text-gray-500">
                    <span>${article.estimatedReadMin} min read</span>
                    <span>${formatDate(article.publishedAt)}</span>
                </div>
            </div>
        </article>
        `;
    }).join('');
    
    if (replace) {
        container.innerHTML = articlesHTML;
    } else {
        container.insertAdjacentHTML('beforeend', articlesHTML);
        
        // Announce to screen readers
        const announcement = document.getElementById('announcements');
        if (announcement) {
            announcement.textContent = `Loaded ${articles.length} more articles`;
        }
    }
    
    // Observe the new cards for scroll animations
    observeCards(container);
}

/**
 * Fallback for articles
 */
function renderArticlesFallback() {
    const container = document.getElementById('article-grid');
    if (!container) return;
    
    container.innerHTML = `
        <div class="col-span-full text-center py-12">
            <div class="text-gray-500 mb-4">
                <span class="text-4xl">📚</span>
            </div>
            <p class="text-gray-600">Articles will appear here once content is generated.</p>
        </div>
    `;
}

/**
 * Load more articles
 */
function loadMoreArticles() {
    currentOffset += currentLimit;
    loadArticles(currentTab, currentCategory);
    
    trackEvent('load_more', { offset: currentOffset, tab: currentTab, category: currentCategory });
}

/**
 * Load footer stats - REMOVED per user request
 */
async function loadFooterStats() {
    // Stats removed from footer per user request
    return;
}

/**
 * Handle hero CTA click
 */
async function handleHeroCTA(e) {
    e.preventDefault();
    
    // Track conversion
    trackABTest('hero', abVariant, 'convert');
    trackEvent('hero_cta', { variant: abVariant });
    
    // Get first featured route
    try {
        const response = await fetch('/api/routes/featured?limit=1');
        const routes = await response.json();
        
        if (routes.length > 0) {
            const route = routes[0];
            handleAffiliateClick(e, route.slug, route.dest_url);
        } else {
            // Fallback to articles section
            const articlesSection = document.getElementById('article-tabs');
            if (articlesSection) {
                articlesSection.scrollIntoView({ behavior: 'smooth' });
            }
        }
    } catch (error) {
        console.error('Failed to get featured route:', error);
        const articlesSection = document.getElementById('article-tabs');
        if (articlesSection) {
            articlesSection.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

/**
 * Handle affiliate link clicks
 */
function handleAffiliateClick(e, slug, href) {
    e.preventDefault();
    
    // Get UTM parameters
    const utm = getStoredUTM();
    
    // Add UTM to href if present
    let finalHref = href;
    if (utm && Object.keys(utm).length > 0) {
        try {
            const url = new URL(href, window.location.origin);
            Object.entries(utm).forEach(([key, value]) => {
                url.searchParams.set(key, value);
            });
            finalHref = url.toString();
        } catch (e) {
            // If URL parsing fails, use original href
            finalHref = href;
        }
    }
    
    // Track the click
    trackEvent('affiliate_click', { slug, href: finalHref, utm });
    
    // Navigate
    window.open(finalHref, '_blank');
}

/**
 * Handle article clicks
 */
function handleArticleClick(e, slug) {
    e.preventDefault();
    
    // Track the click
    trackEvent('article_open', { slug });
    
    // Navigate to article
    window.location.href = `/content/${slug}.html`;
}

/**
 * Handle newsletter submission
 */
async function handleNewsletterSubmit(e) {
    e.preventDefault();
    
    const emailInput = document.getElementById('newsletter-email');
    if (!emailInput) return;
    
    const email = emailInput.value;
    const button = e.target.querySelector('button[type="submit"]');
    if (!button) return;
    
    const originalText = button.textContent;
    
    button.textContent = 'Subscribing...';
    button.disabled = true;
    
    try {
        // Submit to API
        const response = await fetch('/api/newsletter/subscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        
        if (response.ok) {
            const data = await response.json();
            showNewsletterPopup(data.message || 'Successfully subscribed!', 'success');
            emailInput.value = '';
        } else {
            throw new Error('Subscription failed');
        }
    } catch (error) {
        console.error('Newsletter subscription error:', error);
        showNewsletterPopup('Something went wrong. Please try again.', 'error');
    }
    
    // Reset button
    button.textContent = originalText;
    button.disabled = false;
}

/**
 * Show newsletter subscription popup
 */
function showNewsletterPopup(message, type = 'success') {
    // Remove existing popup if any
    const existingPopup = document.querySelector('.newsletter-popup');
    if (existingPopup) {
        existingPopup.remove();
    }
    
    // Create popup element
    const popup = document.createElement('div');
    popup.className = 'newsletter-popup';
    
    const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
    const icon = type === 'success' ? '✅' : '❌';
    
    popup.innerHTML = `
        <div class="fixed top-4 right-4 ${bgColor} text-white px-6 py-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300 ease-out">
            <div class="flex items-center space-x-3">
                <span class="text-xl">${icon}</span>
                <span class="font-medium">${message}</span>
            </div>
        </div>
    `;
    
    document.body.appendChild(popup);
    
    const popupContent = popup.querySelector('div');
    
    // Animate in
    setTimeout(() => {
        popupContent.style.transform = 'translateX(0)';
    }, 100);
    
    // Animate out and remove after 4 seconds
    setTimeout(() => {
        popupContent.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (popup.parentNode) {
                popup.parentNode.removeChild(popup);
            }
        }, 300);
    }, 4000);
}

/**
 * Tracking Functions
 */

/**
 * Track general events
 */
function trackEvent(type, payload = {}) {
    // Respect Do Not Track
    if (navigator.doNotTrack === "1") return;
    
    const data = {
        slug: payload.slug || 'homepage',
        href: payload.href || window.location.href,
        utm: payload.utm || getStoredUTM(),
        event_type: type,
        ...payload
    };
    
    // Debounced tracking
    debounce(() => {
        if (navigator.sendBeacon) {
            navigator.sendBeacon('/api/clicks', JSON.stringify(data));
        } else {
            fetch('/api/clicks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).catch(console.error);
        }
    }, 100)();
}

/**
 * Track A/B tests
 */
function trackABTest(area, variant, action) {
    if (navigator.doNotTrack === "1") return;
    
    const data = { area, variant, action };
    
    const endpoint = action === 'convert' ? '/api/ab/convert' : '/api/ab/impression';
    
    fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).catch(console.error);
}

/**
 * Utility Functions
 */

/**
 * Get stored UTM parameters
 */
function getStoredUTM() {
    try {
        const stored = sessionStorage.getItem('utm');
        return stored ? JSON.parse(stored) : {};
    } catch {
        return {};
    }
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric',
            year: 'numeric'
        });
    } catch {
        return 'Recent';
    }
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Update structured data with articles
 */
function updateStructuredData(articles = []) {
    if (articles.length === 0) return;
    
    const structuredData = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Eco Pet Guide",
        "description": "Sustainable dog products and eco-friendly pet care guides",
        "url": window.location.origin,
        "publisher": {
            "@type": "Organization",
            "name": "Eco Pet Guide"
        },
        "blogPost": articles.map(article => ({
            "@type": "BlogPosting",
            "headline": article.title,
            "description": article.excerpt,
            "url": `${window.location.origin}/content/${article.slug}.html`,
            "datePublished": article.publishedAt,
            "author": {
                "@type": "Organization",
                "name": "Eco Pet Guide"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Eco Pet Guide"
            }
        }))
    };
    
    const scriptTag = document.getElementById('structured-data');
    if (scriptTag) {
        scriptTag.textContent = JSON.stringify(structuredData);
    }
}

/**
 * Initialize scroll animations
 */
function initScrollAnimations() {
    const observerOptions = {
        root: null, // Use viewport as the root
        threshold: 0.1, // Trigger when 10% of the element is visible
        rootMargin: '50px 0px 50px 0px' // Trigger before element fully enters/exits viewport
    };

    scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Card is entering viewport - animate in
                entry.target.classList.add('animate-in');
                entry.target.classList.remove('animate-out');
            } else {
                // Card is leaving viewport - animate out
                entry.target.classList.remove('animate-in');
                entry.target.classList.add('animate-out');
            }
            // Keep observing to handle both directions
        });
    }, observerOptions);
}

/**
 * Observe cards for scroll animations
 */
function observeCards(container) {
    if (!scrollObserver) return;
    
    const cards = container.querySelectorAll('.card-animate');
    cards.forEach(card => {
        scrollObserver.observe(card);
    });
}

/**
 * Load and render product comparisons dynamically
 */
async function loadProductComparisons() {
    const loadingElement = document.getElementById('comparisons-loading');
    const contentElement = document.getElementById('comparisons-content');
    const noComparisonsElement = document.getElementById('no-comparisons');
    
    try {
        const response = await fetch('/api/product-comparisons');
        const data = await response.json();
        
        // Hide loading
        if (loadingElement) loadingElement.style.display = 'none';
        
        if (data.comparisons && data.comparisons.length > 0) {
            // Render comparisons
            contentElement.innerHTML = data.comparisons.map(comparison => 
                renderComparison(comparison)
            ).join('');
            
            // Apply scroll animations to new content
            observeCards(contentElement);
        } else {
            // Show no comparisons message
            if (noComparisonsElement) noComparisonsElement.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error loading product comparisons:', error);
        
        // Hide loading and show error message
        if (loadingElement) loadingElement.style.display = 'none';
        if (contentElement) {
            contentElement.innerHTML = `
                <div class="text-center py-8 text-red-500">
                    <div class="text-4xl mb-4">⚠️</div>
                    <p class="text-lg">Failed to load product comparisons</p>
                    <p class="text-sm">Please try refreshing the page</p>
                </div>
            `;
        }
    }
}

/**
 * Render a single product comparison
 */
function renderComparison(comparison) {
    if (comparison.display_type === 'table') {
        return renderTableComparison(comparison);
    } else if (comparison.display_type === 'cards') {
        return renderCardsComparison(comparison);
    }
    return '';
}

/**
 * Render table-style comparison
 */
function renderTableComparison(comparison) {
    const tableHeaders = getTableHeaders(comparison.products[0]);
    const tableRows = comparison.products.map((product, index) => 
        renderTableRow(product, index % 2 === 1)
    ).join('');
    
    return `
        <div class="mb-12 card-animate">
            <h3 class="text-2xl font-semibold mb-6">${comparison.title}</h3>
            <div class="overflow-x-auto">
                <table class="w-full border-collapse border border-gray-300">
                    <thead>
                        <tr class="bg-eco-green-100">
                            ${tableHeaders}
                        </tr>
                    </thead>
                    <tbody>
                        ${tableRows}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

/**
 * Generate table headers based on product properties
 */
function getTableHeaders(sampleProduct) {
    const headers = ['Product'];
    
    if (sampleProduct.material) headers.push('Material');
    if (sampleProduct.durability) headers.push('Durability');
    if (sampleProduct.price) headers.push('Price');
    if (sampleProduct.rating) headers.push('Rating');
    
    headers.push('Buy');
    
    return headers.map(header => 
        `<th class="border border-gray-300 px-4 py-2 text-center">${header}</th>`
    ).join('');
}

/**
 * Render a table row for a product
 */
function renderTableRow(product, isEven) {
    const rowClass = isEven ? 'bg-gray-50' : '';
    let cells = `<td class="border border-gray-300 px-4 py-2 font-semibold">${product.name}</td>`;
    
    if (product.material) {
        cells += `<td class="border border-gray-300 px-4 py-2 text-center">${product.material}</td>`;
    }
    if (product.durability) {
        cells += `<td class="border border-gray-300 px-4 py-2 text-center">${product.durability}</td>`;
    }
    if (product.price) {
        cells += `<td class="border border-gray-300 px-4 py-2 text-center">${product.price}</td>`;
    }
    if (product.rating) {
        cells += `<td class="border border-gray-300 px-4 py-2 text-center">${product.rating}</td>`;
    }
    
    const badgeText = product.badge || 'Buy Now';
    cells += `
        <td class="border border-gray-300 px-4 py-2 text-center">
            <a href="${product.link}" class="bg-eco-green-600 text-white px-3 py-1 rounded text-sm hover:bg-eco-green-700 transition-colors">
                ${badgeText}
            </a>
        </td>
    `;
    
    return `<tr class="${rowClass}">${cells}</tr>`;
}

/**
 * Render cards-style comparison
 */
function renderCardsComparison(comparison) {
    const cards = comparison.products.map(product => 
        renderProductCard(product)
    ).join('');
    
    return `
        <div class="mb-12 card-animate">
            <h3 class="text-2xl font-semibold mb-6">${comparison.title}</h3>
            <div class="grid md:grid-cols-3 gap-6">
                ${cards}
            </div>
        </div>
    `;
}

/**
 * Render a single product card
 */
function renderProductCard(product) {
    const badgeColor = product.badge_color === 'eco-green' ? 'bg-eco-green-600' : 'bg-gray-600';
    const badgeText = product.badge || 'Buy Now';
    
    return `
        <div class="border border-gray-200 rounded-lg p-6 text-center hover:shadow-lg transition-shadow">
            <h4 class="font-semibold text-lg mb-2">${product.name}</h4>
            <div class="text-2xl mb-2">${product.rating || '⭐⭐⭐⭐'}</div>
            <p class="text-sm text-gray-600 mb-4">${product.description || ''}</p>
            <div class="text-lg font-bold mb-4">${product.price || ''}</div>
            <a href="${product.link}" class="${badgeColor} text-white px-4 py-2 rounded inline-block hover:opacity-90 transition-opacity">
                ${badgeText}
            </a>
        </div>
    `;
}
