import logging
import strawberry
from strawberry.extensions import Extension

from rich_strawberry import RichGraphQLLogger, SchemaWithRichLogger

logger = logging.getLogger("strawberry.execution")
logger.disabled = True
debug_logger = RichGraphQLLogger(
    log_context_keys=[
        "request",
    ]
)


class RichLoggerExtension(Extension):
    def __init__(self, logger: RichGraphQLLogger):
        self.debug_logger = logger

    def on_request_end(self):
        if self.execution_context.errors:
            self.debug_logger.print_errors(
                self.execution_context.errors,
                self.execution_context,
            )


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> int:
        raise ValueError
        return 139


schema = SchemaWithRichLogger(
    query=Query,
    extensions=[RichLoggerExtension(debug_logger)],
)
