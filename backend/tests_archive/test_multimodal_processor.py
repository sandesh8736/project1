import unittest
from unittest.mock import Mock

from services.multimodal.multimodal_processor import MultimodalProcessor


class MultimodalProcessorTests(unittest.TestCase):
    def setUp(self):
        self.processor = MultimodalProcessor("uploads/example.pdf")
        self.text_processor = Mock(
            process=Mock(
                return_value=[
                    {"page_number": 1, "text": "  First page  "},
                    {"page_number": 2, "text": "   "},
                ]
            )
        )
        self.image_extractor = Mock(process=Mock(return_value=["processed/image.png"]))
        self.table_extractor = Mock(
            process=Mock(return_value=[{"page_number": 1, "data": [["A"]]}])
        )
        self.ocr_processor = Mock(
            process=Mock(return_value=[{"page_number": 2, "text": "OCR text"}])
        )

        self.processor._create_text_processor = Mock(return_value=self.text_processor)
        self.processor._create_image_extractor = Mock(return_value=self.image_extractor)
        self.processor._create_table_extractor = Mock(return_value=self.table_extractor)
        self.processor._create_ocr_processor = Mock(return_value=self.ocr_processor)

    def test_process_combines_each_modality(self):
        document = self.processor.process()

        self.assertEqual(
            document,
            {
                "text": [{"page_number": 1, "text": "First page"}],
                "images": ["processed/image.png"],
                "tables": [{"page_number": 1, "data": [["A"]]}],
                "ocr": [{"page_number": 2, "text": "OCR text"}],
            },
        )
        for component in (
            self.text_processor,
            self.image_extractor,
            self.table_extractor,
            self.ocr_processor,
        ):
            component.process.assert_called_once_with()

    def test_process_resets_data_from_a_previous_run(self):
        self.processor.document_data["text"].append({"page_number": 99, "text": "stale"})

        document = self.processor.process()

        self.assertEqual(document["text"], [{"page_number": 1, "text": "First page"}])


if __name__ == "__main__":
    unittest.main()
