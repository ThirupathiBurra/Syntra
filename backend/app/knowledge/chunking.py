import uuid
from typing import List
from .models import Document, DocumentChunk

class ChunkingService:
    """Chunks documents into embeddable pieces while retaining metadata."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: Document) -> List[DocumentChunk]:
        """Splits document content into chunks using simple token/character overlap."""
        text = document.content
        chunks = []
        
        # Simple character-based chunking for demonstration
        # In production, use langchain.text_splitter.RecursiveCharacterTextSplitter
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_content = text[start:end]
            
            # Create chunk
            chunk_id = f"chunk-{uuid.uuid4().hex[:8]}"
            
            # Simple page mapping (assuming 1 page for now if not using PDF)
            page_num = 1
            if hasattr(document, "_page_map"):
                # Rough estimation logic goes here
                pass
                
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                document_id=document.document_id,
                content=chunk_content,
                page_number=page_num,
                metadata={"title": document.metadata.title}
            )
            chunks.append(chunk)
            start += (self.chunk_size - self.chunk_overlap)
            
        return chunks
