"""Тесты валидаторов."""

import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.depviz.validation import (
    ValidationError,
    validate_depth,
    validate_filter,
    validate_package,
    validate_repo,
    validate_version,
)


class PackageValidationTests(unittest.TestCase):
    """Проверки validate_package."""

    def test_ok(self) -> None:
        """Корректное имя проходит."""
        self.assertEqual(validate_package("requests"), "requests")

    def test_none(self) -> None:
        """None отклоняется."""
        with self.assertRaises(ValidationError):
            validate_package(None)

    def test_spaces(self) -> None:
        """Пробелы отклоняются."""
        with self.assertRaises(ValidationError):
            validate_package("a b")


class RepoValidationTests(unittest.TestCase):
    """Проверки validate_repo."""

    def test_url_ok(self) -> None:
        """URL принимается."""
        self.assertEqual(validate_repo("https://x", False), "https://x")

    def test_url_bad(self) -> None:
        """Не-URL отклоняется в обычном режиме."""
        with self.assertRaises(ValidationError):
            validate_repo("not-a-url", False)

    def test_test_mode_file_ok(self) -> None:
        """Существующий файл принимается в test-mode."""
        with NamedTemporaryFile(suffix=".txt") as tmp:
            self.assertEqual(validate_repo(tmp.name, True), str(Path(tmp.name)))

    def test_test_mode_file_missing(self) -> None:
        """Отсутствующий файл отклоняется."""
        with self.assertRaises(ValidationError):
            validate_repo("/no/such/file", True)


class VersionValidationTests(unittest.TestCase):
    """Проверки validate_version."""

    def test_ok(self) -> None:
        """Обычная версия проходит."""
        self.assertEqual(validate_version("1.2.3"), "1.2.3")

    def test_empty(self) -> None:
        """Пустая версия отклоняется."""
        with self.assertRaises(ValidationError):
            validate_version("  ")


class DepthValidationTests(unittest.TestCase):
    """Проверки validate_depth."""

    def test_ok(self) -> None:
        """Границы диапазона проходят."""
        self.assertEqual(validate_depth(1), 1)
        self.assertEqual(validate_depth(100), 100)

    def test_zero(self) -> None:
        """0 отклоняется."""
        with self.assertRaises(ValidationError):
            validate_depth(0)

    def test_too_big(self) -> None:
        """> 100 отклоняется."""
        with self.assertRaises(ValidationError):
            validate_depth(101)


class FilterValidationTests(unittest.TestCase):
    """Проверки validate_filter."""

    def test_none(self) -> None:
        """None допустим."""
        self.assertIsNone(validate_filter(None))

    def test_empty(self) -> None:
        """Пустая строка отклоняется."""
        with self.assertRaises(ValidationError):
            validate_filter("   ")


if __name__ == "__main__":
    unittest.main()
