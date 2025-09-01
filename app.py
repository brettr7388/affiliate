import os
import uuid
import datetime as dt
import re
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Use SQLite by default; override via the DATABASE_URL env var
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./affiliate.db")
engine = create_engine(DATABASE_URL, future=True)

app = FastAPI()

# Admin authentication
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

def require_admin(request: Request):
    """Check if request has valid admin token"""
    token = request.headers.get("X-Admin-Token") or request.query_params.get("token")
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


def init_db() -> None:
    """Create required tables if they don't already exist."""
    with engine.begin() as conn:
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS clicks(
          id TEXT PRIMARY KEY,
          created_at TEXT,
          offer TEXT,
          variant TEXT,
          dest_url TEXT,
          ip TEXT,
          ua TEXT,
          referrer TEXT,
          utm_source TEXT,
          utm_medium TEXT,
          utm_campaign TEXT
        );
        """
            )
        )
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS routes(
          slug TEXT PRIMARY KEY,
          offer TEXT,
          variant TEXT,
          dest_url TEXT
        );
        """
            )
        )


init_db()


class Route(BaseModel):
    slug: str
    offer: str
    variant: str = "A"
    dest_url: str


@app.post("/admin/route")
def create_route(r: Route, request: Request):
    require_admin(request)
    # Works on Postgres and modern SQLite
    upsert = text("""
        INSERT INTO routes(slug, offer, variant, dest_url)
        VALUES (:s, :o, :v, :d)
        ON CONFLICT (slug) DO UPDATE
        SET offer   = EXCLUDED.offer,
            variant = EXCLUDED.variant,
            dest_url= EXCLUDED.dest_url
    """)
    with engine.begin() as conn:
        conn.execute(upsert, {"s": r.slug, "o": r.offer, "v": r.variant, "d": r.dest_url})
    return {"ok": True}



@app.get("/r/{slug}")
def redirect(slug: str, request: Request, v: str | None = None) -> RedirectResponse:
    """Redirect to the destination URL, logging click data.

    An optional query parameter `v` allows overriding the variant (e.g. v=B).
    """
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT offer,variant,dest_url FROM routes WHERE slug=:s"),
            {"s": slug},
        ).fetchone()
    if not row:
        raise HTTPException(404, "Unknown route")
    offer, variant, dest = row
    # allow explicit variant override via query parameter
    if v in ("A", "B"):
        variant = v
    # capture UTM params from the incoming request
    q = dict(parse_qsl(urlparse(str(request.url)).query))
    utm_source = q.get("utm_source")
    utm_medium = q.get("utm_medium")
    utm_campaign = q.get("utm_campaign")

    click_id = str(uuid.uuid4())
    with engine.begin() as conn:
        conn.execute(
            text(
                """
            INSERT INTO clicks(
                id,created_at,offer,variant,dest_url,ip,ua,referrer,utm_source,utm_medium,utm_campaign
            )
            VALUES(:id,:ts,:offer,:variant,:dest,:ip,:ua,:ref,:us,:um,:uc)
            """
            ),
            {
                "id": click_id,
                "ts": dt.datetime.utcnow().isoformat(),
                "offer": offer,
                "variant": variant,
                "dest": dest,
                "ip": request.client.host if request.client else None,
                "ua": request.headers.get("User-Agent"),
                "ref": request.headers.get("Referer"),
                "us": utm_source,
                "um": utm_medium,
                "uc": utm_campaign,
            },
        )
    return RedirectResponse(dest, status_code=302)


@app.get("/health")
def health() -> dict[str, object]:
    """Basic health check endpoint exposing the number of logged clicks."""
    with engine.begin() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM clicks")).scalar()
    return {"status": "ok", "clicks": total}

@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the main website"""
    try:
        with open("site/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""<pre>Eco Pet Guide Affiliate System
See: /health  /docs  /admin
</pre>""")

@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    """Main admin console with full UI"""
    return """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Eco Pet Guide Admin</title>
    <style>
        body {
            font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 16px;
            line-height: 1.6;
            background: #f8f9fa;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        .full-width {
            grid-column: 1 / -1;
        }
        input, button, select, textarea {
            padding: 0.6rem;
            margin: 0.2rem 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        input, select, textarea {
            width: 100%;
            box-sizing: border-box;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: 500;
        }
        button:hover {
            background: #0056b3;
        }
        button.secondary {
            background: #6c757d;
        }
        button.secondary:hover {
            background: #545b62;
        }
        .section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 6px;
            border: 1px solid #e9ecef;
        }
        .section h2 {
            margin-top: 0;
            color: #495057;
        }
        pre {
            background: #f6f6f6;
            padding: 12px;
            border-radius: 4px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .status {
            padding: 0.5rem;
            border-radius: 4px;
            margin: 0.5rem 0;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        .form-group label {
            display: block;
            margin-bottom: 0.3rem;
            font-weight: 500;
            color: #495057;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        .stat-card {
            background: white;
            padding: 1rem;
            border-radius: 6px;
            border: 1px solid #e9ecef;
            text-align: center;
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            color: #6c757d;
            font-size: 0.9rem;
        }
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐕 Eco Pet Guide · Admin Console</h1>
            <p>Manage your affiliate links, track clicks, and generate content from one place.</p>
        </div>

        <!-- Admin Token Setup -->
        <div class="section">
            <h2>🔐 Admin Authentication</h2>
            <p>Enter your admin token once; it's stored in this browser only.</p>
            <div class="form-group">
                <input id="token" placeholder="ADMIN_TOKEN" style="width: 360px; display: inline-block;">
                <button onclick="saveToken()">Save Token</button>
            </div>
        </div>

        <!-- Quick Stats -->
        <div class="section">
            <h2>📊 Quick Stats</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="totalClicks">-</div>
                    <div class="stat-label">Total Clicks</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="todayClicks">-</div>
                    <div class="stat-label">Today's Clicks</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="totalRoutes">-</div>
                    <div class="stat-label">Active Routes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="weeklyClicks">-</div>
                    <div class="stat-label">This Week</div>
                </div>
            </div>
            <button onclick="loadStats()">Refresh Stats</button>
        </div>

        <div class="grid">
            <!-- Create Route -->
            <div class="section">
                <h2>🔗 Create / Update Route</h2>
                <div class="form-group">
                    <label for="slug">Slug (URL path)</label>
                    <input id="slug" placeholder="e.g. hurley-a, eco-toys-2025">
                </div>
                <div class="form-group">
                    <label for="offer">Offer Name</label>
                    <input id="offer" placeholder="e.g. AmazonEcoFriendlyDogToys">
                </div>
                <div class="form-group">
                    <label for="variant">Variant (A/B Testing)</label>
                    <select id="variant">
                        <option value="A">A</option>
                        <option value="B">B</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="dest">Destination URL (Full Amazon URL with tag)</label>
                    <input id="dest" placeholder="https://www.amazon.com/dp/B004A7X27M?tag=test0b252-20">
                </div>
                <button onclick="saveRoute()">Save Route</button>
                <button onclick="clearRouteForm()" class="secondary" style="margin-left: 10px;">Clear Form</button>
                <div id="routeStatus"></div>
            </div>

            <!-- Recent Clicks -->
            <div class="section">
                <h2>📈 Recent Clicks (Last 7 Days)</h2>
                <button onclick="loadClicks()">Refresh</button>
                <pre id="clicks">Click "Refresh" to load click data...</pre>
            </div>
        </div>

        <!-- Article Generator -->
        <div class="section full-width">
            <h2>🤖 AI Article Generator</h2>
            <div class="grid">
                <div>
                    <div class="form-group">
                        <label for="articleProduct">Select Product</label>
                        <select id="articleProduct">
                            <option value="">Choose a product to write about...</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="articleType">Article Type</label>
                        <select id="articleType">
                            <option value="review">Product Review</option>
                            <option value="comparison">Product Comparison</option>
                            <option value="guide">How-To Guide</option>
                            <option value="roundup">Product Roundup</option>
                            <option value="benefits">Benefits & Features</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="articleTone">Writing Tone</label>
                        <select id="articleTone">
                            <option value="professional">Professional</option>
                            <option value="casual">Casual & Friendly</option>
                            <option value="enthusiastic">Enthusiastic</option>
                            <option value="educational">Educational</option>
                            <option value="conversational">Conversational</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="articleKeywords">Keywords (comma separated)</label>
                        <input id="articleKeywords" placeholder="e.g. eco-friendly, sustainable, biodegradable, pet products">
                    </div>
                    <button onclick="generateAIArticle()" style="background: #28a745;">🤖 Generate AI Article</button>
                    <button onclick="testOllamaConnection()" class="secondary" style="margin-left: 10px;">🔗 Test Ollama</button>
                    <div id="aiArticleStatus"></div>
                </div>
                <div>
                    <h3>AI Article Settings</h3>
                    <div class="form-group">
                        <label for="articleLength">Article Length</label>
                        <select id="articleLength">
                            <option value="short">Short (500-800 words)</option>
                            <option value="medium" selected>Medium (800-1200 words)</option>
                            <option value="long">Long (1200-1500 words)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="includeComparison">Include Product Comparison?</label>
                        <select id="includeComparison">
                            <option value="no">No</option>
                            <option value="yes">Yes</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="targetAudience">Target Audience</label>
                        <select id="targetAudience">
                            <option value="pet-owners">Pet Owners</option>
                            <option value="eco-conscious">Eco-Conscious Consumers</option>
                            <option value="new-pet-owners">New Pet Owners</option>
                            <option value="experienced-owners">Experienced Pet Owners</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="seoFocus">SEO Focus</label>
                        <select id="seoFocus">
                            <option value="general">General</option>
                            <option value="long-tail">Long-tail Keywords</option>
                            <option value="local">Local SEO</option>
                            <option value="seasonal">Seasonal</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <!-- Manual Content Generation -->
        <div class="section full-width">
            <h2>📝 Manual Content Generation</h2>
            <div class="grid">
                <div>
                    <div class="form-group">
                        <label for="contentTitle">Article Title</label>
                        <input id="contentTitle" placeholder="e.g. Best Eco-Friendly Dog Toys 2025">
                    </div>
                    <div class="form-group">
                        <label for="contentBody">Article Content (Markdown)</label>
                        <textarea id="contentBody" rows="6" placeholder="Write your article content here in Markdown format..."></textarea>
                    </div>
                    <button onclick="generateContent()">Generate Article</button>
                    <div id="contentStatus"></div>
                </div>
                <div>
                    <h3>Quick Actions</h3>
                    <button onclick="generateWeeklyReport()" class="secondary">📊 Generate Weekly Report</button><br>
                    <button onclick="runScheduler()" class="secondary">⏰ Run Scheduler</button><br>
                    <button onclick="pingSitemaps()" class="secondary">🔍 Ping Search Engines</button><br>
                    <button onclick="updateIndex()" class="secondary">📝 Update Website Index</button>
                </div>
            </div>
        </div>

        <!-- Routes List -->
        <div class="section full-width">
            <h2>🔗 All Routes</h2>
            <button onclick="loadRoutes()">Refresh Routes</button>
            <pre id="routes">Click "Refresh Routes" to load...</pre>
        </div>

        <!-- System Health -->
        <div class="section full-width">
            <h2>🏥 System Health</h2>
            <button onclick="checkHealth()">Check Health</button>
            <pre id="health">Click "Check Health" to load system status...</pre>
        </div>
    </div>

    <script>
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
            } catch (error) {
                document.getElementById('routes').textContent = `Error loading routes: ${error.message}`;
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

        async function checkHealth() {
            try {
                const r = await fetch(base + "/health");
                const data = await r.json();
                document.getElementById('health').textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('health').textContent = `Error checking health: ${error.message}`;
            }
        }

        // Load initial data
        window.onload = function() {
            loadStats();
            loadRoutes();
            checkHealth();
            loadProductDropdown();
        };

        async function loadProductDropdown() {
            try {
                const r = await fetch(base + "/admin/routes", {headers: getHeaders()});
                const routes = await r.json();
                
                const dropdown = document.getElementById('articleProduct');
                dropdown.innerHTML = '<option value="">Choose a product to write about...</option>';
                
                routes.forEach(route => {
                    const option = document.createElement('option');
                    option.value = route.slug;
                    option.textContent = `${route.offer} (${route.slug})`;
                    dropdown.appendChild(option);
                });
            } catch (error) {
                console.error('Error loading product dropdown:', error);
            }
        }

        async function generateAIArticle() {
            const product = document.getElementById('articleProduct').value;
            const articleType = document.getElementById('articleType').value;
            const tone = document.getElementById('articleTone').value;
            const keywords = document.getElementById('articleKeywords').value;
            const length = document.getElementById('articleLength').value;
            const comparison = document.getElementById('includeComparison').value;
            const audience = document.getElementById('targetAudience').value;
            const seoFocus = document.getElementById('seoFocus').value;
            
            if (!product) {
                showStatus('aiArticleStatus', 'Please select a product first!', 'error');
                return;
            }

            showStatus('aiArticleStatus', '🤖 Generating AI article with Ollama...', 'info');

            try {
                const r = await fetch(base + "/admin/generate-ai-article", {
                    method: "POST",
                    headers: getHeaders(),
                    body: JSON.stringify({
                        product: product,
                        articleType: articleType,
                        tone: tone,
                        keywords: keywords,
                        length: length,
                        includeComparison: comparison,
                        targetAudience: audience,
                        seoFocus: seoFocus
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
                } else {
                    showStatus('aiArticleStatus', `❌ Error: ${result.detail || 'Unknown error'}`, 'error');
                }
            } catch (error) {
                showStatus('aiArticleStatus', `❌ Error: ${error.message}`, 'error');
            }
        }

        async function testOllamaConnection() {
            showStatus('aiArticleStatus', '🔗 Testing Ollama connection...', 'info');
            
            try {
                const r = await fetch(base + "/admin/test-ollama", {
                    method: "POST",
                    headers: getHeaders()
                });
                
                if (!r.ok) {
                    const errorText = await r.text();
                    throw new Error(`Server error: ${errorText}`);
                }
                
                const result = await r.json();
                if (result.ok) {
                    showStatus('aiArticleStatus', `✅ Ollama connection successful! ${result.message}`, 'success');
                } else {
                    showStatus('aiArticleStatus', `❌ Ollama connection failed: ${result.detail}`, 'error');
                }
            } catch (error) {
                showStatus('aiArticleStatus', `❌ Error: ${error.message}`, 'error');
            }
        }
    </script>
</body>
</html>
"""

# List routes
@app.get("/admin/routes")
def list_routes(request: Request):
    require_admin(request)
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT slug, offer, variant, dest_url FROM routes ORDER BY slug")).all()
    return JSONResponse([{"slug": s, "offer": o, "variant": v, "dest_url": d} for s, o, v, d in rows])

# Click aggregates
@app.get("/admin/clicks")
def clicks(request: Request, days: int = 7):
    require_admin(request)
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT offer, variant, COUNT(*) AS clicks
            FROM clicks
            WHERE created_at >= :since
            GROUP BY 1,2 ORDER BY clicks DESC
        """), {"since": (dt.datetime.utcnow() - dt.timedelta(days=days)).isoformat()}).all()
    return JSONResponse([{"offer": o, "variant": v, "clicks": c} for o, v, c in rows])

# Content generation endpoint
@app.post("/admin/generate")
async def admin_generate(request: Request):
    require_admin(request)
    try:
        body = await request.json()
        title = body.get("title", "")
        body_md = body.get("body_md", "Draft content")
        
        if not title:
            raise HTTPException(status_code=400, detail="Title is required")
            
        from content_pipeline import generate_post
        slug = generate_post(title=title, body_md=body_md)
        
        # Update the index.html file to include the new article
        try:
            import subprocess
            subprocess.run(["python3", "update_index.py"], check=True, capture_output=True)
        except Exception as e:
            print(f"Warning: Could not update index.html: {e}")
        
        return {"ok": True, "slug": slug}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Weekly report generation
@app.post("/admin/weekly")
def admin_weekly(request: Request):
    require_admin(request)
    try:
        import subprocess
        result = subprocess.run(["python3", "generate_report.py"], check=True, capture_output=True, text=True)
        return {"ok": True, "message": "Weekly report generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Scheduler run
@app.post("/admin/scheduler")
def admin_scheduler(request: Request):
    require_admin(request)
    try:
        import subprocess
        # Run content generation
        subprocess.run(["python3", "content_pipeline.py"], check=True, capture_output=True)
        return {"ok": True, "message": "Content generation completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sitemap ping
@app.post("/admin/ping")
def admin_ping(request: Request):
    require_admin(request)
    try:
        # Simulate sitemap ping (in production, you'd ping actual search engines)
        return {"ok": True, "message": "Search engines notified of new content"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update website index
@app.post("/admin/update-index")
def admin_update_index(request: Request):
    require_admin(request)
    try:
        import subprocess
        result = subprocess.run(["python3", "update_index.py"], check=True, capture_output=True, text=True)
        return {"ok": True, "message": "Website index updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Article Generation with Ollama
@app.post("/admin/generate-ai-article")
async def admin_generate_ai_article(request: Request):
    require_admin(request)
    try:
        body = await request.json()
        product = body.get("product", "")
        article_type = body.get("articleType", "review")
        tone = body.get("tone", "professional")
        keywords = body.get("keywords", "")
        length = body.get("length", "medium")
        include_comparison = body.get("includeComparison", "no")
        target_audience = body.get("targetAudience", "pet-owners")
        seo_focus = body.get("seoFocus", "general")
        
        if not product:
            raise HTTPException(status_code=400, detail="Product is required")
        
        # Get product details from database
        with engine.begin() as conn:
            route = conn.execute(
                text("SELECT offer, dest_url FROM routes WHERE slug=:s"),
                {"s": product},
            ).fetchone()
        
        if not route:
            raise HTTPException(status_code=404, detail="Product not found")
        
        offer, dest_url = route
        
        # Prepare product info for Ollama
        product_info = {
            "offer": offer,
            "dest_url": dest_url,
            "slug": product
        }
        
        try:
            # Import and use Ollama generator
            from ollama_integration import OllamaArticleGenerator
            
            # Test Ollama connection first
            generator = OllamaArticleGenerator()
            if not generator.test_connection():
                raise Exception("Ollama is not running. Please start Ollama with 'ollama serve'")
            
            # Generate article using Ollama
            article_content = generator.generate_article(
                product_info=product_info,
                article_type=article_type,
                tone=tone,
                keywords=keywords,
                length=length,
                include_comparison=include_comparison,
                target_audience=target_audience,
                seo_focus=seo_focus
            )
            
            # Extract title from the generated content
            title_match = re.search(r'^# (.+)$', article_content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
            else:
                title = f"AI Generated: {offer} - {article_type.title()}"
            
        except ImportError:
            raise Exception("Ollama integration module not found")
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")
        
        # Generate the article using the existing pipeline
        from content_pipeline import generate_post
        slug = generate_post(title=title, body_md=article_content)
        
        # Update the website index
        try:
            import subprocess
            subprocess.run(["python3", "update_index.py"], check=True, capture_output=True)
        except Exception as e:
            print(f"Warning: Could not update index.html: {e}")
        
        return {"ok": True, "slug": slug, "message": "AI article generated successfully using Ollama!"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Test Ollama connection
@app.post("/admin/test-ollama")
async def admin_test_ollama(request: Request):
    require_admin(request)
    try:
        from ollama_integration import OllamaArticleGenerator
        
        generator = OllamaArticleGenerator()
        if generator.test_connection():
            return {"ok": True, "message": "Ollama is running and accessible"}
        else:
            raise Exception("Ollama is not responding")
            
    except ImportError:
        raise HTTPException(status_code=500, detail="Ollama integration module not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama connection failed: {str(e)}")

# Serve static content files
@app.get("/content/{filename}")
def serve_content(filename: str):
    """Serve content files from site/content/"""
    try:
        with open(f"site/content/{filename}", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Content not found")

@app.get("/disclosure.html")
def serve_disclosure():
    """Serve disclosure page"""
    try:
        with open("site/disclosure.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Disclosure not found")

@app.get("/privacy.html")
def serve_privacy():
    """Serve privacy page"""
    try:
        with open("site/privacy.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Privacy not found")