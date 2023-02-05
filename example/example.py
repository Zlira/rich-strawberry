import logging

import strawberry

from rich_strawberry import RichGraphQLLogger, RichLoggerExtension

logger = logging.getLogger("strawberry.execution")
logger.disabled = True


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> int:
        raise ValueError


debug_logger = RichGraphQLLogger(log_context_keys=("request",))
schema = strawberry.Schema(
    query=Query, extensions=[RichLoggerExtension(logger=debug_logger)]
)
