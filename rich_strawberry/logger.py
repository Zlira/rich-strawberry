from operator import getitem
from types import ModuleType
from typing import Any, Final, Iterable, Optional

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
        suppress_traceback_from: Iterable[ModuleType] | None = None,
    ):
        """
        log_context_keys: which keys form the context to log,
          the logger assumes the context is a mapping,
          the default value is empty
        suppress_traceback_from: a list of modules, in a traceback the frames
          from these modules will be suppressed, i.e. shown as a file line only
          the default value is (strawberry, graphql)
        """
        self.log_context_keys = log_context_keys
        self.suppress_traceback_from = (
            suppress_traceback_from
            if suppress_traceback_from is not None
            else (strawberry, graphql)
        )

    def _get_context_key(self, context: Any, key: str) -> Any:
        val = strawberry.UNSET
        try:
            try:
                val = getitem(context, key)
            except TypeError:
                val = getattr(context, key, strawberry.UNSET)
        except (KeyError, AttributeError):
            pass
        return val

    def _log_context(self, context: Any) -> None:
        if not self.log_context_keys or not context:
            return
        self.console.rule("CONTEXT")
        for key in self.log_context_keys:
            self.console.print(key, justify="center", style="reverse")
            val = self._get_context_key(context, key)
            if val is not strawberry.UNSET:
                inspect(context[key], console=self.console)
            else:
                self.console.print(
                    f"[italic]Warning:[/italic] missing context key '{key}'"
                )

    def _print_error(self, error: GraphQLError) -> None:
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
            self._print_error(error)
