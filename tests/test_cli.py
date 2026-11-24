"""Тесты CLI: успех, ошибки, формат ключ-значение."""

import io
import unittest
from contextlib import redirect_stdout, redirect_stderr
from tempfile import NamedTemporaryFile

from src.depviz.cli import EXIT_OK, EXIT_USAGE, main


def _run(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class CliSuccessTests(unittest.TestCase):
    """Успешный сценарий с URL."""

    def test_prints_all_keys(self) -> None:
        """Печатаются все 7 ключей."""
        code, out, _ = _run([
            "--package", "requests",
            "--repo", "https://example.com/repo",
            "--version", "2.31.0",
            "--max-depth", "3",
        ])
        self.assertEqual(code, EXIT_OK)
        for key in (
            "package", "repo", "test_mode", "version",
            "ascii_tree", "max_depth", "filter_substring",
        ):
            self.assertIn(f"{key}=", out)

    def test_test_mode_file(self) -> None:
        """test-mode с файлом проходит."""
        with NamedTemporaryFile() as tmp:
            code, out, _ = _run([
                "--package", "A",
                "--repo", tmp.name,
                "--test-mode",
                "--version", "1",
                "--max-depth", "1",
            ])
        self.assertEqual(code, EXIT_OK)
        self.assertIn("test_mode=True", out)


class CliErrorTests(unittest.TestCase):
    """Сценарии ошибок — код 2 и сообщение в stderr."""

    def test_missing_package(self) -> None:
        """Без --package — ошибка."""
        code, _, err = _run(["--repo", "https://x", "--version", "1",
                             "--max-depth", "1"])
        self.assertEqual(code, EXIT_USAGE)
        self.assertIn("package", err)

    def test_bad_depth(self) -> None:
        """Некорректная глубина — ошибка."""
        code, _, err = _run(["--package", "A", "--repo", "https://x",
                             "--version", "1", "--max-depth", "0"])
        self.assertEqual(code, EXIT_USAGE)
        self.assertIn("max-depth", err)


if __name__ == "__main__":
    unittest.main()
