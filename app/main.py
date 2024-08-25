from fastapi import FastAPI
from app.routes import code_routes

app = FastAPI()

# コード生成用のルートを追加
app.include_router(code_routes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the GPT-4 Code Generator API"}
