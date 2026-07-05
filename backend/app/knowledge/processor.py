from typing import BinaryIO, Dict, Any
import csv
import io
import markdown

class DocumentProcessor:
    """Extracts raw text and metadata from various file formats."""
    
    def extract(self, file_stream: BinaryIO, file_type: str) -> Dict[str, Any]:
        """Routes to the correct extractor based on file type."""
        file_type = file_type.lower()
        if file_type == "pdf":
            return self._extract_pdf(file_stream)
        elif file_type == "docx":
            return self._extract_docx(file_stream)
        elif file_type == "txt":
            return self._extract_txt(file_stream)
        elif file_type == "md" or file_type == "markdown":
            return self._extract_md(file_stream)
        elif file_type == "csv":
            return self._extract_csv(file_stream)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def _extract_pdf(self, file_stream: BinaryIO) -> Dict[str, Any]:
        from pypdf import PdfReader
        reader = PdfReader(file_stream)
        full_text = ""
        page_map = {}
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            full_text += text + "\n\n"
            page_map[i+1] = text
        return {"full_text": full_text.strip(), "page_map": page_map}

    def _extract_docx(self, file_stream: BinaryIO) -> Dict[str, Any]:
        from docx import Document as DocxDocument
        doc = DocxDocument(file_stream)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return {"full_text": full_text, "page_map": {1: full_text}}

    def _extract_txt(self, file_stream: BinaryIO) -> Dict[str, Any]:
        content = file_stream.read().decode("utf-8")
        return {"full_text": content, "page_map": {1: content}}

    def _extract_md(self, file_stream: BinaryIO) -> Dict[str, Any]:
        content = file_stream.read().decode("utf-8")
        # Optional: strip markdown tags if we want pure text, or just keep it
        return {"full_text": content, "page_map": {1: content}}
        
    def _extract_csv(self, file_stream: BinaryIO) -> Dict[str, Any]:
        """Converts CSV rows into readable context for RAG."""
        content = file_stream.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        
        full_text = ""
        for i, row in enumerate(reader):
            row_str = ", ".join(f"{k}: {v}" for k, v in row.items())
            full_text += f"Row {i+1}: {row_str}\n"
            
        return {"full_text": full_text.strip(), "page_map": {1: full_text}}
