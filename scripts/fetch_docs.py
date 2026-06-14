import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

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


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n{'=' * 50}")
    print("AVATA CO-PILOT — Fetching documentation")
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
    print(f"Done: {ok}/{len(results)} sources fetched")
    print(f"Total text: {total_chars:,} characters")
    print(f"Output: {OUTPUT_DIR}/")

    if ok < len(results):
        print("\n[NOTE] Some sources failed. The system will still work with partial data.")
        print("       You can manually add text files to data/raw/ if needed.")


if __name__ == "__main__":
    main()
