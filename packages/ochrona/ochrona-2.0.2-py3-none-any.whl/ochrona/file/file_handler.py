# -*- coding: utf-8 -*-
"""
Ochrona-cli
:author: ascott
"""

import io
import os

from typing import Any, Dict, IO, Optional, List, Type, TextIO, Union

from ochrona.config import OchronaConfig
from ochrona.const import (
    CONDA_ENVIRONMENT,
    CONSTRAINTS_TXT,
    PIPFILE_LOCK,
    POETRY_LOCK,
    REQUIREMENTS_TXT,
    SETUP_PY,
    SUPPORTED_DEPENDENCY_FILE_PATTERNS,
    TOX_INI,
)
from ochrona.exceptions import OchronaFileException
from ochrona.log import OchronaLogger
from ochrona.parser import Parsers

Path: Optional[Type] = None
try:
    from pathlib import Path
except ImportError:
    pass


def rfind_all_dependencies_files(
    logger: OchronaLogger,
    directory: Optional[str] = None,
    excluded_directories: Optional[Union[List[str], str]] = None,
    file_obj: Optional[Union[IO, str]] = None,
) -> List[str]:
    """
    Recursively searches for dependency files to analyze

    :param logger: A configured `OchronaFormatter` instance
    :param directory: str - starting directory (optional)
    :param excluded_directories: list - directories to exclude
    :param file_obj: A specified file to use
    :return: list - list of paths for files to analyze
    """
    if not directory:
        directory = os.getcwd()

    files = []

    # if this is somehow still a string, let's fix that
    if excluded_directories:
        directories_to_exclude = (
            excluded_directories.split(",")
            if isinstance(excluded_directories, str)
            else excluded_directories
        )
    else:
        directories_to_exclude = []

    if file_obj:
        if isinstance(file_obj, str):
            files.append(file_obj)
        elif isinstance(file_obj, io.TextIOWrapper):
            files.append(file_obj.name)
        else:
            raise OchronaFileException(
                f"Unknown type for file path {type(file_obj)} - {file_obj}"
            )
    else:
        if Path:
            for filename in Path(directory).glob(
                SUPPORTED_DEPENDENCY_FILE_PATTERNS[REQUIREMENTS_TXT]
            ):
                if not any([excl in str(filename) for excl in directories_to_exclude]):
                    logger.debug(
                        f"Found matching requirements*.txt file at [bold]{filename}[/bold]"
                    )
                    files.append(filename)
            for filename in Path(directory).glob(
                SUPPORTED_DEPENDENCY_FILE_PATTERNS[PIPFILE_LOCK]
            ):
                if not any([excl in str(filename) for excl in directories_to_exclude]):
                    logger.debug(
                        f"Found matching pipfile.lock file at [bold]{filename}[/bold]"
                    )
                    files.append(filename)
            for filename in Path(directory).glob(
                SUPPORTED_DEPENDENCY_FILE_PATTERNS[POETRY_LOCK]
            ):
                if not any([excl in str(filename) for excl in directories_to_exclude]):
                    logger.debug(
                        f"Found matching poetry.lock file at [bold]{filename}[/bold]"
                    )
                    files.append(filename)
            for filename in Path(directory).glob(
                SUPPORTED_DEPENDENCY_FILE_PATTERNS[SETUP_PY]
            ):
                if not any([excl in str(filename) for excl in directories_to_exclude]):
                    logger.debug(
                        f"Found matching setup.py file at [bold]{filename}[/bold]"
                    )
                    files.append(filename)
            for filename in Path(directory).glob(
                SUPPORTED_DEPENDENCY_FILE_PATTERNS[CONDA_ENVIRONMENT]
            ):
                if not any([excl in str(filename) for excl in directories_to_exclude]):
                    logger.debug(
                        f"Found matching conda environment.yml file at [bold]{filename}[/bold]"
                    )
                    files.append(filename)
            for filename in Path(directory).glob(
                SUPPORTED_DEPENDENCY_FILE_PATTERNS[TOX_INI]
            ):
                if not any([excl in str(filename) for excl in directories_to_exclude]):
                    logger.debug(
                        f"Found matching conda tox.ini file at [bold]{filename}[/bold]"
                    )
                    files.append(filename)
            for filename in Path(directory).glob(
                SUPPORTED_DEPENDENCY_FILE_PATTERNS[CONSTRAINTS_TXT]
            ):
                if not any([excl in str(filename) for excl in directories_to_exclude]):
                    logger.debug(
                        f"Found matching conda constraints.txt file at [bold]{filename}[/bold]"
                    )
                    files.append(filename)

    if not files:
        raise OchronaFileException("No dependency files found")

    return files


def parse_to_payload(
    logger: OchronaLogger, file_path: str, config: OchronaConfig
) -> Dict[str, Any]:
    """
    Parses a requirements.txt type file or Pipefile.lock into a JSON payload.
    :param logger: A configured `OchronaLogger` instance
    :param file_path: path to file
    :param config: An instance of `OchronaConfig`
    :return: JSON payload
    """
    dependencies = []
    parsers = Parsers()
    if os.path.basename(file_path).lower() == PIPFILE_LOCK.lower():
        dependencies = parsers.pipfile.parse(
            file_path=file_path, include_dev=config.include_dev
        )
    elif os.path.basename(file_path).lower() == POETRY_LOCK.lower():
        dependencies = parsers.poetry.parse(
            file_path=file_path, include_dev=config.include_dev
        )
    elif os.path.basename(file_path).lower() == SETUP_PY.lower():
        dependencies = parsers.setup.parse(
            file_path=file_path, include_dev=config.include_dev
        )
    elif os.path.basename(file_path).lower() == CONDA_ENVIRONMENT.lower():
        dependencies = parsers.conda.parse(file_path=file_path)
    elif os.path.basename(file_path).lower() == TOX_INI.lower():
        dependencies = parsers.tox.parse(file_path=file_path)
    elif os.path.basename(file_path).lower() == CONSTRAINTS_TXT.lower():
        dependencies = parsers.constraints.parse(file_path=file_path)
    else:
        dependencies = parsers.requirements.parse(file_path=file_path)

    logger.debug(
        f"Discovered dependencies: {os.linesep}{os.linesep.join([(' --- [bold]' + d.get('version') +'[/bold]') for d in dependencies])}"
    )
    return {"dependencies": dependencies, "logger": logger, "config": config}


def parse_direct_to_payload(
    logger: OchronaLogger, direct: str, config: OchronaConfig
) -> Dict[str, Any]:
    """
    Parses direct input string as PEP-508 compliant file and outputs a JSON payload.
    :param logger: A configured `OchronaLogger` instance
    :param direct: input string
    :param config: An instance of `OchronaConfig`
    :return: JSON payload
    """
    dependencies = []
    parsers = Parsers()
    dependencies = parsers.requirements.direct_parse(direct=direct)
    logger.debug(
        f"Discovered dependencies: {os.linesep}{os.linesep.join([(' --- [bold]' + d.get('version') +'[/bold]') for d in dependencies])}"
    )
    return {"dependencies": dependencies, "logger": logger, "config": config}
