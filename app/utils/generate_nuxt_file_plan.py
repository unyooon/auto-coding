import markdown_it
import json
from app.services.gpt_service import GPTService


class NuxtFilePlanGenerator:
    def __init__(self):
        self.gpt_service = GPTService()

    def generate_plan_from_markdown(self, markdown_text):
        """
        Markdownテキストを解析して、生成するファイルとその説明のリストを生成する。
        :param markdown_text: Markdown形式の設計書。
        :return: ファイルパスと説明文のリスト。
        """
        # GPTを使ってファイルと説明文のリストを生成
        prompt = f"The following Markdown description generates a list of Nuxt 3 files and components that need to be created in typescript, in JSON format, including the file path and a brief description of each.\n\n## Json format\n `[{file_path: str, description: str}]`\n\n## Markdown\n{
            markdown_text}"
        plan = self.gpt_service.generate_json(prompt)

        try:
            # JSON形式でパースしてリストを取得
            return json.loads(plan)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {str(e)}")
