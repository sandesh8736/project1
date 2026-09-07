from collections.abc import Iterable
from pathlib import Path
from typing import Any

from PIL import Image


class ImageUnderstanding:

    def __init__(
        self,
        model_name="Salesforce/blip-image-captioning-base"
    ):
        self.model_name = model_name
        self.model = None

    def load_model(self) -> None:
        """Load the captioning model on first use."""
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError(
                "Image captioning requires the optional 'transformers' dependency. "
                "Install backend/requirements.txt in the active Python environment."
            ) from exc

        self.model = pipeline("image-text-to-text", model=self.model_name)

    def understand(self, image_path: str | Path) -> str:
        image_path = Path(image_path)
        if not image_path.is_file():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        if self.model is None:
            self.load_model()

        with Image.open(image_path) as image:
            # Detach the image from the file before it is closed.
            image = image.convert("RGB")
            result = self.model(
                image,
                max_new_tokens=100
            )

        try:
            description = result[0]["generated_text"]
        except (IndexError, KeyError, TypeError) as exc:
            raise RuntimeError(
                f"Captioning model returned an unexpected response: {result!r}"
            ) from exc

        return description

    def process(self, image_paths: str | Path | Iterable[str | Path]) -> list[dict[str, Any]]:
        """Caption one image path or an iterable of image paths."""
        if isinstance(image_paths, (str, Path)):
            image_paths = [image_paths]

        results = []
        for image_path in image_paths:
            path = Path(image_path)
            results.append(
                {
                    "image_path": str(path),
                    "description": self.understand(path),
                }
            )

        return results
