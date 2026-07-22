from dataclasses import dataclass


@dataclass
class ToolResponse:

    success: bool

    title: str

    message: str