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

    def generate_file(self, file_path, description, markdown):
        """
        GPTを使用してNuxt 3のファイルコードを生成し、ファイルに保存する。
        :param file_path: 生成するファイルのパス。
        :param description: ファイルの説明文。
        :return: 生成されたコード。
        """
        # GPTを使ってコードを生成
        prompt = f"Create the Nuxt 3 file at {
            file_path} with the following description:\n{description}\nmarkdown:{markdown}"
        code = self.gpt_service.generate_code_from_markdown(prompt)
        self.create_file(file_path, code)
        return code
