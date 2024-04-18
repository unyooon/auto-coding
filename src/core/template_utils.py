import os

def read_go_template(template_path):
    """
    指定されたパスからGoテンプレートファイルを読み込む
    """
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()
        return template
    except OSError as e:
        print(f"テンプレートファイルの読み込みに失敗しました: {e}")
        return None

def render_go_template(template, context):
    """
    Goテンプレートをレンダリングする
    """
    try:
        rendered_content = template.format(**context)
        return rendered_content
    except KeyError as e:
        print(f"テンプレートのレンダリングに失敗しました: {e}")
        return None