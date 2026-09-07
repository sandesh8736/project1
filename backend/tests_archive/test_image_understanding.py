from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image
from services.multimodal.image_understanding import ImageUnderstanding


class ImageUnderstandingTests(unittest.TestCase):
    def test_understand_converts_an_image_to_rgb_and_returns_caption(self):
        received_modes = []

        def caption_model(image, **kwargs):
            received_modes.append(image.mode)
            self.assertEqual(kwargs["max_new_tokens"], 100)
            return [{"generated_text": "a test image"}]

        with TemporaryDirectory() as directory:
            image_path = Path(directory) / "image.png"
            Image.new("RGBA", (1, 1)).save(image_path)

            understanding = ImageUnderstanding()
            understanding.model = caption_model

            self.assertEqual(understanding.understand(image_path), "a test image")

        self.assertEqual(received_modes, ["RGB"])

    def test_understand_raises_for_a_missing_file_before_loading_model(self):
        with self.assertRaises(FileNotFoundError):
            ImageUnderstanding().understand("does-not-exist.png")

    def test_process_accepts_one_path_string(self):
        understanding = ImageUnderstanding()
        understanding.understand = lambda path: f"caption for {path}"

        results = understanding.process("image.png")

        self.assertEqual(
            results,
            [{"image_path": "image.png", "description": "caption for image.png"}],
        )

    def test_understand_rejects_an_unexpected_model_response(self):
        with TemporaryDirectory() as directory:
            image_path = Path(directory) / "image.png"
            Image.new("RGB", (1, 1)).save(image_path)

            understanding = ImageUnderstanding()
            understanding.model = lambda image, **kwargs: []

            with self.assertRaisesRegex(RuntimeError, "unexpected response"):
                understanding.understand(image_path)


if __name__ == "__main__":
    unittest.main()
