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

This will give you the following output in the console:

![Features](https://github.com/Zlira/rich-strawberry/raw/main/imgs/basic.svg)
