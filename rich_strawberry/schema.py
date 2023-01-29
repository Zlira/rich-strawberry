from typing import Optional

import strawberry
from graphql import GraphQLError
from strawberry.types import ExecutionContext

from .logger import RichGraphQLLogger


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
