# ベースイメージを指定
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY ./app .
COPY ./requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ポートを公開
EXPOSE 8000

# アプリケーションを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]