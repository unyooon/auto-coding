from pydantic import BaseModel


# 設計書(Design document)のデータベーススキーマを定義
class DesignDocument(BaseModel):
    id: int
    title: str
    description: str
