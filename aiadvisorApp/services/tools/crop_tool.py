from .base_tool import BaseTool
from ..entity_extractor import EntityExtractor

from sqlApp.models import Crop, ProductionCycle


class CropTool(BaseTool):

    name = "Crop"

    description = "Answers crop-related questions."

    keywords = [
        "crop",
        "crops",
        "tomato",
        "cucumber",
        "pepper",
        "lettuce",
        "plant",
        "planted",
    ]

    def can_handle(self, question):

        question = question.lower()

        return any(word in question for word in self.keywords)

    def execute(self, question):

        crop = EntityExtractor.extract_crop(question)

        if crop:

            cycles = ProductionCycle.objects.filter(
                crop_variety__crop=crop
            ).count()

            return f"""
🌱 Crop Information

Crop:
{crop.crop_name}

Production Cycles:
{cycles}
"""

        total = Crop.objects.count()

        crops = Crop.objects.all().order_by("crop_name")

        names = ", ".join(c.crop_name for c in crops)

        return f"""
🌱 Farm Crops

Total Crops:
{total}

Available Crops:

{names}
"""