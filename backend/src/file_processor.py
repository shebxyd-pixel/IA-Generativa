import os
import io
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from markitdown import MarkItDown


class FileProcessor:
    """Process files using MarkItDown to convert them to Markdown/LLM-ready content."""

    def __init__(self, enable_llm_image_processing: bool = False, llm_client=None, llm_model=None):
        self.markitdown = MarkItDown(
            llm_client=llm_client,
            llm_model=llm_model,
            enable_plugins=False
        )
        self.enable_llm_image_processing = enable_llm_image_processing

    def process_file(self, file_stream: io.BytesIO, filename: str) -> Dict[str, Any]:
        """
        Process a file stream and return the converted content.

        Args:
            file_stream: Binary stream of the file
            filename: Name of the file (for extension detection)

        Returns:
            Dictionary with processing results
        """
        try:
            result = self.markitdown.convert_stream(
                file_stream,
                stream_info=self.markitdown._get_stream_info_guesses(
                    file_stream,
                    self.markitdown._base_guess(filename=filename)
                )[0] if hasattr(self.markitdown, '_base_guess') else None
            )

            return {
                "success": True,
                "text_content": result.text_content,
                "markdown": getattr(result, "markdown", None) or result.text_content,
                "filename": filename,
                "file_type": os.path.splitext(filename)[1].lstrip(".") or "unknown"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filename": filename
            }

    def process_local_file(self, file_path: str) -> Dict[str, Any]:
        """Process a local file."""
        try:
            result = self.markitdown.convert_local(file_path)
            return {
                "success": True,
                "text_content": result.text_content,
                "markdown": getattr(result, "markdown", None) or result.text_content,
                "filename": os.path.basename(file_path),
                "file_type": os.path.splitext(file_path)[1].lstrip(".") or "unknown"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filename": os.path.basename(file_path)
            }

    @staticmethod
    def is_supported_file(filename: str) -> bool:
        """Check if the file extension is supported."""
        supported_extensions = {
            ".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".csv", ".txt", ".md",
            ".html", ".htm", ".xml", ".json", ".yaml", ".yml", ".rtf",
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff",
            ".wav", ".mp3", ".m4a", ".ogg", ".flac",
            ".epub", ".zip", ".msg", ".ipynb"
        }
        ext = os.path.splitext(filename)[1].lower()
        return ext in supported_extensions
