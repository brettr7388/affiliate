# 🐕 Eco Pet Guide - Affiliate Marketing System

An automated affiliate marketing system for eco-friendly pet products with a beautiful admin console to manage everything from your browser.

## 🚀 Quick Start

### 1. Start the Admin Console
```bash
python start_admin.py
```

This will:
- Create a `.env` file with a secure admin token
- Install dependencies if needed
- Start the server at `http://127.0.0.1:8088`

**⚠️ Important**: Before deploying, update `config.yaml` and replace `YOUR-AMAZON-ASSOCIATES-TAG` with your actual Amazon Associates tag.

### 2. Access the Admin Console
Open your browser and go to: `http://127.0.0.1:8088/admin`

Enter the admin token that was displayed when you started the server.

## 🎯 What This System Does

### Core Features
- **Affiliate Link Tracking**: Create short, trackable URLs that redirect to Amazon
- **Click Analytics**: Track every click with detailed data (IP, user agent, UTM parameters)
- **A/B Testing**: Test different offers and track performance
- **Content Generation**: Automatically create blog posts with affiliate links
- **Admin Console**: Manage everything from a beautiful web interface

### Revenue Streams
- **Amazon Associates**: Earn commissions on pet product sales
- **Other Affiliate Programs**: Add Chewy, Petco, PetSmart, etc.
- **Sponsored Content**: Brands pay for product reviews
- **Email Marketing**: Build an audience for future promotions

## 📊 Admin Console Features

### Dashboard
- **Real-time Stats**: Total clicks, today's clicks, active routes, weekly performance
- **Quick Actions**: Generate content, run reports, ping search engines

### Route Management
- **Create/Edit Routes**: Set up affiliate links with custom slugs
- **A/B Testing**: Test different offers and track performance
- **Bulk Operations**: Manage multiple routes at once

### Content Generation
- **Article Creator**: Write and publish blog posts with affiliate links
- **Auto-disclosure**: FTC-compliant disclosures added automatically
- **SEO Optimization**: Proper meta tags and structure

### Analytics
- **Click Tracking**: See which links perform best
- **Traffic Sources**: Track UTM parameters and referrers
- **Conversion Data**: Monitor click-through rates

## 🔗 How to Make Money

### 1. Set Up Your Affiliate Links
1. Go to the admin console
2. Create a new route with your Amazon product URL
3. Use a memorable slug like `eco-toys-2025`
4. Your tracking URL becomes: `http://yoursite.com/r/eco-toys-2025`

### 2. Generate Traffic
- **Social Media**: Share your articles on Pinterest, Instagram, TikTok
- **SEO**: Optimize content for search engines
- **Paid Ads**: Run Facebook/Google ads to your articles
- **Reddit/Facebook Groups**: Answer questions and share helpful content

### 3. Track Performance
- Monitor clicks in the admin console
- A/B test different offers
- Optimize based on data

## 📈 Traffic Generation Strategies

### Free Methods
1. **Pinterest**: Create boards for eco-friendly pet products
2. **Instagram**: Post product photos and tips
3. **TikTok**: Create short videos about sustainable pet care
4. **Reddit**: Answer questions in pet-related subreddits
5. **Facebook Groups**: Join pet owner communities
6. **Quora**: Answer questions about pet products

### Paid Methods
1. **Facebook Ads**: Target pet owners and eco-conscious people
2. **Google Ads**: Bid on keywords like "eco-friendly dog toys"
3. **Pinterest Ads**: Great for visual products

## 🛠 Technical Setup

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python start_admin.py

# Or manually
uvicorn app:app --reload --port 8088
```

### Production Deployment
1. **Netlify** (for static site): Deploy the `site/` folder
2. **Render** (for API): Deploy the FastAPI app
3. **Database**: Use PostgreSQL for production

### Environment Variables
```bash
ENV=prod
DATABASE_URL=postgresql://...
ADMIN_TOKEN=your-secure-token
AFFILIATE_DISCLOSURE="As an Amazon Associate I earn from qualifying purchases."
```

## 📝 Content Strategy

### Article Types
- **Product Reviews**: "Best Eco-Friendly Dog Toys 2025"
- **Comparison Guides**: "West Paw vs Kong: Which is Greener?"
- **How-to Guides**: "How to Choose Non-Toxic Dog Toys"
- **Roundups**: "9 Sustainable Dog Essentials"

### SEO Optimization
- Use long-tail keywords
- Include product images
- Add internal links
- Optimize meta descriptions

## 💰 Monetization Tips

### Amazon Associates
- Focus on high-commission categories
- Use seasonal content (holidays, back-to-school)
- Create gift guides
- Review trending products

### Other Affiliate Programs
- **Chewy**: 4% commission on pet products
- **Petco**: 3-8% commission
- **PetSmart**: 3-8% commission
- **Etsy**: 4% commission on handmade items

### Sponsored Content
- Reach out to eco-friendly pet brands
- Offer product reviews
- Create sponsored posts
- Build an email list

## 🔍 Analytics & Optimization

### Key Metrics to Track
- **Click-through rate**: How many people click your links
- **Conversion rate**: How many clicks result in sales
- **Revenue per click**: Average earnings per visitor
- **Traffic sources**: Which platforms drive the most sales

### A/B Testing
- Test different headlines
- Try different product images
- Experiment with call-to-action text
- Test different affiliate programs

## 🚨 Legal Compliance

### FTC Requirements
- Always disclose affiliate relationships
- Use clear, conspicuous disclosures
- Don't make false claims about products
- Keep records of all affiliate activities

### Amazon Associates Policy
- Don't use Amazon trademarks in URLs
- Don't incentivize clicks
- Don't use misleading content
- Follow all program terms

## 📞 Support

If you need help:
1. Check the admin console for system status
2. Review the API documentation at `/docs`
3. Check the logs for error messages
4. Ensure your `.env` file is properly configured

## 🎉 Success Tips

1. **Start Small**: Focus on one product category first
2. **Be Consistent**: Post regularly and build an audience
3. **Test Everything**: A/B test offers, headlines, and content
4. **Track Performance**: Use the analytics to optimize
5. **Scale Gradually**: Add more products and traffic sources as you grow

---

**Remember**: This system is designed to run automatically once set up. Focus on creating great content and driving traffic - the system will handle the rest! 