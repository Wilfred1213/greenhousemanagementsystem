from .base_tool import BaseTool

from sqlApp.models import Greenhouse, Bed
from sqlApp.models import ProductionCycle



class GreenhouseTool(BaseTool):

    name = "Greenhouse"

    description = "Answers greenhouse questions."

    keywords = [
        "greenhouse",
        "bed",
        "bay",
        "occupancy",
        "available",
        "occupied",
    ]

    def can_handle(self, question):

        question = question.lower()

        greenhouse_words = [
            "greenhouse",
            "bed",
            "bay",
            "occupancy",
            "available",
            "occupied",
        ]

        return any(word in question for word in greenhouse_words)

    def execute(self, plan):

        print("=" * 50)
        print("Greenhouse Tool")
        print("Question:", plan.original_question)
        print("=" * 50)

        question = plan.original_question.lower()
        # crop = EntityExtractor.extract_crop(question)
        crop = plan.crop
        if crop:

            cycles = ProductionCycle.objects.filter(
                crop_variety__crop=crop
            ).select_related("greenhouse")

            if not cycles.exists():

                return f"No greenhouse is currently growing {crop.crop_name}."

            names = []

            for cycle in cycles:

                if cycle.greenhouse:

                    names.append(cycle.greenhouse.greenhouse_name)

            names = sorted(set(names))

            return f"""
    🌱 {crop.crop_name}

    Currently planted in:

    {chr(10).join(names)}
    """

        ...