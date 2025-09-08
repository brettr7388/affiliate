#!/usr/bin/env python3
"""
Image Library Management System
Organizes, stores, and provides access to all generated images
"""

import os
import json
import shutil
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class ImageLibrary:
    def __init__(self, library_path: str = "site/images/library"):
        """Initialize the image library"""
        self.library_path = Path(library_path)
        self.metadata_file = self.library_path / "metadata.json"
        self.slideshows_path = Path("site/images/slideshows")
        
        # Create directories
        self.library_path.mkdir(parents=True, exist_ok=True)
        self.slideshows_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize metadata file
        if not self.metadata_file.exists():
            self._save_metadata({})
    
    def _load_metadata(self) -> Dict:
        """Load image metadata from JSON file"""
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_metadata(self, metadata: Dict):
        """Save image metadata to JSON file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
    
    def add_images(self, images: List[Dict], product: str, style: str, generation_id: str = None) -> Dict:
        """Add images to the library with metadata"""
        if not generation_id:
            generation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        metadata = self._load_metadata()
        
        # Create entry for this generation
        entry = {
            "id": generation_id,
            "product": product,
            "style": style,
            "created_at": datetime.now().isoformat(),
            "images": [],
            "tags": self._generate_tags(product, style),
            "total_images": len(images)
        }
        
        # Process each image
        for i, img in enumerate(images):
            # Copy image to library with organized naming
            original_path = Path(img["path"])
            library_filename = f"{generation_id}_{i+1}_{img['title'].lower().replace(' ', '_')}.png"
            library_path = self.library_path / library_filename
            
            # Copy file
            if original_path.exists():
                shutil.copy2(original_path, library_path)
                
                # Add to entry
                entry["images"].append({
                    "filename": library_filename,
                    "title": img["title"],
                    "prompt": img.get("prompt", ""),
                    "url": f"/images/library/{library_filename}",
                    "size": library_path.stat().st_size if library_path.exists() else 0,
                    "index": i + 1
                })
        
        # Add to metadata
        metadata[generation_id] = entry
        self._save_metadata(metadata)
        
        return entry
    
    def _generate_tags(self, product: str, style: str) -> List[str]:
        """Generate searchable tags for images"""
        tags = [product.lower(), style.lower()]
        
        # Add product-specific tags
        if "dog" in product.lower():
            tags.extend(["dog", "pet", "canine"])
        if "eco" in product.lower() or "biodegradable" in product.lower():
            tags.extend(["eco-friendly", "sustainable", "green"])
        if "toy" in product.lower():
            tags.extend(["toy", "play", "entertainment"])
        if "poop" in product.lower() or "bag" in product.lower():
            tags.extend(["waste", "cleanup", "bags"])
        
        # Add style-specific tags
        if style == "professional":
            tags.extend(["professional", "clean", "commercial"])
        elif style == "vibrant":
            tags.extend(["colorful", "bright", "eye-catching"])
        elif style == "minimal":
            tags.extend(["minimal", "simple", "clean"])
        
        return list(set(tags))  # Remove duplicates
    
    def search_images(self, query: str = "", product: str = "", style: str = "", limit: int = 50) -> List[Dict]:
        """Search images by various criteria"""
        metadata = self._load_metadata()
        results = []
        
        for entry_id, entry in metadata.items():
            # Filter by product
            if product and product.lower() not in entry["product"].lower():
                continue
            
            # Filter by style
            if style and style.lower() != entry["style"].lower():
                continue
            
            # Filter by query (search in tags, product, titles)
            if query:
                search_text = f"{entry['product']} {entry['style']} {' '.join(entry['tags'])}".lower()
                for img in entry["images"]:
                    search_text += f" {img['title']} {img.get('prompt', '')}".lower()
                
                if query.lower() not in search_text:
                    continue
            
            results.append(entry)
        
        # Sort by creation date (newest first)
        results.sort(key=lambda x: x["created_at"], reverse=True)
        
        return results[:limit]
    
    def get_all_images(self, limit: int = 100) -> List[Dict]:
        """Get all images sorted by creation date"""
        return self.search_images(limit=limit)
    
    def get_image_stats(self) -> Dict:
        """Get library statistics"""
        metadata = self._load_metadata()
        
        total_generations = len(metadata)
        total_images = sum(entry["total_images"] for entry in metadata.values())
        
        # Count by product
        products = {}
        styles = {}
        
        for entry in metadata.values():
            product = entry["product"]
            style = entry["style"]
            
            products[product] = products.get(product, 0) + entry["total_images"]
            styles[style] = styles.get(style, 0) + entry["total_images"]
        
        return {
            "total_generations": total_generations,
            "total_images": total_images,
            "products": products,
            "styles": styles,
            "library_size_mb": self._get_library_size()
        }
    
    def _get_library_size(self) -> float:
        """Calculate total library size in MB"""
        total_size = 0
        if self.library_path.exists():
            for file_path in self.library_path.glob("*.png"):
                total_size += file_path.stat().st_size
        return round(total_size / (1024 * 1024), 2)
    
    def delete_generation(self, generation_id: str) -> bool:
        """Delete a complete generation and its images"""
        metadata = self._load_metadata()
        
        if generation_id not in metadata:
            return False
        
        entry = metadata[generation_id]
        
        # Delete image files
        for img in entry["images"]:
            img_path = self.library_path / img["filename"]
            if img_path.exists():
                img_path.unlink()
        
        # Remove from metadata
        del metadata[generation_id]
        self._save_metadata(metadata)
        
        return True
    
    def organize_existing_images(self):
        """Organize existing slideshow images into the library"""
        if not self.slideshows_path.exists():
            return {"organized": 0, "message": "No slideshow directory found"}
        
        organized_count = 0
        
        # Find existing slideshow images
        for img_path in self.slideshows_path.glob("*.png"):
            # Parse filename to extract info
            filename = img_path.name
            
            # Try to extract generation info from filename
            # Format: YYYYMMDD_HHMMSS_product_slide_N.png
            parts = filename.replace('.png', '').split('_')
            
            if len(parts) >= 4:
                date_part = parts[0]
                time_part = parts[1]
                product_part = '_'.join(parts[2:-2])  # Everything between time and slide_N
                
                generation_id = f"{date_part}_{time_part}"
                
                # Create library entry if it doesn't exist
                metadata = self._load_metadata()
                if generation_id not in metadata:
                    # Copy to library
                    library_filename = f"{generation_id}_{parts[-1]}_product_hero.png"
                    library_path = self.library_path / library_filename
                    
                    shutil.copy2(img_path, library_path)
                    
                    # Create metadata entry
                    metadata[generation_id] = {
                        "id": generation_id,
                        "product": product_part,
                        "style": "simple",  # Default style
                        "created_at": datetime.now().isoformat(),
                        "images": [{
                            "filename": library_filename,
                            "title": "Product Hero Shot",
                            "prompt": f"Product photo of {product_part}",
                            "url": f"/images/library/{library_filename}",
                            "size": library_path.stat().st_size,
                            "index": 1
                        }],
                        "tags": self._generate_tags(product_part, "simple"),
                        "total_images": 1,
                        "migrated_from": "slideshows"
                    }
                    
                    self._save_metadata(metadata)
                    organized_count += 1
        
        return {
            "organized": organized_count,
            "message": f"Organized {organized_count} existing images into library"
        }

# Global library instance
image_library = ImageLibrary()
