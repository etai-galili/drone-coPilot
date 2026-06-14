import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = Path("data/chunks/all_chunks.jsonl")
CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "avata_copilot_v1"
BATCH_SIZE = 64

SELF_TEST_QUERIES = [
    "What is the maximum flight time of the DJI Avata?",
    "How do I activate Return to Home on DJI Avata?",
    "What do the LED status codes mean on DJI Avata?",
]


def main():
    if not CHUNKS_PATH.exists():
        print(f"[ERR] {CHUNKS_PATH} not found. Run chunk_docs.py first.")
        return

    print(f"\n{'=' * 50}")
    print("AVATA CO-PILOT — Building vector index")
    print(f"{'=' * 50}\n")

    print("Loading embedding model (sentence-transformers/all-MiniLM-L6-v2)...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("  Embedding model loaded.\n")

    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"  Cleared existing collection: {COLLECTION_NAME}")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    print(f"  Created collection: {COLLECTION_NAME}\n")

    chunks: list[dict] = []
    with CHUNKS_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))

    print(f"Indexing {len(chunks)} chunks...")
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        texts = [c["text"] for c in batch]
        embeddings = model.encode(texts, show_progress_bar=False).tolist()
        ids = [f"chunk_{i + j}" for j in range(len(batch))]
        metadatas = [{k: v for k, v in c.items() if k != "text"} for c in batch]
        collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)
        done = min(i + BATCH_SIZE, len(chunks))
        print(f"  Indexed {done}/{len(chunks)}", end="\r")

    print(f"\n  Done. {len(chunks)} chunks indexed.\n")

    print("--- Self-Test ---")
    for query in SELF_TEST_QUERIES:
        emb = model.encode(query).tolist()
        results = collection.query(query_embeddings=[emb], n_results=3)
        print(f"\nQuery: {query}")
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            score = round(1 - float(dist), 4)
            source = meta.get("source", "?")
            preview = doc[:90].replace("\n", " ")
            print(f"  [{score:.4f}] {source} — {preview}...")

    print("\n[OK] Index built successfully.")


if __name__ == "__main__":
    main()
