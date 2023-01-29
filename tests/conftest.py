import re

import pytest

from rich_strawberry import SchemaWithRichLogger
from rich_strawberry.logger import RichGraphQLLogger

from .query import Query

ANSI_ESCAPE_SEQ_PATTERN = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")


def remove_ansi_sequences(text: str) -> str:
    return ANSI_ESCAPE_SEQ_PATTERN.sub("", text)


@pytest.fixture
def query():
    return Query


@pytest.fixture
def default_schema(query):
    return SchemaWithRichLogger(query=query)


@pytest.fixture
def get_schema_with_logger_params(query):
    def _get_schema_with_logger_params(*args, **kwargs):
        return SchemaWithRichLogger(
            query=query,
            debug_logger=RichGraphQLLogger(*args, **kwargs),
        )

    return _get_schema_with_logger_params


@pytest.fixture
def get_stripped_stderr(capsys):
    def _get_stripped_stderr():
        return remove_ansi_sequences(capsys.readouterr().err)

    return _get_stripped_stderr
