from dataclasses import dataclass, field


@dataclass
class Plan:

    original_question: str = ""

    intent: str = ""

    crop: object = None

    greenhouse: object = None

    season: object = None

    month: str = None

    year: int = None

    tools: list = field(default_factory=list)