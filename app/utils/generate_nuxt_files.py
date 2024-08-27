import json
import os
import subprocess
from app.services.gpt_service import GPTService
from app.utils.generate_project_overview import ProjectOverviewGenerator


class NuxtFileGenerator:
    def __init__(self, base_dir=".generated"):
        """
        NuxtFileGeneratorクラスの初期化メソッド。
        :param base_dir: 生成されたファイルを保存するベースディレクトリ。
        """
        self.base_dir = base_dir
        self.gpt_service = GPTService()

    def ensure_directories(self):
        """
        .generatedディレクトリとNuxt 3プロジェクトが存在しない場合、それらを作成し、
        必要なレイアウトファイルの設定と不要なapp.vueの削除を行う。
        """
        # .generatedフォルダが存在しない場合、作成する
        if not os.path.exists(self.base_dir):
            print(f"{self.base_dir} フォルダが存在しないため、新しく作成します。")
            os.makedirs(self.base_dir, exist_ok=True)

        # Nuxt 3プロジェクトが存在しない場合、作成する
        if not os.listdir(self.base_dir):  # フォルダが空の場合にのみプロジェクトを作成
            print(f"Nuxt 3プロジェクトが見つかりません。{self.base_dir} に新しいプロジェクトを作成します。")
            subprocess.run(["npx", "nuxi", "init", self.base_dir], check=True)
            print("Nuxt 3プロジェクトが作成されました。")

            # app.vueの削除
            app_vue_path = os.path.join(self.base_dir, "app.vue")
            if os.path.exists(app_vue_path):
                os.remove(app_vue_path)
                print("app.vueが削除されました。")

            # layoutsフォルダの作成とdefault.vueの作成
            layouts_dir = os.path.join(self.base_dir, "layouts")
            os.makedirs(layouts_dir, exist_ok=True)
            default_vue_content = """
<template>
  <div>
    <NuxtPage />
  </div>
</template>
"""
            with open(os.path.join(layouts_dir, "default.vue"), "w") as file:
                file.write(default_vue_content)
                print("layouts/default.vue が作成されました。")

        # プロジェクト概要の生成
        overview_generator = ProjectOverviewGenerator(self.base_dir)
        overview_generator.generate_overview()

    def create_file(self, path, content):
        """
        指定されたパスにファイルを作成し、指定された内容を書き込む。
        :param path: ファイルのパス。
        :param content: ファイルに書き込む内容。
        """
        full_path = os.path.join(self.base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as file:
            file.write(content)

    def generate_file(self, file_path, description, markdown, other_files):
        """
        GPTを使用してNuxt 3のファイルコードを生成し、ファイルに保存する。
        :param file_path: 生成するファイルのパス。
        :param description: ファイルの説明文。
        :param markdown: 設計書
        :param other_files: 他のファイル
        :return: 生成されたコード。
        """
        print(f"{file_path} を生成中...")
        # GPTを使ってコードを生成
        prompt = f"Create the Nuxt 3 file with typescript at {
            file_path} with the following description:\n{description}\nmarkdown:{markdown}\nReference other files to be generated:{other_files}"
        code = self.gpt_service.generate_code_from_markdown(prompt)
        self.create_file(file_path, code)
        return code

    def update_overview_with_gpt(self, files_info: list[dict]):
        """
        既存のproject_overview.mdと新しいファイル情報を基に、生成AIにプロジェクト概要を再生成させる。
        :param files_info: ファイル情報のリスト。各ファイル情報は辞書形式で、`file_path`, `generated_code`, `description`を含む。
        """
        overview_path = os.path.join(self.base_dir, "project_overview.md")

        # 既存のproject_overview.mdを読み込む
        if os.path.exists(overview_path):
            with open(overview_path, "r") as overview_file:
                existing_content = overview_file.read()
        else:
            existing_content = "# Project Overview\n\n"

        # 生成AIへのプロンプトを作成
        prompt = (
            f"Here is the current project overview:\n\n"
            f"{existing_content}\n\n"
            f"Here are the new files that were added:\n\n"
            f"{files_info}\n\n"
            f"Please update the project overview to include the new files."
        )

        # 生成AIにプロンプトを渡して、プロジェクト概要を再生成
        updated_overview = self.gpt_service.generate_description(prompt)

        # 新しいプロジェクト概要をファイルに書き込む
        with open(overview_path, "w") as overview_file:
            overview_file.write(updated_overview)
        print(f"Project overview updated at {overview_path}")


class NuxtFileUpdater:
    def __init__(self, base_dir=".generated"):
        self.base_dir = base_dir
        self.gpt_service = GPTService()

    def identify_fixes(self, change_description: str) -> list[dict]:
        """
        生成AIにプロジェクトの修正箇所を特定させ、修正するファイルとその箇所の説明文を返す。
        :param change_description: 修正内容の説明。
        :return: 修正するファイルとその修正箇所の説明文のリスト。
        """
        overview_path = os.path.join(self.base_dir, "project_overview.md")
        if not os.path.exists(overview_path):
            raise FileNotFoundError(f"{overview_path} does not exist.")

        with open(overview_path, "r") as file:
            overview_content = file.read()

        # 生成AIに修正箇所を特定させるためのプロンプトを作成
        prompt = (
            f"Please identify the files and the specific sections that need to be modified. "
            f"Return the results in a list of dictionaries with the format: "
            f"[{{'file_path': str, 'fix_description': str}}]."
            f"\n"
            f"\n"
            f"Here is the current project overview:\n\n"
            f"{overview_content}\n\n"
            f"The following change is required:\n{change_description}\n\n"
        )

        # 生成AIにプロンプトを渡して、修正箇所を特定
        analysis_result = self.gpt_service.generate_json(prompt)

        # 修正箇所を解析してリスト形式で返す
        try:
            # JSON形式でパースしてリストを取得
            return json.loads(analysis_result)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {str(e)}")

    def apply_fixes(self, fixes: list[dict]):
        """
        修正リストに基づいてファイルを1つずつ修正する。
        :param fixes: 修正するファイルと修正内容のリスト。
        """
        results = []
        for fix in fixes:
            file_path = fix['file_path']
            fix_description = fix['fix_description']

            if not os.path.exists(file_path):
                print(f"File {file_path} does not exist, skipping...")
                continue

            with open(file_path, "r") as file:
                current_content = file.read()

            # 生成AIに修正内容を渡して新しいコードを生成
            prompt = (
                f"The following file content needs to be updated\n\n"
                f"According to this description:\n{fix_description}\n\n"
                f"Please provide the updated code."
                f"\n\n### Current content:\n"
                f"{current_content}\n\n"
            )
            new_code = self.gpt_service.generate_code(prompt)

            # ファイルを更新
            with open(file_path, "w") as file:
                file.write(new_code)

            print(f"File {file_path} has been updated.")

            results.append({
                "file_path": file_path,
                "fix_description": fix_description,
                "new_code": new_code,
                "old_code": current_content,
            })

        return results
