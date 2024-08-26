import os
from app.services.gpt_service import GPTService


class ProjectOverviewGenerator:
    def __init__(self, base_dir=".generated"):
        """
        ProjectOverviewGeneratorクラスの初期化メソッド。
        :param base_dir: Nuxtプロジェクトのルートディレクトリ。
        """
        self.base_dir = base_dir
        self.ignored_paths = self.load_nuxtignore()
        self.gpt_service = GPTService()  # GPTサービスを初期化

    def load_nuxtignore(self):
        """
        .nuxtignoreファイルを読み込み、無視するパスのリストを作成する。
        :return: 無視するパスのリスト。
        """
        nuxtignore_path = ".nuxtignore"
        ignored_paths = []

        if os.path.exists(nuxtignore_path):
            with open(nuxtignore_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # 絶対パスに変換して保存
                        ignored_paths.append(os.path.join(self.base_dir, line))
        else:
            # .nuxtignoreが存在しない場合のログ
            print(f"注意: {nuxtignore_path} が存在しません。無視リストは設定されていません。")

        return ignored_paths

    def is_ignored(self, path):
        """
        指定されたパスが無視リストに含まれているかを確認する。
        :param path: チェックするパス。
        :return: 無視リストに含まれている場合はTrue、含まれていない場合はFalse。
        """
        for ignored in self.ignored_paths:
            if path.startswith(ignored):
                return True
        return False

    def generate_overview(self):
        """
        プロジェクトのフォルダ構成を解析し、各フォルダやファイルの説明を記載した
        Markdownファイルを生成する。すでにファイルが存在する場合は、新たに作成しない。
        """
        overview_path = os.path.join(self.base_dir, "project_overview.md")

        # 既存のファイルがあるか確認
        if os.path.exists(overview_path):
            print(f"{overview_path} はすでに存在します。新しいファイルは作成されません。")
            return

        overview_lines = ["# Project Overview\n"]
        for root, dirs, files in os.walk(self.base_dir):
            # 無視するパスをスキップ
            if self.is_ignored(root):
                continue

            level = root.replace(self.base_dir, "").count(os.sep)
            indent = " " * 4 * level
            overview_lines.append(f"{indent}- **{os.path.basename(root)
                                                 }/**: Directory for storing related files and folders.")

            sub_indent = " " * 4 * (level + 1)
            for f in files:
                file_path = os.path.join(root, f)
                if self.is_ignored(file_path):
                    continue
                # GPTに説明を生成させる
                file_description = self.describe_file(file_path)
                overview_lines.append(
                    f"{sub_indent}- **{f}**: {file_description}")

        overview_content = "\n".join(overview_lines)
        with open(overview_path, "w") as file:
            file.write(overview_content)
        print(f"Project overview generated at {overview_path}")

    def describe_file(self, file_path):
        """
        GPTを使用してファイルの説明を生成する。
        :param file_path: ファイルのパス。
        :return: 生成されたファイルの説明。
        """
        prompt = f"Describe the purpose and contents of the following file in a Nuxt.js project: {
            file_path}"
        description = self.gpt_service.generate_description(prompt)
        return description.strip()
