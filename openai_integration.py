#!/usr/bin/env python3
"""
OpenAI API integration for AI article generation
"""

import os
import re
from typing import Dict, Any
import openai

class OpenAIArticleGenerator:
    def __init__(self, api_key: str = None):
        """Initialize OpenAI API client"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Configure the API
        openai.api_key = self.api_key
        
        # Use GPT-4 for high-quality content generation
        self.model = "gpt-4o-mini"  # Cost-effective and fast
    
    def test_connection(self) -> bool:
        """Test if OpenAI API is accessible"""
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Hello, please respond with 'API connection successful'"}
                ],
                max_tokens=10,
                temperature=0.1
            )
            return "successful" in response.choices[0].message.content.lower()
        except Exception as e:
            print(f"OpenAI API connection test failed: {e}")
            return False
    
    def generate_article(self, 
                        product_info: Dict[str, Any],
                        article_type: str,
                        tone: str,
                        keywords: str,
                        length: str,
                        include_comparison: str,
                        target_audience: str,
                        seo_focus: str) -> str:
        """
        Generate an article using OpenAI API
        """
        
        # Build the prompt based on article type and parameters
        prompt = self._build_prompt(
            product_info, article_type, tone, keywords, length, 
            include_comparison, target_audience, seo_focus
        )
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert content writer specializing in eco-friendly pet products. You write engaging, SEO-optimized articles that help pet owners make informed purchasing decisions. Always include proper affiliate disclosures and focus on sustainability and environmental benefits."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self._get_max_tokens(length),
                temperature=self._get_temperature(tone),
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            # Post-process the content
            content = self._post_process_content(content, product_info)
            
            return content
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _build_prompt(self, 
                     product_info: Dict[str, Any],
                     article_type: str,
                     tone: str,
                     keywords: str,
                     length: str,
                     include_comparison: str,
                     target_audience: str,
                     seo_focus: str) -> str:
        """Build the prompt for article generation"""
        
        product_name = product_info.get("offer", "eco-friendly pet product")
        
        # Article type specific instructions
        article_instructions = {
            "review": f"Write a comprehensive product review of {product_name}. Include detailed analysis of features, benefits, pros and cons, and real-world usage scenarios.",
            "comparison": f"Write a comparison guide featuring {product_name} alongside similar products. Include a comparison table and detailed analysis of each option.",
            "guide": f"Write a comprehensive buying guide about {product_name}. Include tips for choosing the right product, what to look for, and how to use it effectively.",
            "listicle": f"Write a listicle featuring {product_name} and other top products in the same category. Include rankings, brief descriptions, and why each product made the list.",
            "how-to": f"Write a how-to guide about using {product_name}. Include step-by-step instructions, tips, and best practices."
        }
        
        base_instruction = article_instructions.get(article_type, f"Write an informative article about {product_name}")
        
        # Length specifications
        length_specs = {
            "short": "Keep the article concise, around 500-800 words.",
            "medium": "Write a comprehensive article, around 800-1200 words.",
            "long": "Write an in-depth article, around 1200-1800 words."
        }
        
        # Tone specifications
        tone_specs = {
            "professional": "Use a professional, authoritative tone with industry expertise.",
            "friendly": "Use a warm, friendly tone that feels like advice from a knowledgeable friend.",
            "casual": "Use a casual, conversational tone that's easy to read and relatable.",
            "expert": "Use an expert, technical tone with detailed analysis and insights."
        }
        
        # SEO focus
        seo_instructions = {
            "general": "Optimize for general eco-friendly pet product searches.",
            "specific": f"Optimize for specific searches related to {product_name}.",
            "long-tail": "Focus on long-tail keywords and specific use cases.",
            "local": "Include location-based optimization where relevant."
        }
        
        # Build the complete prompt
        prompt_parts = [
            f"# Article Generation Request",
            f"",
            f"**Product:** {product_name}",
            f"**Article Type:** {article_type.title()}",
            f"**Target Audience:** {target_audience.replace('-', ' ').title()}",
            f"",
            f"## Instructions:",
            f"",
            f"1. {base_instruction}",
            f"2. {length_specs.get(length, 'Write a well-structured article of appropriate length.')}",
            f"3. {tone_specs.get(tone, 'Use an appropriate tone for the content.')}",
            f"4. {seo_instructions.get(seo_focus, 'Optimize for relevant search terms.')}",
            f"",
        ]
        
        if keywords:
            prompt_parts.extend([
                f"5. **Important Keywords to Include:** {keywords}",
                f"",
            ])
        
        if include_comparison == "yes":
            prompt_parts.extend([
                f"6. **Include Product Comparison:** Add a comparison section with similar products, including pros/cons and recommendations.",
                f"",
            ])
        
        prompt_parts.extend([
            f"## Content Requirements:",
            f"",
            f"- Start with a compelling headline using markdown (e.g., # Best Eco-Friendly Dog Toys 2025)",
            f"- Include an engaging introduction that hooks the reader",
            f"- Structure content with clear headings and subheadings",
            f"- Focus on sustainability, environmental benefits, and eco-friendly aspects",
            f"- Include practical tips and actionable advice",
            f"- Add a conclusion that summarizes key points",
            f"- Include affiliate disclosure: 'As an Amazon Associate I earn from qualifying purchases.'",
            f"- Use proper markdown formatting throughout",
            f"- Include relevant emojis to make content engaging",
            f"- End with a strong call-to-action",
            f"",
            f"## Important Notes:",
            f"- This is for affiliate marketing, so include natural product mentions",
            f"- Focus on helping pet owners make informed decisions",
            f"- Emphasize environmental benefits and sustainability",
            f"- Make content scannable with bullet points and short paragraphs",
            f"- Include specific product details and real-world usage scenarios",
            f"",
            f"Please generate the article now:"
        ])
        
        return "\n".join(prompt_parts)
    
    def _get_max_tokens(self, length: str) -> int:
        """Get max tokens based on desired length"""
        length_tokens = {
            "short": 800,
            "medium": 1500,
            "long": 2500
        }
        return length_tokens.get(length, 1500)
    
    def _get_temperature(self, tone: str) -> float:
        """Get temperature based on desired tone"""
        tone_temps = {
            "professional": 0.3,
            "friendly": 0.7,
            "casual": 0.8,
            "expert": 0.4
        }
        return tone_temps.get(tone, 0.7)
    
    def _post_process_content(self, content: str, product_info: Dict[str, Any]) -> str:
        """Post-process the generated content"""
        
        # Ensure proper markdown formatting
        if not content.startswith('#'):
            content = f"# {product_info.get('offer', 'Eco-Friendly Pet Product Review')}\n\n{content}"
        
        # Add affiliate disclosure if not present
        if "Amazon Associate" not in content:
            disclosure = "\n\n> As an Amazon Associate I earn from qualifying purchases.\n"
            content = content.replace('\n\n', disclosure, 1)
        
        # Add call-to-action if not present
        if "call-to-action" not in content.lower() and "shop" not in content.lower():
            cta = "\n\n## 🛒 Ready to Shop?\n\nIf you're ready to purchase eco-friendly pet products, check out our recommended options above. Each product has been carefully selected for its sustainability and quality.\n"
            content += cta
        
        return content

# For backward compatibility, create an alias
GeminiArticleGenerator = OpenAIArticleGenerator
