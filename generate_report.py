#!/usr/bin/env python3
"""
Generate a weekly report of click statistics
"""

import sqlite3
import datetime as dt
import os

def generate_weekly_report():
    """Generate a weekly report of click statistics"""
    
    # Connect to database
    conn = sqlite3.connect("affiliate.db")
    cursor = conn.cursor()
    
    # Get date range (last 7 days)
    week_ago = (dt.datetime.utcnow() - dt.timedelta(days=7)).isoformat()
    
    # Get click statistics
    cursor.execute("""
        SELECT offer, variant, COUNT(*) as clicks
        FROM clicks 
        WHERE created_at >= ? 
        GROUP BY offer, variant 
        ORDER BY clicks DESC
    """, (week_ago,))
    
    rows = cursor.fetchall()
    
    # Generate report
    report_lines = [
        "# Weekly Affiliate Report",
        f"Generated: {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        f"Period: Last 7 days (since {week_ago[:10]})",
        "",
        "## Click Statistics",
        ""
    ]
    
    total_clicks = 0
    for offer, variant, clicks in rows:
        report_lines.append(f"- **{offer}** (Variant {variant}): {clicks} clicks")
        total_clicks += clicks
    
    report_lines.extend([
        "",
        f"**Total Clicks: {total_clicks}**",
        "",
        "## Performance Summary",
        ""
    ])
    
    if total_clicks > 0:
        report_lines.extend([
            "### Top Performing Offers:",
            ""
        ])
        
        for i, (offer, variant, clicks) in enumerate(rows[:3], 1):
            percentage = (clicks / total_clicks) * 100
            report_lines.append(f"{i}. {offer} (Variant {variant}): {clicks} clicks ({percentage:.1f}%)")
    else:
        report_lines.append("No clicks recorded in the last 7 days.")
    
    report_lines.extend([
        "",
        "## Recommendations",
        "",
        "- Focus on top-performing offers",
        "- Consider A/B testing different variants",
        "- Create more content around popular products",
        "- Monitor conversion rates from clicks to sales"
    ])
    
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    # Write report
    report_filename = f"reports/weekly_{dt.date.today().isoformat()}.md"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    conn.close()
    
    return report_filename

if __name__ == "__main__":
    filename = generate_weekly_report()
    print(f"✅ Weekly report generated: {filename}")
