import strawberry

from rich_strawberry.schema import SchemaWithRichLogger
from rich_strawberry.logger import RichGraphQLLogger


@strawberry.type
class User:
    id: int
    name: str
    age: int


def get_user(id: int) -> User:
    if id not in (1, 2):
        raise ValueError("User not found")
    if id == 2:
        raise ValueError("This is a secret user!")
    return User(id=1, name="Solpavchek", age=100)


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User | None:
        return get_user(id)


schema = SchemaWithRichLogger(
    query=Query,
    debug_logger=RichGraphQLLogger(log_context_keys=("solpavchek", "request")),
)
