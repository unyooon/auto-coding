from pydantic import BaseModel


class CodeRequest(BaseModel):
    instruction: str  # ユーザーがGPT-4に与える指示


class CodeResponse(BaseModel):
    generated_code: str  # GPT-4が生成したコード


class MarkdownRequest(BaseModel):
    markdown: str


class FixRequest(BaseModel):
    change_description: str
