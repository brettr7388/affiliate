import os
import uuid
import datetime as dt
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Use SQLite by default; override via the DATABASE_URL env var
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./affiliate.db")
engine = create_engine(DATABASE_URL, future=True)

app = FastAPI()


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
def create_route(r: Route) -> dict[str, bool]:
    """Create or update a short redirect route.

    You can POST a JSON body like:
    {"slug":"eco-toy","offer":"AmazonEcoFriendlyDogToys","variant":"A",
     "dest_url":"https://example.com"}
    to register a new redirect.
    """
    with engine.begin() as conn:
        conn.execute(
            text(
                "REPLACE INTO routes(slug,offer,variant,dest_url) VALUES(:s,:o,:v,:d)"
            ),
            {"s": r.slug, "o": r.offer, "v": r.variant, "d": r.dest_url},
        )
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