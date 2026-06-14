import time
from pathlib import Path
from llama_cpp import Llama


class LocalLLMClient:
    def __init__(
        self,
        model_path: str,
        n_gpu_layers: int = 0,
        context_length: int = 2048,
    ):
        self.model_path = str(model_path)
        self.n_gpu_layers = n_gpu_layers
        self.context_length = context_length
        self.model_name = Path(model_path).stem
        self._llm: Llama | None = None

    def _load(self):
        if self._llm is None:
            self._llm = Llama(
                model_path=self.model_path,
                n_ctx=self.context_length,
                n_gpu_layers=self.n_gpu_layers,
                chat_format="chatml",
                verbose=False,
            )

    def generate(self, prompt: str, max_tokens: int = 300) -> tuple[str, int]:
        self._load()
        start = time.time()
        output = self._llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.15,
            repeat_penalty=1.1,
            top_p=0.9,
            stop=["<|im_end|>", "<|im_start|>", "User:", "###"],
        )
        latency_ms = int((time.time() - start) * 1000)
        text = output["choices"][0]["text"].strip()
        return text, latency_ms
