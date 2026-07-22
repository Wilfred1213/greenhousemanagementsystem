from .base_tool import BaseTool
from ..entity_extractor import EntityExtractor
from sqlApp.models import ProductionCycle


class GreenhouseCropTool(BaseTool):

    name = "Greenhouse Crop"

    description = "Shows where crops are planted."

    keywords = [
        "greenhouse",
        "grow",
        "planted",
        "which greenhouse",
    ]

    def execute(self, question):

        # crop = self.extract_crop(question)
        crop = EntityExtractor.extract_crop(question)

        if not crop:
            return None

        cycles = (
            ProductionCycle.objects
            .filter(
                crop_variety__crop=crop
            )
            .select_related(
                "greenhouse"
            )
        )

        if not cycles.exists():
            return f"No greenhouse is currently growing {crop.crop_name}."

        names = []

        for cycle in cycles:

            if cycle.greenhouse:

                names.append(cycle.greenhouse.greenhouse_name)

        names = sorted(set(names))

        greenhouse_list = "\n".join(
            f"• {name}"
            for name in names
        )

        return f"""
🌱 {crop.crop_name}

Currently planted in:

{greenhouse_list}
"""