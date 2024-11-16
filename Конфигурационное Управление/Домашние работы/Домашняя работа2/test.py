import unittest
from unittest.mock import patch, MagicMock
from main import get_commits_with_file, get_commit_files, build_dependency_graph  # Замените на правильный путь


class TestGitFunctions(unittest.TestCase):

    # Тест для get_commits_with_file
    @patch('main.subprocess.run')  # Замените на правильный путь
    def test_get_commits_with_file(self, mock_run):
        # Имитируем вывод команды git log
        mock_run.return_value = MagicMock(stdout="commit_hash_1\ncommit_hash_2")

        repo_path = "/path/to/repo"
        filename = "file.txt"

        result = get_commits_with_file(repo_path, filename)

        mock_run.assert_called_once_with(
            ["git", "-C", repo_path, "log", "--pretty=format:%H", "--", filename],
            capture_output=True, text=True, check=True
        )

        self.assertEqual(result, ["commit_hash_1", "commit_hash_2"])

    # Тест для get_commit_files
    @patch('main.subprocess.run')  # Замените на правильный путь
    def test_get_commit_files(self, mock_run):
        # Имитируем вывод команды git show
        mock_run.return_value = MagicMock(stdout="file1.txt\nfile2.txt")

        repo_path = "/path/to/repo"
        commit_hash = "commit_hash_1"

        result = get_commit_files(repo_path, commit_hash)

        mock_run.assert_called_once_with(
            ["git", "-C", repo_path, "show", "--name-only", "--pretty=format:", commit_hash],
            capture_output=True, text=True, check=True
        )

        self.assertEqual(result, ["file1.txt", "file2.txt"])

    # Тест для build_dependency_graph
    @patch('main.get_commits_with_file')  # Замените на правильный путь
    @patch('main.get_commit_files')  # Замените на правильный путь
    def test_build_dependency_graph(self, mock_get_files, mock_get_commits):
        # Имитируем поведение функций
        commits = ["commit_hash_1", "commit_hash_2"]
        files_commit_1 = ["file1.txt", "file2.txt"]
        files_commit_2 = ["file2.txt", "file3.txt"]

        mock_get_commits.return_value = commits
        mock_get_files.side_effect = [files_commit_1, files_commit_2]

        repo_path = "/path/to/repo"
        filename = "file.txt"

        graph_code = build_dependency_graph(repo_path, filename)

        expected_graph = """digraph dependencies {
    node [shape=box];
    "commit_hash_1" [label="commit_hash_1:\nfile1.txt\nfile2.txt"];
    "commit_hash_2" [label="commit_hash_2:\nfile2.txt\nfile3.txt"];
    "commit_hash_1" -> "commit_hash_2";
}
"""
        self.assertEqual(graph_code, expected_graph)


if __name__ == '__main__':
    unittest.main()
