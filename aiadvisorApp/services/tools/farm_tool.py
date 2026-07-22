from .base_tool import BaseTool

from sqlApp.models import (
    Greenhouse,
    Crop,
    Harvest,
)


class FarmTool(BaseTool):

    name = "Farm"

    description = "Overall farm information."

    keywords = [

        "farm",
        "overview",
        "summary",
        "status",
        "my farm",

    ]

    def execute(self, question):

        question = question.lower()

        greenhouses = Greenhouse.objects.count()
        crops = Crop.objects.count()
        harvests = Harvest.objects.count()

        # Overall summary
        if (
            "summary" in question
            or "overview" in question
            or "my farm" in question
            or "about my farm" in question
        ):

            return f"""
            🌱 Farm Summary

            Greenhouses : {greenhouses}

            Crops : {crops}

            Harvest Records : {harvests}
            """

        # Greenhouse count
        if "greenhouse" in question:

                        return f"""
            There are currently {greenhouses} greenhouses on the farm.
            """

        # Crop count
        if "crop" in question:

            return f"""
            There are currently {crops} crop records.
            """

        return f"""
            The farm currently contains:

            • {greenhouses} Greenhouses

            • {crops} Crops

            • {harvests} Harvest Records
            """