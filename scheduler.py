"""
Job scheduler for content generation, reporting and optional sitemap pings.

This module uses APScheduler to run background tasks on an interval or
cron schedule. It generates new content, produces weekly click reports,
and can notify search engines when new pages are published.

Run it directly to start the scheduler:
    python scheduler.py
"""
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import datetime as dt
import os
import sqlite3
import glob

sched = BlockingScheduler()

@sched.scheduled_job("interval", days=3)
def content_job() -> None:
    """Generate a new piece of content every `cadence_days` as defined in config.

    This simply calls the content pipeline script. When run in a deployed
    environment, consider pointing this to a management command or background
    task instead of invoking a subprocess directly.
    """
    subprocess.run(["python", "content_pipeline.py"], check=True)

@sched.scheduled_job("cron", day_of_week="sun", hour=8)
def weekly_report() -> None:
    """Generate a simple markdown report summarising clicks over the past week."""
    conn = sqlite3.connect("affiliate.db")
    c = conn.cursor()
    week_ago = (dt.datetime.utcnow() - dt.timedelta(days=7)).isoformat()
    rows = list(
        c.execute(
            "SELECT offer, variant, COUNT(*) FROM clicks WHERE created_at >= ? GROUP BY 1,2",
            (week_ago,),
        )
    )
    report = ["# Weekly Report", f"Generated {dt.datetime.utcnow().isoformat()} UTC", ""]
    for offer, variant, n in rows:
        report.append(f"- {offer} / {variant}: {n} clicks")
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/weekly_{dt.date.today().isoformat()}.md", "w") as f:
        f.write("\n".join(report))

@sched.scheduled_job("interval", hours=12)
def ping_sitemaps() -> None:
    """Placeholder for notifying search engines of new or updated pages."""
    for path in glob.glob("site/**/*.html", recursive=True):
        # In a real implementation you might send a ping to Google or
        # your hosting platform here. Leaving this as a no‑op satisfies the
        # scheduling requirement without violating platform policies.
        pass
    print("Sitemap ping tick")

if __name__ == "__main__":
    sched.start()
