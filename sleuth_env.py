import os
import sys
import nbformat
import pkgutil

def extract_dependencies_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as nb_file:
        notebook_content = nb_file.read()

    notebook = nbformat.reads(notebook_content, as_version=nbformat.NO_CONVERT)
    dependencies = set()

    for cell in notebook.cells:
        if cell.cell_type == 'code':
            code = cell.source
            if 'import' in code or 'from ' in code:
                lines = [line.split() for line in code.split('\n') if line.startswith(('import ', 'from '))]
                for line in lines:
                    if len(line) >= 2:
                        package = line[1].split('.')[0]
                        dependencies.add(package)

    return dependencies

def get_base_python_modules():
    return set(module[1] for module in pkgutil.iter_modules())

def main(repo_directory):
    notebook_files = [file for file in os.listdir(repo_directory) if file.endswith('.ipynb')]
    all_dependencies = set()

    for notebook_file in notebook_files:
        notebook_path = os.path.join(repo_directory, notebook_file)
        dependencies = extract_dependencies_from_notebook(notebook_path)
        all_dependencies |= dependencies

    base_python_modules = get_base_python_modules()
    additional_dependencies = all_dependencies - base_python_modules

    with open("environment.yml", 'w', encoding='utf-8') as env_file:
        env_file.write("name: myenv\n")
        env_file.write("dependencies:\n")
        for package in sorted(additional_dependencies):
            env_file.write(f"  - {package}\n")

    print("environment.yml file generated.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py repo_directory")
        sys.exit(1)

    repo_directory = sys.argv[1]
    main(repo_directory)