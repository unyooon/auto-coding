from fastapi import APIRouter, HTTPException
from app.services.gpt_service import GPTService
from app.schemas.code_schema import CodeRequest, CodeResponse

router = APIRouter()

gpt_service = GPTService()


@router.post("/generate-code", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    try:
        code = gpt_service.generate_code(request.instruction)
        return {"generated_code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
