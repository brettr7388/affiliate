/**
 * Image Rotation System for Eco Pet Guide
 * Rotates product images based on category and page refresh
 */

class ImageRotator {
    constructor() {
        this.categories = {
            'toy': ['toy1.png', 'toy2.png', 'toy3.png', 'toy4.png'], // 4 images for toys
            'bag': ['bag1.png', 'bag2.png', 'bag3.png'],
            'bowl': ['bowl1.png', 'bowl2.png', 'bowl3.png'],
            'leash': ['leash1.png', 'leash2.png', 'leash3.png'],
            'bed': ['bed1.png', 'bed2.png', 'bed3.png'],
            'treat': ['treat1.png', 'treat2.png', 'treat3.png'],
            'all': ['all1.png', 'all2.png', 'all3.png']
        };
        
        this.init();
    }
    
    init() {
        // Rotate images on page load
        this.rotateAllImages();
        
        // Add refresh button functionality
        this.addRefreshButton();
    }
    
    getRandomImage(category) {
        const images = this.categories[category];
        if (!images || images.length === 0) return null;
        
        // Use truly random selection for each page load
        const randomIndex = Math.floor(Math.random() * images.length);
        return images[randomIndex];
    }
    
    rotateAllImages() {
        // Find all elements with data-product-category attribute
        const productElements = document.querySelectorAll('[data-product-category]');
        
        productElements.forEach(element => {
            const category = element.getAttribute('data-product-category');
            const imagePath = this.getRandomImage(category);
            
            if (imagePath) {
                const img = element.querySelector('img');
                if (img) {
                    img.src = `../images/rotating/${category}/${imagePath}`;
                    img.alt = `Eco-friendly ${category} product image`;
                }
            }
        });
        
        // Handle hero images
        const heroElements = document.querySelectorAll('[data-hero-category]');
        heroElements.forEach(element => {
            const category = element.getAttribute('data-hero-category');
            const imagePath = this.getRandomImage(category);
            
            if (imagePath) {
                const img = element.querySelector('img');
                if (img) {
                    img.src = `../images/rotating/${category}/${imagePath}`;
                    img.alt = `Eco-friendly ${category} hero image`;
                }
            }
        });
    }
    
    addRefreshButton() {
        // Add a refresh button to the page
        const refreshButton = document.createElement('button');
        refreshButton.innerHTML = '🔄 Refresh Images';
        refreshButton.className = 'refresh-images-btn';
        refreshButton.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(40,167,69,0.4);
            z-index: 1000;
            transition: all 0.3s ease;
        `;
        
        refreshButton.addEventListener('click', () => {
            this.rotateAllImages();
            refreshButton.innerHTML = '✅ Refreshed!';
            setTimeout(() => {
                refreshButton.innerHTML = '🔄 Refresh Images';
            }, 2000);
        });
        
        refreshButton.addEventListener('mouseenter', () => {
            refreshButton.style.transform = 'translateY(-2px)';
            refreshButton.style.boxShadow = '0 6px 20px rgba(40,167,69,0.6)';
        });
        
        refreshButton.addEventListener('mouseleave', () => {
            refreshButton.style.transform = 'translateY(0)';
            refreshButton.style.boxShadow = '0 4px 15px rgba(40,167,69,0.4)';
        });
        
        document.body.appendChild(refreshButton);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ImageRotator();
});
