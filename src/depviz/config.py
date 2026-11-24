"""Конфигурация CLI-приложения: параметры этапа 1."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, Optional


@dataclass
class Config:
    """Настраиваемые пользователем параметры (вариант №6, этап 1).

    Attributes:
        package: имя анализируемого пакета.
        repo: URL репозитория или путь к файлу тестового репозитория.
        test_mode: режим работы с тестовым репозиторием.
        version: версия пакета.
        ascii_tree: режим вывода зависимостей в виде ASCII-дерева.
        max_depth: максимальная глубина анализа зависимостей.
        filter_substring: подстрока для фильтрации пакетов.
    """

    package: Optional[str] = None
    repo: Optional[str] = None
    test_mode: bool = False
    version: Optional[str] = None
    ascii_tree: bool = False
    max_depth: Optional[int] = None
    filter_substring: Optional[str] = None

    def as_key_value(self) -> Dict[str, object]:
        """Вернуть параметры в формате ключ-значение для печати.

        Returns:
            Словарь, где ключи — имена параметров, значения — их значения.
        """
        raw = asdict(self)
        return {key: value for key, value in raw.items()}
