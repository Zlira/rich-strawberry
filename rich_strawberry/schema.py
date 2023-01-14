from typing import Dict, Iterable, List, Optional, Type, Union

import strawberry
from graphql import ExecutionContext as GraphQLExecutionContext
from graphql import GraphQLError
from strawberry.custom_scalar import ScalarDefinition, ScalarWrapper
from strawberry.directive import StrawberryDirective
from strawberry.extensions import Extension
from strawberry.schema.config import StrawberryConfig
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
        errors: List[GraphQLError],
        execution_context: Optional[ExecutionContext] = None,
    ) -> None:
        self.debug_logger.print_errors(errors, execution_context)
