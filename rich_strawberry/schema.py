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
        query: Type,
        mutation: Optional[Type] = None,
        subscription: Optional[Type] = None,
        directives: Iterable[StrawberryDirective] = (),
        types=(),
        extensions: Iterable[Union[Type[Extension], Extension]] = (),
        execution_context_class: Optional[Type[GraphQLExecutionContext]] = None,
        config: Optional[StrawberryConfig] = None,
        scalar_overrides: Optional[
            Dict[object, Union[ScalarWrapper, ScalarDefinition]]
        ] = None,
        schema_directives: Iterable[object] = (),
        debug_logger: Optional[RichGraphQLLogger] = None,
    ):
        super().__init__(
            query,
            mutation,
            subscription,
            directives,
            types,
            extensions,
            execution_context_class,
            config,
            scalar_overrides,
            schema_directives,
        )
        self.debug_logger = debug_logger or RichGraphQLLogger()

    def process_errors(
        self,
        errors: List[GraphQLError],
        execution_context: Optional[ExecutionContext] = None,
    ) -> None:
        self.debug_logger.print_errors(errors, execution_context)
