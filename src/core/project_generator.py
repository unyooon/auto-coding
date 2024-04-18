import argparse

from .file_utils import create_file, create_directory
from .template_utils import read_go_template, render_go_template

def get_project_name():
    """
    ユーザーからプロジェクト名を取得する
    """
    parser = argparse.ArgumentParser(description='Go言語プロジェクトを生成します')
    parser.add_argument('project_name', help='プロジェクト名を入力してください')
    args = parser.parse_args()
    return args.project_name

def generate_go_project_structure(project_name):
    """
    Go言語プロジェクトの基本的な構造を生成する
    """
    project_dir = project_name
    create_directory(project_dir)
    create_directory(f"{project_dir}/cmd")
    create_directory(f"{project_dir}/internal")
    create_directory(f"{project_dir}/internal/entity")
    create_directory(f"{project_dir}/internal/usecase")
    create_directory(f"{project_dir}/internal/repository")
    create_directory(f"{project_dir}/internal/handler")


def generate_file(project_name, template_name, output_path, context=None):
    """
    テンプレートからファイルを生成する
    """
    template_path = f"templates/go/{template_name}.template"
    template = read_go_template(template_path)
    if template:
        if context:
            rendered_content = render_go_template(template, context)
        else:
            rendered_content = template
        if rendered_content:
            create_file(output_path, rendered_content)

##################
#
# ファイル生成関数
#
##################

def generate_go_main_file(project_name):
    output_path = f"{project_name}/cmd/main.go"
    generate_file(project_name, "main.go", output_path)

def generate_go_mod_file(project_name):
    output_path = f"{project_name}/go.mod"
    context = {"project_name": project_name}
    generate_file(project_name, "go.mod", output_path, context)

# 他の生成関数も同様に実装