import json
import platform
import subprocess
from pathlib import Path

MODELS_DIR = Path("models")
CONFIG_PATH = Path("config.json")

MODEL = {
    "repo_id": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
    "filename": "qwen2.5-1.5b-instruct-q4_k_m.gguf",
    "label": "Qwen2.5 1.5B Instruct Q4_K_M",
    "size_gb": 1.0,
}


def detect_backend() -> tuple[int, str]:
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return -1, "CUDA"
    except Exception:
        pass

    if platform.system() == "Darwin" and platform.machine() == "arm64":
        return -1, "Metal"

    return 0, "CPU"


def download_model() -> Path:
    from huggingface_hub import hf_hub_download

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    target = MODELS_DIR / MODEL["filename"]

    if target.exists():
        print(f"  Model already present: {target}")
        return target

    print(f"  Downloading {MODEL['label']} (~{MODEL['size_gb']} GB)...")
    path = hf_hub_download(
        repo_id=MODEL["repo_id"],
        filename=MODEL["filename"],
        local_dir=str(MODELS_DIR),
        local_dir_use_symlinks=False,
    )
    return Path(path)


def write_config(model_path: Path, n_gpu_layers: int, backend: str) -> None:
    config = {
        "model_path": str(model_path),
        "model_label": MODEL["label"],
        "n_gpu_layers": n_gpu_layers,
        "backend": backend,
        "chroma_path": "data/chroma_db",
        "context_length": 2048,
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    print(f"  Config saved: {CONFIG_PATH}")


def main():
    print(f"\n{'=' * 50}")
    print("AVATA CO-PILOT — Model Setup")
    print(f"{'=' * 50}\n")

    n_gpu_layers, backend = detect_backend()
    print(f"Backend detected: {backend} (n_gpu_layers={n_gpu_layers})")
    print(f"Model: {MODEL['label']}\n")

    model_path = download_model()
    print(f"  Model ready: {model_path}")

    write_config(model_path, n_gpu_layers, backend)

    print(f"\n[OK] Setup complete.")
    print(f"     Model : {MODEL['label']}")
    print(f"     Backend: {backend}")
    print(f"     Path  : {model_path}")


if __name__ == "__main__":
    main()
