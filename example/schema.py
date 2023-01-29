import strawberry

from rich_strawberry import RichGraphQLLogger, SchemaWithRichLogger


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> int:
        raise ValueError
        return 139


debug_logger = RichGraphQLLogger(suppress_traceback_from=[])
schema = SchemaWithRichLogger(query=Query, debug_logger=debug_logger)
