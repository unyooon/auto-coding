import os

def create_directory(path):
    """
    指定されたパスにディレクトリを作成する
    """
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print(f"ディレクトリの作成に失敗しました: {e}")

def create_file(path, content):
    """
    指定されたパスにファイルを作成し、コンテンツを書き込む
    """
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
    except OSError as e:
        print(f"ファイルの作成に失敗しました: {e}")