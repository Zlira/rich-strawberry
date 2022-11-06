import re
from enum import Enum
from typing import Type


class LineType(Enum):
    FILE_NAME = "file_name"
    FILE_LINE = "file_line"
    BREAK = "break"


class TraceBackParser:
    panel_end_pattern = re.compile(r"^╰─+╯")
    line_patterns: dict[LineType, re.Pattern] = {
        LineType.BREAK: re.compile(r"^\s*$"),
        LineType.FILE_LINE: re.compile(r"^(❱ +)?\d+"),
        LineType.FILE_NAME: re.compile(r"^\/|[a-zA-Z]"),
    }

    def __init__(self):
        self.state: "State" = InFileName(self)
        self.in_traceback = False

        self.curr_file_name: str = ""
        self.curr_file_lines: list[str] = []
        self.result: dict[str, list[str]] = {}

    def finalize_curr_file(self):
        self.result[self.curr_file_name] = self.curr_file_lines
        self.curr_file_name = ""
        self.curr_file_lines = []

    def setState(self, state_cls: Type["State"]) -> None:
        self.state = state_cls(self)

    def get_line_type(self, line: str) -> LineType:
        for line_type, pattern in self.line_patterns.items():
            if pattern.match(line):
                return line_type
        raise ValueError("Could not determine line type", line)

    def parse(self, lines):
        for line in lines:
            if "Traceback (most recent call last)" in line:
                self.in_traceback = True
                continue
            if self.in_traceback and self.panel_end_pattern.match(line):
                self.in_traceback = False
            if not self.in_traceback:
                continue
            line_type = self.get_line_type(line)
            handler_name = f"handle_{line_type.value}"
            getattr(self.state, handler_name)(line)
        self.finalize_curr_file()


class State:
    def __init__(self, parser: TraceBackParser):
        self.parser = parser

    def handle_file_name(self, line) -> None:
        raise NotImplementedError

    def handle_file_line(self, line) -> None:
        raise NotImplementedError

    def handle_break(self, line) -> None:
        raise NotImplementedError


class InFileName(State):
    def handle_file_name(self, line) -> None:
        self.parser.curr_file_name += line

    def handle_break(self, line) -> None:
        self.parser.state = InBreak(self.parser)


class InBreak(State):
    def handle_file_name(self, line) -> None:
        self.parser.finalize_curr_file()
        self.parser.curr_file_name = line
        self.parser.state = InFileName(self.parser)

    def handle_file_line(self, line) -> None:
        assert not self.parser.curr_file_lines
        self.parser.curr_file_lines.append(line)
        self.parser.state = InFileLine(self.parser)


class InFileLine(State):
    def handle_file_line(self, line) -> None:
        self.parser.curr_file_lines.append(line)

    def handle_break(self, line) -> None:
        self.parser.state = InBreak(self.parser)
