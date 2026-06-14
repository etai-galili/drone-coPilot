from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

# requests / bs4 are imported lazily inside the --web path so that building the
# authoritative knowledge base from data/seed/ works fully offline with no
# scraping dependencies installed.

# Curated, version-controlled, verified DJI Avata 2 documentation. This is the
# authoritative knowledge base: it is deterministic, offline, and trustworthy,
# unlike scraped web pages which mix Avata 1/2 facts and contain stale specs.
SEED_DIR = Path("data/seed")

# Optional supplementary web sources. Disabled by default to keep the knowledge
# base reliable and reproducible. Enable with: python scripts/fetch_docs.py --web
SOURCES = {
    "dji_avata_manualslib": "https://www.manualslib.com/manual/2833828/Dji-Avata.html",
    "dji_avata_manualsplus": "https://manuals.plus/m/7821e4e36bf6bce7d4da7c7723396daa1e09bf6253aa4239f7eab923979c7ffe",
    "dji_support_avata": "https://support.dji.com/help/content?customId=en-us03400006874&spaceId=34&re=US&lang=en",
    "dronespec_avata": "https://dronespec.dronedesk.io/dji-avata",
    "dji_avata2_specs": "https://www.dji.com/avata-2/specs",
    "wikipedia_dji_avata": "https://en.wikipedia.org/wiki/DJI_Avata",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

OUTPUT_DIR = Path("data/raw")

REMOVE_SELECTORS = [
    "nav", "footer", "header", "script", "style", "aside",
    "iframe", "form", "noscript", "advertisement", "cookie-banner",
    ".nav", ".footer", ".header", ".sidebar", ".ads", ".cookie",
    ".advertisement", ".navbar", ".menu", ".breadcrumb",
    "#nav", "#footer", "#header", "#sidebar", "#cookie",
]


def extract_text(soup: BeautifulSoup) -> str:
    for selector in REMOVE_SELECTORS:
        for el in soup.select(selector):
            el.decompose()

    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find(attrs={"role": "main"})
        or soup.find(id=lambda x: x and "content" in x.lower() if x else False)
        or soup.find(class_=lambda x: x and "content" in " ".join(x).lower() if x else False)
        or soup.body
        or soup
    )

    text = main.get_text(separator="\n", strip=True)
    lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 3]
    return "\n".join(lines)


def fetch_and_save(slug: str, url: str) -> dict:
    import requests
    from bs4 import BeautifulSoup

    log = {
        "slug": slug,
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "error",
        "char_count": 0,
    }
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        text = extract_text(soup)

        if len(text) < 200:
            log["status"] = "too_short"
            log["char_count"] = len(text)
            print(f"  [WARN] {slug}: only {len(text)} chars — saving anyway")

        out_path = OUTPUT_DIR / f"{slug}.txt"
        out_path.write_text(text, encoding="utf-8")
        log["status"] = "ok"
        log["char_count"] = len(text)
        print(f"  [OK]   {slug}: {len(text):,} chars → {out_path}")

    except requests.HTTPError as e:
        log["error"] = f"HTTP {e.response.status_code}"
        print(f"  [ERR]  {slug}: HTTP {e.response.status_code}")
    except Exception as e:
        log["error"] = str(e)
        print(f"  [ERR]  {slug}: {e}")

    return log


def copy_seed_docs() -> int:
    """Copy the curated, verified Avata 2 docs into data/raw. Authoritative."""
    seed_files = sorted(SEED_DIR.glob("*.txt"))
    if not seed_files:
        print(f"  [WARN] No seed docs found in {SEED_DIR}/")
        return 0
    total_chars = 0
    for path in seed_files:
        text = path.read_text(encoding="utf-8")
        out_path = OUTPUT_DIR / path.name
        out_path.write_text(text, encoding="utf-8")
        total_chars += len(text)
        print(f"  [SEED] {path.name}: {len(text):,} chars → {out_path}")
    print(f"\n  Seeded {len(seed_files)} verified docs ({total_chars:,} chars)")
    return len(seed_files)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    use_web = "--web" in sys.argv

    print(f"\n{'=' * 50}")
    print("AVATA CO-PILOT — Building documentation (DJI Avata 2)")
    print(f"{'=' * 50}\n")

    print("Loading curated knowledge base (authoritative):")
    seeded = copy_seed_docs()

    if not use_web:
        print("\nWeb scraping disabled (default). The knowledge base is built from")
        print("the verified, version-controlled docs in data/seed/.")
        print("Run with --web to also pull supplementary online sources.")
        print(f"\nReady: {seeded} verified docs in {OUTPUT_DIR}/")
        return

    print(f"\n{'=' * 50}")
    print("Fetching supplementary web sources (--web)")
    print(f"{'=' * 50}\n")

    results = []
    for slug, url in SOURCES.items():
        print(f"Fetching: {slug}")
        result = fetch_and_save(slug, url)
        results.append(result)
        time.sleep(1.5)

    ok = sum(1 for r in results if r["status"] == "ok")
    total_chars = sum(r["char_count"] for r in results)
    print(f"\n{'=' * 50}")
    print(f"Done: {seeded} verified docs + {ok}/{len(results)} web sources fetched")
    print(f"Web text: {total_chars:,} characters")
    print(f"Output: {OUTPUT_DIR}/")

    if ok < len(results):
        print("\n[NOTE] Some web sources failed. The verified seed docs ensure the")
        print("       system still has a complete, reliable knowledge base.")


if __name__ == "__main__":
    main()
