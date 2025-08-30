from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import UploadRequest, UploadResponse
from app.services.rag_pipeline import RAGPipeline
from app.utils.text_processing import extract_text_from_file
from app.utils.security import is_valid_file, clean_for_log
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
rag_pipeline = RAGPipeline()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    try:
        if not file and not text:
            raise HTTPException(status_code=400, detail="Either file or text must be provided")
        
        if file:
            if not is_valid_file(file.filename):
                raise HTTPException(status_code=400, detail="File type not allowed. Only TXT, MD, PDF, DOCX files are supported.")
            content = await file.read()
            document_text = extract_text_from_file(content, file.filename)
            filename = file.filename
        else:
            document_text = text
            filename = "text_input.txt"
        
        if not document_text.strip():
            raise HTTPException(status_code=400, detail="Document text is empty")
        
        doc_id = rag_pipeline.process_document(document_text, filename)
        
        return UploadResponse(
            message="Document uploaded and processed successfully",
            document_id=doc_id,
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Upload error: {clean_for_log(str(e))}")
        raise HTTPException(status_code=500, detail=str(e))