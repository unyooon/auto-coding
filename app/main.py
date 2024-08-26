from fastapi import FastAPI
from app.routes import code_routes
from app.utils.generate_nuxt_files import NuxtFileGenerator

app = FastAPI()

# アプリケーションの初期化時に、Nuxtプロジェクトを確認・生成


@app.on_event("startup")
async def startup_event():
    # Nuxt 3プロジェクトを初期化
    generator = NuxtFileGenerator()
    generator.ensure_directories()

# コード生成用のルートを追加
app.include_router(code_routes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the GPT-4 Nuxt.js Code Generator API"}
