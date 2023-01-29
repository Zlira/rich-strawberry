# Rich Strawberry
_This is a work in progress!_

`rich-strawberry` is a small add-on for the [strawberry-graphql](https://github.com/strawberry-graphql/strawberry) library that uses [rich](https://github.com/Textualize/rich) to print error information nicely.

## Basic Example
At the moment, you have to use a special `SchemaWithRichLogger` class when defining your schema to use the `RichGraphQLLogger`. Here's a basic example:
```python
import strawberry

from rich_strawberry import SchemaWithRichLogger


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> int:
        raise ValueError


schema = SchemaWithRichLogger(query=Query)
```

This will give you the following output in the console for the query `query { version }`:

![Basic Output](https://github.com/Zlira/rich-strawberry/raw/main/imgs/basic.svg)

## Configuration
### Suppressing frames
By default the logger uses `rich`'es [feature](https://rich.readthedocs.io/en/stable/traceback.html#suppressing-frames) to suppress the frames from `graphql` and `strawberry-graphql` libraries. You can configure the list of modules for which the frames will be suppressed. For example, if you want the full traceback:
```python
import strawberry

from rich_strawberry import RichGraphQLLogger, SchemaWithRichLogger


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> int:
        raise ValueError


debug_logger = RichGraphQLLogger(suppress_traceback_from=[])
schema = SchemaWithRichLogger(query=Query, debug_logger=debug_logger)
```
Here's the full console output:

![Output Without Frame Suppression](https://github.com/Zlira/rich-strawberry/raw/main/imgs/without_frame_suppression.svg)

### Logging context
You can also configure some values from the context to be logged on error.
```python
import strawberry

from rich_strawberry import RichGraphQLLogger, SchemaWithRichLogger


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> int:
        raise ValueError


debug_logger = RichGraphQLLogger(log_context_keys=("request",))
schema = SchemaWithRichLogger(query=Query, debug_logger=debug_logger)
```
This will use `rich.inspect` to print that context value into the console:


![Output With Request](https://github.com/Zlira/rich-strawberry/raw/main/imgs/with_request.svg)

❗ This feature is not very well tested with different integrations so it might not work as expected.
