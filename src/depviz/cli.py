"""CLI этапа 1: разбор аргументов, валидация, вывод ключ-значение."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .config import Config
from .validation import (
    ValidationError,
    validate_depth,
    validate_filter,
    validate_package,
    validate_repo,
    validate_version,
)

EXIT_OK = 0
EXIT_USAGE = 2


def build_parser() -> argparse.ArgumentParser:
    """Собрать парсер аргументов командной строки.

    Returns:
        Настроенный ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        prog="depviz",
        description="Визуализация графа зависимостей (этап 1).",
    )
    parser.add_argument("--package", required=False,
                        help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=False,
                        help="URL репозитория или путь к файлу")
    parser.add_argument("--test-mode", action="store_true",
                        help="Режим работы с тестовым репозиторием")
    parser.add_argument("--version", required=False,
                        help="Версия пакета")
    parser.add_argument("--ascii-tree", action="store_true",
                        help="Вывод зависимостей ASCII-деревом")
    parser.add_argument("--max-depth", type=int, required=False,
                        help="Максимальная глубина анализа")
    parser.add_argument("--filter", dest="filter_substring",
                        required=False,
                        help="Подстрока для фильтрации пакетов")
    return parser


def parse_args(argv: Sequence[str]) -> Config:
    """Разобрать argv и получить валидированную конфигурацию.

    Args:
        argv: аргументы командной строки без имени программы.

    Returns:
        Config с валидированными значениями.

    Raises:
        ValidationError: если хотя бы один параметр некорректен.
    """
    parser = build_parser()
    ns = parser.parse_args(argv)
    config = Config(
        package=validate_package(ns.package),
        repo=validate_repo(ns.repo, ns.test_mode),
        test_mode=bool(ns.test_mode),
        version=validate_version(ns.version),
        ascii_tree=bool(ns.ascii_tree),
        max_depth=validate_depth(ns.max_depth),
        filter_substring=validate_filter(ns.filter_substring),
    )
    return config


def print_key_value(config: Config) -> None:
    """Напечатать параметры в формате ключ-значение.

    Args:
        config: валидированная конфигурация.
    """
    for key, value in config.as_key_value().items():
        print(f"{key}={value}")


def main(argv: Sequence[str] | None = None) -> int:
    """Точка входа CLI.

    Args:
        argv: аргументы без имени программы; по умолчанию sys.argv[1:].

    Returns:
        Код возврата процесса.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        config = parse_args(args)
    except ValidationError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return EXIT_USAGE
    print_key_value(config)
    return EXIT_OK
