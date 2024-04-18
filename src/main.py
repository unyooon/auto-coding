from core.project_generator import get_project_name, generate_go_project_structure
from core.project_generator import generate_go_main_file, generate_go_mod_file
# from core.project_generator import generate_go_gitignore_file, generate_go_readme_file

def main():
    # プロジェクト名を取得
    project_name = get_project_name()

    # プロジェクトの基本構造を生成
    generate_go_project_structure(project_name)

    # 必要なファイルを生成
    generate_go_main_file(project_name)
    generate_go_mod_file(project_name)
    # generate_go_gitignore_file()
    # generate_go_readme_file(project_name, "プロジェクトの説明")

    print(f"{project_name} プロジェクトが生成されました。")


if __name__ == "__main__":
    main()