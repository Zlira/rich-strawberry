from types import ModuleType
from typing import Final, Iterable, Mapping, Optional

import graphql
import strawberry
from graphql import GraphQLError
from rich import inspect
from rich.console import Console
from rich.traceback import Traceback
from strawberry.types import ExecutionContext


class RichGraphQLLogger:
    console: Final[Console] = Console(stderr=True)

    def __init__(
        self,
        log_context_keys: Iterable[str] = (),
        suppress_traceback_from: Iterable[ModuleType] = (),
    ):
        self.log_context_keys = log_context_keys or ("request",)
        self.suppress_traceback_from = suppress_traceback_from or (strawberry, graphql)

    # TODO context doesn't need to be a mapping
    def _log_context(self, context: Mapping | None) -> None:
        if not self.log_context_keys or not context:
            return
        # TODO don't print if no keys found?
        self.console.rule("CONTEXT")
        for key in self.log_context_keys:
            if context_val := context.get(key):
                inspect(context_val, console=self.console)
            # TODO what to do if key is absent?

    def print_error(self, error: GraphQLError) -> None:
        self.console.rule("GRAPHQL ERROR")
        self.console.print(error)
        if error.original_error:
            rich_traceback = Traceback.from_exception(
                error.original_error.__class__,
                error.original_error,
                traceback=error.original_error.__traceback__,
                suppress=self.suppress_traceback_from,
            )
            self.console.print(rich_traceback)

    def print_errors(
        self,
        errors=list[GraphQLError],
        execution_context: Optional[ExecutionContext] = None,
    ):
        if execution_context:
            self._log_context(execution_context.context)
        for error in errors:
            self.print_error(error)
