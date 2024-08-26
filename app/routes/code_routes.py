from fastapi import APIRouter, HTTPException
from app.services.gpt_service import GPTService
from app.schemas.code_schema import CodeRequest, CodeResponse, MarkdownRequest
from app.utils.generate_nuxt_files import NuxtFileGenerator

router = APIRouter()

gpt_service = GPTService()


@router.post("/generate-code", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    try:
        code = gpt_service.generate_code(request.instruction)
        return {"generated_code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-nuxt")
async def generate_nuxt_files(request: MarkdownRequest):
    try:
        generator = NuxtFileGenerator()
        files = generator.generate_from_markdown(request.markdown)

        # 生成されたファイルとその説明を返す
        response = [{"file_path": file[0], "content": file[1]}
                    for file in files]
        return {"generated_files": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
