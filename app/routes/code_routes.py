from fastapi import APIRouter, HTTPException
from app.services.gpt_service import GPTService
from app.schemas.code_schema import CodeRequest, CodeResponse, MarkdownRequest, FixRequest
from app.utils.generate_nuxt_files import NuxtFileGenerator, NuxtFileUpdater
from app.utils.generate_nuxt_file_plan import NuxtFilePlanGenerator

router = APIRouter()

gpt_service = GPTService()


@router.post("/generate-code", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    try:
        code = gpt_service.generate_code(request.instruction)
        return {"generated_code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-nuxt-files")
async def generate_nuxt_files(request: MarkdownRequest):
    """
    Markdown設計書に基づいて、生成するファイルのリストを生成し、実際にファイルを生成するエンドポイント。
    """
    try:
        # Step 1: Markdownからファイルの生成計画を作成
        plan_generator = NuxtFilePlanGenerator()
        plan = plan_generator.generate_plan_from_markdown(request.markdown)

        # Step 2: 生成されたファイルの計画に基づいてファイルを生成
        generator = NuxtFileGenerator()
        generated_files = []
        for item in plan:
            file_path = item['file_path']
            description = item['description']
            code = generator.generate_file(
                file_path, description, request.markdown, plan)
            generated_files.append({
                "file_path": file_path,
                "description": description,
                "generated_code": code
            })

        generator.update_overview_with_gpt(generated_files)

        return {"generated_files": generated_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fix-code")
def fix_code(request: FixRequest):
    try:
        updater = NuxtFileUpdater()

        # 修正箇所を特定
        fixes = updater.identify_fixes(request.change_description)

        # 修正を適用
        result = updater.apply_fixes(fixes)

        return {"status": "success", "details": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
