import re

import rich
import strawberry

from rich_strawberry import SchemaWithRichLogger

from .traceback_parser import TraceBackParser

ANSI_ESCAPE_SEQ_PATTERN = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")


def remove_ansi_sequences(text: str) -> str:
    return ANSI_ESCAPE_SEQ_PATTERN.sub("", text)


@strawberry.type
class User:
    id: int
    name: str
    age: int


def get_user(id: int) -> User:
    if id != 1:
        raise ValueError("User not found")
    return User(id=1, name="Solpavchek", age=100)


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return get_user(id)


schema = SchemaWithRichLogger(query=Query)
# schema = strawberry.Schema(query=Query)


def test_query_without_errors():
    query = """
      query GetUser($id: Int!) {
        user(id: $id) {
          name
          age
        }
      }
    """
    result = schema.execute_sync(query=query, variable_values={"id": 1})
    assert result.data == {"user": {"name": "Solpavchek", "age": 100}}
    assert not result.errors


def test_error_in_the_query(capsys):
    query = """
      query GetUser($id: Int!) {
        user(id: $id) {
          name
          age
        }
      }
    """
    result = schema.execute_sync(query=query)

    assert not result.data == {"user": {"name": "Patrick", "age": 100}}
    assert result.errors
    assert len(result.errors) == 1

    graphql_err = result.errors[0]
    err_output = remove_ansi_sequences(capsys.readouterr().err)

    assert "GRAPHQL ERROR" in err_output
    assert graphql_err.message in err_output
    assert str(graphql_err) in err_output


def test_error_in_code(capsys):
    query = """
      query GetUser($id: Int!) {
        user(id: $id) {
          name
          age
        }
      }
    """
    result = schema.execute_sync(query=query, variable_values={"id": 2})

    assert not result.data == {"user": {"name": "Patrick", "age": 100}}
    assert result.errors
    assert len(result.errors) == 1

    graphql_err = result.errors[0]
    err_output = remove_ansi_sequences(capsys.readouterr().err)
    print(err_output)
    output_lines = [line.strip("│").strip() for line in err_output.splitlines()]

    with capsys.disabled():
      parser = TraceBackParser()
      parser.parse(output_lines)
      rich.print(parser.result)

    assert "GRAPHQL ERROR" in err_output
    assert graphql_err.message in err_output
    assert str(graphql_err) in err_output
