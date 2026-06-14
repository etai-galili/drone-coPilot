import json
from pathlib import Path

import tiktoken

INPUT_DIR = Path("data/raw")
OUTPUT_PATH = Path("data/chunks/all_chunks.jsonl")
CHUNK_TOKENS = 400
OVERLAP_TOKENS = 80
ENCODING_NAME = "cl100k_base"


def detect_section(lines: list[str], char_offset: int, full_text: str) -> str:
    text_so_far = full_text[:char_offset]
    last_lines = text_so_far.split("\n")[-8:]
    for line in reversed(last_lines):
        line = line.strip()
        if 4 < len(line) < 100 and not line.endswith(".") and not line.endswith(","):
            return line
    return "General"


def chunk_text(text: str, slug: str, enc: tiktoken.Encoding) -> list[dict]:
    tokens = enc.encode(text)
    chunks = []
    idx = 0
    chunk_index = 0

    while idx < len(tokens):
        end = min(idx + CHUNK_TOKENS, len(tokens))
        chunk_tokens = tokens[idx:end]
        chunk_str = enc.decode(chunk_tokens)

        char_offset = len(enc.decode(tokens[:idx]))
        section = detect_section([], char_offset, text)

        chunks.append({
            "text": chunk_str,
            "source": slug,
            "section_title": section,
            "chunk_index": chunk_index,
            "char_count": len(chunk_str),
        })

        chunk_index += 1
        idx += CHUNK_TOKENS - OVERLAP_TOKENS

    return chunks


def main():
    enc = tiktoken.get_encoding(ENCODING_NAME)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    txt_files = sorted(INPUT_DIR.glob("*.txt"))
    if not txt_files:
        print(f"[ERR] No .txt files in {INPUT_DIR}. Run fetch_docs.py first.")
        return

    print(f"\n{'=' * 50}")
    print("AVATA CO-PILOT — Chunking documents")
    print(f"{'=' * 50}\n")
    print(f"Settings: {CHUNK_TOKENS} tokens/chunk, {OVERLAP_TOKENS} token overlap\n")

    all_chunks: list[dict] = []
    for path in txt_files:
        slug = path.stem
        text = path.read_text(encoding="utf-8")
        chunks = chunk_text(text, slug, enc)
        all_chunks.extend(chunks)
        token_count = len(enc.encode(text))
        print(f"  {slug}: {token_count:,} tokens → {len(chunks)} chunks")

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"\nTotal: {len(all_chunks)} chunks from {len(txt_files)} sources")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
