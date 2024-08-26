import os
import markdown_it
from app.services.gpt_service import GPTService

# Nuxt.js 3ファイルの生成を管理するクラス


class NuxtFileGenerator:
    def __init__(self, base_dir=".generated"):
        self.base_dir = base_dir
        self.gpt_service = GPTService()

    def create_file(self, path, content):
        full_path = os.path.join(self.base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as file:
            file.write(content)

    def generate_page(self, page_name, markdown_instruction):
        # GPTを使ってコードを生成
        code = self.gpt_service.generate_code_from_markdown(
            markdown_instruction)
        self.create_file(f"pages/{page_name}.vue", code)
        return code

    def generate_component(self, component_name, markdown_instruction):
        # GPTを使ってコードを生成
        code = self.gpt_service.generate_code_from_markdown(
            markdown_instruction)
        self.create_file(f"components/{component_name}.vue", code)
        return code

    def generate_from_markdown(self, markdown_text):
        # MarkdownをパースしてNuxt.js 3ファイルを生成
        md = markdown_it.MarkdownIt()
        parsed = md.parse(markdown_text)
        files_created = []
        current_instruction = ""

        for token in parsed:
            if token.type == "heading_open" and token.tag == "h2":
                if current_instruction:
                    page_name = current_instruction.strip().lower().replace(" ", "_")
                    content = self.generate_page(
                        page_name, current_instruction)
                    files_created.append((f"pages/{page_name}.vue", content))
                current_instruction = ""
            elif token.type == "heading_open" and token.tag == "h3":
                if current_instruction:
                    component_name = current_instruction.strip().lower().replace(" ", "_")
                    content = self.generate_component(
                        component_name, current_instruction)
                    files_created.append(
                        (f"components/{component_name}.vue", content))
                current_instruction = ""
            elif token.type == "inline":
                current_instruction += token.content + " "

        return files_created
