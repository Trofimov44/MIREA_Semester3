import argparse
import subprocess
import os

def get_commits_with_file(repo_path, filename):
    """
    Получаем список коммитов, где изменялся указанный файл.
    """
    command = ["git", "-C", repo_path, "log", "--pretty=format:%H", "--", filename]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


def get_commit_files(repo_path, commit_hash):
    """
    Получаем файлы и папки, измененные в данном коммите.
    """
    command = ["git", "-C", repo_path, "show", "--name-only", "--pretty=format:", commit_hash]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


def build_dependency_graph(repo_path, filename):
    """
    Строим граф зависимостей в формате Graphviz.
    """
    commits = get_commits_with_file(repo_path, filename)
    graph = "digraph dependencies {\n"
    graph += "    node [shape=box];\n"

    for i, commit in enumerate(commits):
        files = get_commit_files(repo_path, commit)
        # Создаем строку для метки, добавляя переносы строк
        label = f"{commit}:\n" + "\n".join(files)  # Используем полный commit, а не обрезанный
        graph += f'    "{commit}" [label="{label}"];\n'

        # Добавляем ребра для транзитивных зависимостей (связь между коммитами)
        if i > 0:
            graph += f'    "{commits[i - 1]}" -> "{commit}";\n'

    graph += "}\n"
    return graph




def main():
    parser = argparse.ArgumentParser(description="Визуализация графа зависимостей коммитов.")
    parser.add_argument("--graphviz-path", required=True, help="Путь к программе Graphviz (например, dot).")
    parser.add_argument("--repo-path", required=True, help="Путь к Git-репозиторию.")
    parser.add_argument("--output-path", required=True, help="Путь к файлу для записи кода.")
    parser.add_argument("--filename", required=True, help="Имя файла для анализа зависимостей.")

    args = parser.parse_args()

    # Строим граф
    graph_code = build_dependency_graph(args.repo_path, args.filename)

    # Сохраняем результат в файл
    with open(args.output_path, "w") as file:
        file.write(graph_code)

    # Выводим граф на экран
    print(graph_code)


if __name__ == "__main__":
    main()
