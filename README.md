# Rich Strawberry
_This is a work in progress!_

`rich-strawberry` is a small add-on for the [strawberry-graphql](https://github.com/strawberry-graphql/strawberry) library that uses [rich](https://github.com/Textualize/rich) to print error information nicely.

## Basic Example
You can use the `RichLoggerExtension` to get improved traceback in your application. However, you'll need to disable the
default logger to avoid logging every exception twice.

 Here's a basic example:
```python
import logging

import strawberry

from rich_strawberry import RichLoggerExtension

logger = logging.getLogger("strawberry.execution")
logger.disabled = True


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> int:
        raise ValueError


schema = strawberry.Schema(query=Query, extensions=[RichLoggerExtension()])
```

This will give you the following output in the console for the query `query { version }`:

![Basic Output](https://github.com/Zlira/rich-strawberry/raw/main/imgs/basic.svg)

## Configuration
### Suppressing frames
By default, the logger uses a [feature](https://rich.readthedocs.io/en/stable/traceback.html#suppressing-frames) from `rich` to suppress the frames from `graphql` and `strawberry-graphql` libraries. You can configure the list of modules for which the frames will be suppressed. For example, if you want the full traceback:
```python
import logging

import strawberry

from rich_strawberry import RichLoggerExtension, RichGraphQLLogger

logger = logging.getLogger("strawberry.execution")
logger.disabled = True


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> int:
        raise ValueError


debug_logger = RichGraphQLLogger(suppress_traceback_from=[])
schema = strawberry.Schema(
    query=Query, extensions=[RichLoggerExtension(logger=debug_logger)]
)
```
Here's the full console output:

![Output Without Frame Suppression](https://github.com/Zlira/rich-strawberry/raw/main/imgs/without_frame_suppression.svg)

### Logging context
You can also configure some values from the context to be logged on error.
```python
import logging

import strawberry

from rich_strawberry import RichLoggerExtension, RichGraphQLLogger

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
```
This will use `rich.inspect` to print that context value into the console:


![Output With Request](https://github.com/Zlira/rich-strawberry/raw/main/imgs/with_request.svg)

❗ This feature is not very well tested with different integrations so it might not work as expected.


## Using with subscription
At the moment of writing, subscriptions don't support extensions (check [this](https://github.com/strawberry-graphql/strawberry/pull/2430) merge request, maybe they already do!) So if you want to use the `RichGraphQLLogger` for your subscriptions, you'll need
to define a custom `Schema` class and overwrite its `process_errors` method:

```python
from typing import Optional

import strawberry
from strawberry.types import ExecutionContext
from graphql import GraphQLError

from rich_strawberry.logger import RichGraphQLLogger

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
```
You can see a full example with subscriptions [here](https://github.com/Zlira/rich-strawberry/blob/main/example/example_with_subscription.py).

Context values aren't logged for subscriptions.
