import uuid
from typing import BinaryIO
from app.core.logging import get_workflow_logger
from .models import Document, DocumentMetadata
from .processor import DocumentProcessor

logger = get_workflow_logger()

class UploadService:
    """Handles secure file upload and MIME type routing."""
    
    def __init__(self):
        self.processor = DocumentProcessor()
        
    async def process_upload(self, file_stream: BinaryIO, filename: str, workspace_id: str, uploader_id: str) -> Document:
        """Processes an uploaded file into a unified Document object."""
        logger.info("document_upload_started", f"Processing {filename}")
        
        doc_id = f"doc-{uuid.uuid4().hex[:8]}"
        
        # 1. Determine type
        extension = filename.split(".")[-1].lower() if "." in filename else "txt"
        
        # 2. Extract text and pages
        parsed_data = self.processor.extract(file_stream, extension)
        
        # 3. Construct Metadata
        metadata = DocumentMetadata(
            title=filename,
            workspace_id=workspace_id,
            document_type=extension,
            owner=uploader_id
        )
        
        doc = Document(
            document_id=doc_id,
            content=parsed_data["full_text"],
            metadata=metadata
        )
        
        # Temporary holding of page map in model dump is possible but we will rely on chunks
        doc._page_map = parsed_data.get("page_map", {})
        
        logger.info("document_upload_completed", f"Extracted {len(parsed_data['full_text'])} chars")
        return doc
