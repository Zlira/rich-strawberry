import asyncio
from typing import AsyncGenerator, Optional

import strawberry
from graphql import GraphQLError
from starlette.applications import Starlette
from strawberry.asgi import GraphQL
from strawberry.types import ExecutionContext

from rich_strawberry.logger import RichGraphQLLogger


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "world"


class SchemaWithRichLogger(strawberry.Schema):
    def __init__(
        self,
        debug_logger: Optional[RichGraphQLLogger] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.debug_logger = debug_logger or RichGraphQLLogger()

    def process_errors(
        self,
        errors: list[GraphQLError],
        execution_context: Optional[ExecutionContext] = None,
    ) -> None:
        self.debug_logger.print_errors(errors, execution_context)


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        print("we are here")
        for i in range(target):
            yield i
            if i == 3:
                raise ValueError
            await asyncio.sleep(1)


schema = SchemaWithRichLogger(
    query=Query,
    subscription=Subscription,
    debug_logger=RichGraphQLLogger(
        log_context_keys=[
            "request",
        ]
    ),
)
graphql_app = GraphQL(schema)

app = Starlette()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
