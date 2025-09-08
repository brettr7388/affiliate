const base = location.origin;

function getHeaders() {
    return {
        "Content-Type": "application/json",
        "X-Admin-Token": localStorage.getItem("ADMIN_TOKEN") || ""
    };
}

function showStatus(elementId, message, type = 'info') {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="status ${type}">${message}</div>`;
    setTimeout(() => {
        element.innerHTML = '';
    }, 5000);
}

function saveToken() {
    const token = document.getElementById('token').value;
    localStorage.setItem("ADMIN_TOKEN", token);
    showStatus('routeStatus', 'Token saved successfully!', 'success');
}

function clearRouteForm() {
    document.getElementById('slug').value = '';
    document.getElementById('offer').value = '';
    document.getElementById('variant').value = 'A';
    document.getElementById('dest').value = '';
    showStatus('routeStatus', 'Form cleared!', 'info');
}

async function saveRoute() {
    const body = {
        slug: document.getElementById('slug').value,
        offer: document.getElementById('offer').value,
        variant: document.getElementById('variant').value || "A",
        dest_url: document.getElementById('dest').value
    };
    
    try {
        const r = await fetch(base + "/admin/route", {
            method: "POST", 
            headers: getHeaders(), 
            body: JSON.stringify(body)
        });
        const result = await r.text();
        showStatus('routeStatus', `Route saved: ${result}`, 'success');
        loadRoutes();
        loadStats();
    } catch (error) {
        showStatus('routeStatus', `Error: ${error.message}`, 'error');
    }
}

async function loadRoutes() {
    try {
        const r = await fetch(base + "/admin/routes", {headers: getHeaders()});
        const data = await r.json();
        document.getElementById('routes').textContent = JSON.stringify(data, null, 2);
        
        // Update dropdowns with latest routes
        loadProductDropdown();
    } catch (error) {
        document.getElementById('routes').textContent = `Error loading routes: ${error.message}`;
    }
}

async function loadProductDropdown() {
    try {
        const r = await fetch(base + "/admin/routes", {headers: getHeaders()});
        
        if (!r.ok) {
            throw new Error(`HTTP ${r.status}: ${await r.text()}`);
        }
        
        const routes = await r.json();
        console.log('Loaded routes:', routes);
        
        // Update article product dropdown
        const articleDropdown = document.getElementById('articleProduct');
        if (articleDropdown) {
            articleDropdown.innerHTML = '<option value="">Choose a product to write about...</option>';
        }
        
        // Update image product dropdown
        const imageDropdown = document.getElementById('imageProduct');
        if (imageDropdown) {
            imageDropdown.innerHTML = '<option value="">Choose a product...</option>';
        }
        
        routes.forEach(route => {
            // Article dropdown
            if (articleDropdown) {
                const articleOption = document.createElement('option');
                articleOption.value = route.slug;
                articleOption.textContent = `${route.offer} (${route.slug})`;
                articleDropdown.appendChild(articleOption);
            }
            
            // Image dropdown
            if (imageDropdown) {
                const imageOption = document.createElement('option');
                imageOption.value = route.slug;
                imageOption.textContent = `${route.offer} (${route.slug})`;
                imageDropdown.appendChild(imageOption);
            }
        });
        
        console.log(`✅ Populated dropdowns with ${routes.length} products`);
    } catch (error) {
        console.error('Error loading product dropdown:', error);
        showStatus('imageStatus', `Dropdown error: ${error.message}`, 'error');
    }
}

async function loadClicks() {
    try {
        const r = await fetch(base + "/admin/clicks?days=7", {headers: getHeaders()});
        const data = await r.json();
        document.getElementById('clicks').textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById('clicks').textContent = `Error loading clicks: ${error.message}`;
    }
}

async function loadSubscribers() {
    try {
        const r = await fetch(base + "/api/newsletter/subscribers", {headers: getHeaders()});
        const data = await r.json();
        
        // Update stats
        const statsEl = document.getElementById('subscribers-stats');
        statsEl.innerHTML = `📊 Total Subscribers: <span style="color: #28a745;">${data.total}</span>`;
        
        // Update subscriber list
        const subscribersEl = document.getElementById('subscribers');
        if (data.subscribers && data.subscribers.length > 0) {
            const subscribersList = data.subscribers.map((sub, index) => {
                const date = new Date(sub.subscribed_at).toLocaleDateString();
                const time = new Date(sub.subscribed_at).toLocaleTimeString();
                return `
                    <div style="padding: 8px; margin: 4px 0; background: white; border-radius: 4px; border-left: 3px solid #28a745;">
                        <div style="font-weight: bold; color: #333;">${index + 1}. ${sub.email}</div>
                        <div style="font-size: 12px; color: #666;">
                            📅 ${date} at ${time} | 🌐 ${sub.ip_address}
                        </div>
                    </div>
                `;
            }).join('');
            subscribersEl.innerHTML = subscribersList;
        } else {
            subscribersEl.innerHTML = '<div style="text-align: center; color: #666; padding: 20px;">No subscribers yet.</div>';
        }
    } catch (error) {
        const subscribersEl = document.getElementById('subscribers');
        subscribersEl.innerHTML = `<div style="color: red; padding: 10px;">Error loading subscribers: ${error.message}</div>`;
    }
}

async function loadStats() {
    try {
        // Load total clicks
        const healthR = await fetch(base + "/health");
        const healthData = await healthR.json();
        document.getElementById('totalClicks').textContent = healthData.clicks || 0;

        // Load today's clicks
        const todayR = await fetch(base + "/admin/clicks?days=1", {headers: getHeaders()});
        const todayData = await todayR.json();
        const todayTotal = todayData.reduce((sum, item) => sum + item.clicks, 0);
        document.getElementById('todayClicks').textContent = todayTotal;

        // Load weekly clicks
        const weekR = await fetch(base + "/admin/clicks?days=7", {headers: getHeaders()});
        const weekData = await weekR.json();
        const weekTotal = weekData.reduce((sum, item) => sum + item.clicks, 0);
        document.getElementById('weeklyClicks').textContent = weekTotal;

        // Load route count
        const routesR = await fetch(base + "/admin/routes", {headers: getHeaders()});
        const routesData = await routesR.json();
        document.getElementById('totalRoutes').textContent = routesData.length;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function checkHealth() {
    try {
        const r = await fetch(base + "/health");
        const data = await r.json();
        document.getElementById('health').textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById('health').textContent = `Error checking health: ${error.message}`;
    }
}

async function generateImages() {
    const product = document.getElementById('imageProduct').value;
    const style = document.getElementById('imageStyle').value;
    const count = parseInt(document.getElementById('imageCount').value);
    
    if (!product) {
        showStatus('imageStatus', 'Please select a product first!', 'error');
        return;
    }

    // Show loading bar
    showImageLoading(true);
    updateImageProgress(0, `Starting image generation for ${count} images...`);

    try {
        const r = await fetch(base + "/admin/generate-images", {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify({
                product: product,
                style: style,
                count: count
            })
        });
        
        if (!r.ok) {
            const errorText = await r.text();
            throw new Error(`Server error: ${errorText}`);
        }
        
        // Simulate progress updates since we don't have streaming yet
        for (let i = 1; i <= count; i++) {
            const progress = (i / count) * 100;
            updateImageProgress(progress, `Generating image ${i}/${count}...`);
            await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate delay
        }
        
        const result = await r.json();
        if (result.ok && result.images) {
            displayGeneratedImages(result.images);
            showImageLoading(false);
            showStatus('imageStatus', `✅ Generated ${result.images.length} images successfully!`, 'success');
        } else {
            showImageLoading(false);
            showStatus('imageStatus', `❌ Error: ${result.detail || 'Unknown error'}`, 'error');
        }
        
    } catch (error) {
        showImageLoading(false);
        showStatus('imageStatus', `❌ Error: ${error.message}`, 'error');
    }
}

function showImageLoading(show) {
    const container = document.getElementById('imageLoadingContainer');
    container.style.display = show ? 'block' : 'none';
    if (!show) {
        updateImageProgress(0, '');
    }
}

function updateImageProgress(percentage, message) {
    const bar = document.getElementById('imageLoadingBar');
    const text = document.getElementById('imageLoadingText');
    
    bar.style.width = percentage + '%';
    bar.textContent = percentage > 0 ? Math.round(percentage) + '%' : '';
    text.textContent = message;
}

function displayGeneratedImages(images) {
    const gallery = document.getElementById('imageGallery');
    gallery.innerHTML = '';
    
    images.forEach(img => {
        const imageDiv = document.createElement('div');
        imageDiv.style.textAlign = 'center';
        imageDiv.innerHTML = `
            <img src="${img.url}" alt="${img.title}" style="width: 100%; border-radius: 6px; margin-bottom: 0.5rem;">
            <div style="font-size: 12px; color: #6c757d;">${img.title}</div>
        `;
        gallery.appendChild(imageDiv);
    });
}

async function testImageGenerator() {
    showStatus('imageStatus', '🔗 Testing image generator...', 'info');
    
    try {
        const r = await fetch(base + "/admin/test-image-generator", {
            method: "POST",
            headers: getHeaders()
        });
        
        if (!r.ok) {
            const errorText = await r.text();
            throw new Error(`Server error: ${errorText}`);
        }
        
        const result = await r.json();
        if (result.ok) {
            showStatus('imageStatus', `✅ Image generator ready! ${result.message}`, 'success');
        } else {
            showStatus('imageStatus', `❌ Image generator not available: ${result.detail}`, 'error');
        }
    } catch (error) {
        showStatus('imageStatus', `❌ Error: ${error.message}`, 'error');
    }
}

async function generateContent() {
    const title = document.getElementById('contentTitle').value;
    const body = document.getElementById('contentBody').value;
    
    if (!title) {
        showStatus('contentStatus', 'Please enter a title', 'error');
        return;
    }

    try {
        const r = await fetch(base + "/admin/generate", {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify({title: title, body_md: body})
        });
        
        if (!r.ok) {
            const errorText = await r.text();
            throw new Error(`Server error: ${errorText}`);
        }
        
        const result = await r.json();
        if (result.ok && result.slug) {
            showStatus('contentStatus', `✅ Content generated successfully! Slug: ${result.slug}`, 'success');
            document.getElementById('contentTitle').value = '';
            document.getElementById('contentBody').value = '';
        } else {
            showStatus('contentStatus', `❌ Error: ${result.detail || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        showStatus('contentStatus', `❌ Error: ${error.message}`, 'error');
    }
}

async function generateWeeklyReport() {
    try {
        const r = await fetch(base + "/admin/weekly", {
            method: "POST",
            headers: getHeaders()
        });
        const result = await r.json();
        showStatus('contentStatus', `Weekly report generated: ${result.message || 'Success'}`, 'success');
    } catch (error) {
        showStatus('contentStatus', `Error: ${error.message}`, 'error');
    }
}

async function runScheduler() {
    try {
        const r = await fetch(base + "/admin/scheduler", {
            method: "POST",
            headers: getHeaders()
        });
        const result = await r.json();
        showStatus('contentStatus', `Scheduler run: ${result.message || 'Success'}`, 'success');
    } catch (error) {
        showStatus('contentStatus', `Error: ${error.message}`, 'error');
    }
}

async function pingSitemaps() {
    try {
        const r = await fetch(base + "/admin/ping", {
            method: "POST",
            headers: getHeaders()
        });
        const result = await r.json();
        showStatus('contentStatus', `Sitemap ping: ${result.message || 'Success'}`, 'success');
    } catch (error) {
        showStatus('contentStatus', `Error: ${error.message}`, 'error');
    }
}

async function updateIndex() {
    try {
        const r = await fetch(base + "/admin/update-index", {
            method: "POST",
            headers: getHeaders()
        });
        const result = await r.json();
        showStatus('contentStatus', `Website index updated: ${result.message || 'Success'}`, 'success');
    } catch (error) {
        showStatus('contentStatus', `Error: ${error.message}`, 'error');
    }
}

async function generateAIArticle() {
    const product = document.getElementById('articleProduct').value;
    const topic = document.getElementById('articleTopic') ? document.getElementById('articleTopic').value : '';
    const articleType = document.getElementById('articleType').value;
    const productCategory = document.getElementById('productCategory') ? document.getElementById('productCategory').value : '';
    const contentAngle = document.getElementById('contentAngle') ? document.getElementById('contentAngle').value : '';
    const tone = document.getElementById('articleTone').value;
    const keywords = document.getElementById('articleKeywords').value;
    const length = document.getElementById('articleLength').value;
    const comparison = document.getElementById('includeComparison').value;
    const audience = document.getElementById('targetAudience').value;
    const seoStrategy = document.getElementById('seoStrategy') ? document.getElementById('seoStrategy').value : '';
    const seasonalTiming = document.getElementById('seasonalTiming') ? document.getElementById('seasonalTiming').value : '';
    const includeSpecs = document.getElementById('includeProductSpecs') ? document.getElementById('includeProductSpecs').value : '';
    const includeProsCons = document.getElementById('includeProsCons') ? document.getElementById('includeProsCons').value : '';
    
    if (!product && !topic && !keywords) {
        showStatus('aiArticleStatus', '❌ Please select a product, enter a topic, or provide keywords', 'error');
        return;
    }

    showStatus('aiArticleStatus', '🤖 Generating AI article with advanced settings...', 'info');

    try {
        const r = await fetch(base + "/admin/generate-ai-article", {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify({
                product: product,
                topic: topic,
                articleType: articleType,
                productCategory: productCategory,
                contentAngle: contentAngle,
                tone: tone,
                keywords: keywords,
                length: length,
                includeComparison: comparison,
                targetAudience: audience,
                seoStrategy: seoStrategy,
                seasonalTiming: seasonalTiming,
                includeProductSpecs: includeSpecs,
                includeProsCons: includeProsCons
            })
        });
        
        if (!r.ok) {
            const errorText = await r.text();
            throw new Error(`Server error: ${errorText}`);
        }
        
        const result = await r.json();
        if (result.ok && result.slug) {
            showStatus('aiArticleStatus', `✅ AI article generated successfully! Slug: ${result.slug}`, 'success');
            // Clear form
            document.getElementById('articleKeywords').value = '';
            if (document.getElementById('articleTopic')) {
                document.getElementById('articleTopic').value = '';
            }
        } else {
            showStatus('aiArticleStatus', `❌ Error: ${result.detail || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        showStatus('aiArticleStatus', `❌ Error: ${error.message}`, 'error');
    }
}

async function testGeminiConnection() {
    showStatus('aiArticleStatus', '🔗 Testing Gemini API connection...', 'info');
    
    try {
        const r = await fetch(base + "/admin/test-gemini", {
            method: "POST",
            headers: getHeaders()
        });
        
        if (!r.ok) {
            const errorText = await r.text();
            throw new Error(`Server error: ${errorText}`);
        }
        
        const result = await r.json();
        if (result.ok) {
            showStatus('aiArticleStatus', `✅ Gemini API connection successful! ${result.message}`, 'success');
        } else {
            showStatus('aiArticleStatus', `❌ Gemini API connection failed: ${result.detail}`, 'error');
        }
    } catch (error) {
        showStatus('aiArticleStatus', `❌ Error: ${error.message}`, 'error');
    }
}

async function searchLibrary() {
    const query = document.getElementById('librarySearch').value;
    const product = document.getElementById('libraryProduct').value;
    const style = document.getElementById('libraryStyle').value;
    
    showStatus('libraryStatus', '🔍 Searching library...', 'info');
    
    try {
        const params = new URLSearchParams();
        if (query) params.append('query', query);
        if (product) params.append('product', product);
        if (style) params.append('style', style);
        params.append('limit', '50');
        
        const r = await fetch(base + `/admin/library?${params}`, {
            headers: getHeaders()
        });
        
        if (!r.ok) {
            const errorText = await r.text();
            throw new Error(`Server error: ${errorText}`);
        }
        
        const result = await r.json();
        if (result.ok) {
            displayLibraryResults(result.images);
            showStatus('libraryStatus', `✅ Found ${result.images.length} generations`, 'success');
        } else {
            showStatus('libraryStatus', `❌ Error: ${result.detail}`, 'error');
        }
    } catch (error) {
        showStatus('libraryStatus', `❌ Error: ${error.message}`, 'error');
    }
}

async function loadLibraryStats() {
    try {
        const r = await fetch(base + "/admin/library/stats", {
            headers: getHeaders()
        });
        
        if (!r.ok) {
            throw new Error(`HTTP ${r.status}`);
        }
        
        const result = await r.json();
        if (result.ok) {
            const stats = result.stats;
            document.getElementById('statTotalImages').textContent = stats.total_images;
            document.getElementById('statGenerations').textContent = stats.total_generations;
            document.getElementById('statLibrarySize').textContent = stats.library_size_mb;
            document.getElementById('statProducts').textContent = Object.keys(stats.products).length;
            
            // Update library product filter
            const libraryProductDropdown = document.getElementById('libraryProduct');
            libraryProductDropdown.innerHTML = '<option value="">All Products</option>';
            
            Object.keys(stats.products).forEach(product => {
                const option = document.createElement('option');
                option.value = product;
                option.textContent = `${product} (${stats.products[product]} images)`;
                libraryProductDropdown.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading library stats:', error);
    }
}

function displayLibraryResults(generations) {
    const grid = document.getElementById('libraryGrid');
    grid.innerHTML = '';
    
    if (generations.length === 0) {
        grid.innerHTML = '<div style="text-align: center; color: #6c757d; grid-column: 1/-1; padding: 2rem;">No images found. Try a different search or generate some images first!</div>';
        return;
    }
    
    generations.forEach(gen => {
        const genDiv = document.createElement('div');
        genDiv.style.cssText = 'border: 1px solid #e9ecef; border-radius: 8px; padding: 1rem; background: white;';
        
        // Generation header
        const header = document.createElement('div');
        header.style.cssText = 'margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #f0f0f0;';
        header.innerHTML = `
            <div style="font-weight: bold; color: #495057;">${gen.product}</div>
            <div style="font-size: 12px; color: #6c757d;">${gen.style} • ${new Date(gen.created_at).toLocaleDateString()}</div>
            <div style="font-size: 11px; color: #6c757d;">ID: ${gen.id}</div>
        `;
        genDiv.appendChild(header);
        
        // Images grid
        const imagesGrid = document.createElement('div');
        imagesGrid.style.cssText = 'display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 0.5rem;';
        
        gen.images.forEach(img => {
            const imgDiv = document.createElement('div');
            imgDiv.style.cssText = 'text-align: center;';
            imgDiv.innerHTML = `
                <img src="${img.url}" alt="${img.title}" 
                     style="width: 100%; height: 80px; object-fit: cover; border-radius: 4px; cursor: pointer;"
                     onclick="openImageModal('${img.url}', '${img.title}', '${img.prompt}')">
                <div style="font-size: 10px; color: #6c757d; margin-top: 0.2rem;">${img.title}</div>
            `;
            imagesGrid.appendChild(imgDiv);
        });
        
        genDiv.appendChild(imagesGrid);
        
        // Tags and actions
        const footer = document.createElement('div');
        footer.style.cssText = 'margin-top: 1rem; padding-top: 0.5rem; border-top: 1px solid #f0f0f0;';
        footer.innerHTML = `
            <div style="font-size: 11px; color: #6c757d; margin-bottom: 0.5rem;">
                Tags: ${gen.tags.join(', ')}
            </div>
            <button onclick="deleteGeneration('${gen.id}')" 
                    style="background: #dc3545; color: white; border: none; padding: 0.3rem 0.6rem; border-radius: 3px; font-size: 11px; cursor: pointer;">
                🗑️ Delete
            </button>
        `;
        genDiv.appendChild(footer);
        
        grid.appendChild(genDiv);
    });
}

function openImageModal(url, title, prompt) {
    // Create modal overlay
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
        background: rgba(0,0,0,0.8); z-index: 1000; display: flex; 
        align-items: center; justify-content: center; cursor: pointer;
    `;
    
    modal.innerHTML = `
        <div style="max-width: 90vw; max-height: 90vh; background: white; border-radius: 8px; padding: 1rem;" onclick="event.stopPropagation()">
            <img src="${url}" alt="${title}" style="max-width: 100%; max-height: 70vh; display: block; margin: 0 auto;">
            <div style="text-align: center; margin-top: 1rem;">
                <h3 style="margin: 0.5rem 0;">${title}</h3>
                <p style="font-size: 14px; color: #6c757d; margin: 0.5rem 0;">${prompt}</p>
                <button onclick="copyImageUrl('${url}')" style="background: #007bff; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; margin: 0.5rem;">
                    📋 Copy URL
                </button>
                <button onclick="downloadImage('${url}', '${title}')" style="background: #28a745; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; margin: 0.5rem;">
                    💾 Download
                </button>
            </div>
        </div>
    `;
    
    // Close on click outside
    modal.onclick = () => document.body.removeChild(modal);
    
    document.body.appendChild(modal);
}

function copyImageUrl(url) {
    const fullUrl = window.location.origin + url;
    navigator.clipboard.writeText(fullUrl).then(() => {
        alert('Image URL copied to clipboard!');
    });
}

function downloadImage(url, title) {
    const link = document.createElement('a');
    link.href = url;
    link.download = title.replace(/[^a-zA-Z0-9]/g, '_') + '.png';
    link.click();
}

async function deleteGeneration(generationId) {
    if (!confirm('Are you sure you want to delete this generation and all its images?')) {
        return;
    }
    
    try {
        const r = await fetch(base + `/admin/library/${generationId}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        
        const result = await r.json();
        if (result.ok) {
            showStatus('libraryStatus', `✅ Deleted generation ${generationId}`, 'success');
            searchLibrary(); // Refresh results
            loadLibraryStats(); // Refresh stats
        } else {
            showStatus('libraryStatus', `❌ Error: ${result.detail}`, 'error');
        }
    } catch (error) {
        showStatus('libraryStatus', `❌ Error: ${error.message}`, 'error');
    }
}

async function organizeExistingImages() {
    showStatus('libraryStatus', '📁 Organizing existing images...', 'info');
    
    try {
        const r = await fetch(base + "/admin/library/organize", {
            method: 'POST',
            headers: getHeaders()
        });
        
        const result = await r.json();
        if (result.ok) {
            showStatus('libraryStatus', `✅ ${result.result.message}`, 'success');
            loadLibraryStats();
            searchLibrary();
        } else {
            showStatus('libraryStatus', `❌ Error: ${result.detail}`, 'error');
        }
    } catch (error) {
        showStatus('libraryStatus', `❌ Error: ${error.message}`, 'error');
    }
}

function generateContentIdea() {
    const productCategory = document.getElementById('productCategory') ? document.getElementById('productCategory').value : 'dog-toys';
    const contentAngle = document.getElementById('contentAngle') ? document.getElementById('contentAngle').value : 'sustainability-focused';
    const targetAudience = document.getElementById('targetAudience') ? document.getElementById('targetAudience').value : 'eco-conscious-consumers';
    const seasonalTiming = document.getElementById('seasonalTiming') ? document.getElementById('seasonalTiming').value : 'general';
    const articleType = document.getElementById('articleType') ? document.getElementById('articleType').value : 'Product Review';
    
    const contentIdeas = [
        // Product Review Ideas
        `${articleType}: Best ${productCategory.replace(/-/g, ' ')} for ${targetAudience.replace(/-/g, ' ')} in 2025`,
        `${articleType}: Top 5 ${contentAngle.replace(/-/g, ' ')} ${productCategory.replace(/-/g, ' ')} tested by real pet owners`,
        `${articleType}: Why ${targetAudience.replace(/-/g, ' ')} love these ${productCategory.replace(/-/g, ' ')} (honest review)`,
        
        // Seasonal Ideas
        `${seasonalTiming === 'general' ? 'Year-round' : seasonalTiming} guide to choosing ${productCategory.replace(/-/g, ' ')}`,
        `${seasonalTiming === 'general' ? '' : seasonalTiming + ' '}essentials: ${productCategory.replace(/-/g, ' ')} that ${targetAudience.replace(/-/g, ' ')} actually need`,
        
        // Problem-solving Ideas
        `How to choose ${contentAngle.replace(/-/g, ' ')} ${productCategory.replace(/-/g, ' ')} that won't break the bank`,
        `Common mistakes ${targetAudience.replace(/-/g, ' ')} make when buying ${productCategory.replace(/-/g, ' ')}`,
        `The ultimate ${productCategory.replace(/-/g, ' ')} buying guide for ${targetAudience.replace(/-/g, ' ')}`,
        
        // Comparison Ideas
        `${productCategory.replace(/-/g, ' ')} showdown: Premium vs budget options for ${targetAudience.replace(/-/g, ' ')}`,
        `Which ${productCategory.replace(/-/g, ' ')} is best for your lifestyle? Complete comparison`,
        
        // Trend Ideas
        `Latest trends in ${contentAngle.replace(/-/g, ' ')} ${productCategory.replace(/-/g, ' ')} for 2025`,
        `What ${targetAudience.replace(/-/g, ' ')} are buying: ${productCategory.replace(/-/g, ' ')} edition`
    ];
    
    // Shuffle and pick 5 random ideas
    const shuffled = contentIdeas.sort(() => 0.5 - Math.random());
    const selectedIdeas = shuffled.slice(0, 5);
    
    // Display ideas
    const ideasDiv = document.getElementById('contentIdeas');
    const ideasList = document.getElementById('contentIdeasList');
    
    if (ideasDiv && ideasList) {
        ideasList.innerHTML = selectedIdeas.map((idea, index) => 
            `<div style="margin: 8px 0; padding: 8px; background: white; border-radius: 4px; cursor: pointer; border: 1px solid #e0e0e0;" 
                  onclick="useContentIdea('${idea.replace(/'/g, "\\'")}')">
                <strong>${index + 1}.</strong> ${idea}
                <small style="color: #666; display: block; margin-top: 4px;">💡 Click to use this idea</small>
             </div>`
        ).join('');
        
        ideasDiv.style.display = 'block';
    }
}

function useContentIdea(idea) {
    const topicField = document.getElementById('articleTopic');
    if (topicField) {
        topicField.value = idea;
        document.getElementById('contentIdeas').style.display = 'none';
        showStatus('aiArticleStatus', '💡 Content idea applied! You can modify it or generate the article.', 'success');
    }
}

// Load initial data
window.onload = function() {
    loadStats();
    loadRoutes();
    checkHealth();
    loadProductDropdown();
    loadLibraryStats();
    searchLibrary(); // Load recent images
}; 