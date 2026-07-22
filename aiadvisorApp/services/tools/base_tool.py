from abc import ABC, abstractmethod


class BaseTool(ABC):

    name = ""

    description = ""

    keywords = []

    def can_handle(self, question):

        question = question.lower()

        return any(

            keyword.lower() in question

            for keyword in self.keywords

        )

    @abstractmethod
    def execute(self, question):

        pass