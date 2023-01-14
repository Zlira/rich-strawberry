import strawberry
from rich_strawberry import SchemaWithRichLogger, RichGraphQLLogger


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> int:
        raise ValueError
        return 139


debug_logger = RichGraphQLLogger(log_context_keys=("solpavchek", "request"))
schema = SchemaWithRichLogger(query=Query, debug_logger=debug_logger)
