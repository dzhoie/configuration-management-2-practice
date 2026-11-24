"""Валидация параметров CLI. Каждая функция — одна проверка."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

# Пороговые значения (M1: без магических литералов в сравнениях)
MIN_DEPTH = 0
MAX_DEPTH_LIMIT = 100
MIN_PACKAGE_LEN = 1
MIN_FILTER_LEN = 1


class ValidationError(ValueError):
    """Ошибка валидации одного параметра."""


def validate_package(package: Optional[str]) -> str:
    """Проверить имя пакета: непустое, без пробелов.

    Args:
        package: имя пакета.

    Returns:
        Имя пакета.

    Raises:
        ValidationError: если имя пустое/содержит пробелы.
    """
    if package is None:
        raise ValidationError("--package обязателен")
    value = package.strip()
    if len(value) < MIN_PACKAGE_LEN:
        raise ValidationError("--package не может быть пустым")
    if any(ch.isspace() for ch in value):
        raise ValidationError("--package не должен содержать пробелы")
    return value


def validate_repo(repo: Optional[str], test_mode: bool) -> str:
    """Проверить URL репозитория или путь к файлу тестового репозитория.

    Args:
        repo: URL или путь.
        test_mode: если True — ожидается существующий файл.

    Returns:
        Проверенное значение.

    Raises:
        ValidationError: если значение не задано или файл не найден.
    """
    if repo is None:
        raise ValidationError("--repo обязателен")
    value = repo.strip()
    if not value:
        raise ValidationError("--repo не может быть пустым")
    if test_mode:
        path = Path(value)
        if not path.is_file():
            raise ValidationError(f"--repo: файл не найден: {value}")
        return str(path)
    lowered = value.lower()
    if not (lowered.startswith("http://")
            or lowered.startswith("https://")):
        raise ValidationError(
            "--repo: ожидается URL (http/https) или --test-mode с файлом"
        )
    return value


def validate_version(version: Optional[str]) -> str:
    """Проверить версию пакета: непустая, без пробелов.

    Args:
        version: строка версии.

    Returns:
        Строка версии.

    Raises:
        ValidationError: если версия пустая или содержит пробелы.
    """
    if version is None:
        raise ValidationError("--version обязателен")
    value = version.strip()
    if not value:
        raise ValidationError("--version не может быть пустым")
    if any(ch.isspace() for ch in value):
        raise ValidationError("--version не должен содержать пробелы")
    return value


def validate_depth(depth: Optional[int]) -> int:
    """Проверить максимальную глубину анализа.

    Args:
        depth: значение глубины.

    Returns:
        Глубина.

    Raises:
        ValidationError: если значение вне диапазона.
    """
    if depth is None:
        raise ValidationError("--max-depth обязателен")
    if not (MIN_DEPTH < depth <= MAX_DEPTH_LIMIT):
        raise ValidationError(
            f"--max-depth: ожидается 1..{MAX_DEPTH_LIMIT}, получено {depth}"
        )
    return depth


def validate_filter(filter_substring: Optional[str]) -> Optional[str]:
    """Проверить подстроку фильтрации пакетов (опциональный параметр).

    Args:
        filter_substring: подстрока или None.

    Returns:
        Подстрока либо None.

    Raises:
        ValidationError: если строка задана, но пуста.
    """
    if filter_substring is None:
        return None
    value = filter_substring.strip()
    if len(value) < MIN_FILTER_LEN:
        raise ValidationError("--filter не может быть пустым, если задан")
    return value
