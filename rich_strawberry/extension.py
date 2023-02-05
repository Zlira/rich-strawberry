from strawberry.extensions import Extension

from .logger import RichGraphQLLogger


class RichLoggerExtension(Extension):
    def __init__(self, logger: RichGraphQLLogger | None = None):
        self.debug_logger = logger or RichGraphQLLogger()

    def on_request_end(self):
        if self.execution_context.errors:
            self.debug_logger.print_errors(
                self.execution_context.errors,
                self.execution_context,
            )
