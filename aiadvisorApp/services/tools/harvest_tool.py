from django.db.models import Sum

from .base_tool import BaseTool
from ..entity_extractor import EntityExtractor

from sqlApp.models import Harvest


class HarvestTool(BaseTool):

    name = "Harvest"

    description = "Answers harvest and production questions."

    keywords = [
        "harvest",
        "yield",
        "production",
        "produce",
        "kg",
    ]

    def can_handle(self, question):

        question = question.lower()

        harvest_words = [
            "harvest",
            "yield",
            "produce",
            "production",
            "kg",
        ]

        return any(word in question for word in harvest_words)

    def execute(self, question):

        crop = EntityExtractor.extract_crop(question)

        greenhouse = EntityExtractor.extract_greenhouse(question)

        # Temporary debugging
        print("=" * 50)
        print("Harvest Tool")
        print("Question:", question)
        print("Crop:", crop)
        print("Greenhouse:", greenhouse)
        print("=" * 50)

        # Start with all harvests
        harvests = Harvest.objects.all()

        # Filter by crop
        if crop:

            harvests = harvests.filter(
                production_cycle_bed__production_cycle__crop_variety__crop=crop
            )

        # Filter by greenhouse
        if greenhouse:

            harvests = harvests.filter(
                
                production_cycle_bed__production_cycle__greenhouse=greenhouse
            )

        total = harvests.aggregate(
            total=Sum("quantity_kg")
        )["total"] or 0

        crop_names = crop.crop_name if crop else "All Crops"

        greenhouse_names = greenhouse.greenhouse_name if greenhouse else "All Greenhouses"

        return f"""
            🌾 Harvest Summary

            Crop : {crop_names}

            Greenhouse : {greenhouse_names}

            Total Harvest : {total} kg
            """