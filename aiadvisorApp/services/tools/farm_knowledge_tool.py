from .base_tool import BaseTool

from sqlApp.models import (
    ProductionCycle,
    Bed
)

from django.db.models import Count


class FarmKnowledgeTool(BaseTool):

    name = "FarmKnowledge"

    description = "Answers questions about current farm activities."

    keywords = []

    def execute(self, plan):

        if plan.intent == "current_crop":
            return self.current_crops()

        elif plan.intent == "bed_status":
            return self.bed_status()

        elif plan.intent == "greenhouse_status":
            return self.greenhouse_status()

        return None

    def current_crops(self):
    
        cycles = ProductionCycle.objects.filter(

                status__in=[

                    "Growing",
                    "Harvesting"

                ]

            ).select_related(
                "crop_variety__crop"
            )
        

        if not cycles.exists():

            return {
                "tool": "farm",
                "status": "not_found",
                "data": {}
            }

        crops = sorted(set(

            cycle.crop_variety.crop.crop_name

            for cycle in cycles

        ))

        return {

            "tool": "farm",

            "status": "success",

            "data": {

                "knowledge": "current_crop",

                "crops": crops,

                "count": len(crops)

            }

        }

    def bed_status(self):
    
        occupied = Bed.objects.filter(
            status="Occupied"
        ).count()

        available = Bed.objects.filter(
            status="Available"
        ).count()

        return {

            "tool":"farm",

            "status":"success",

            "data":{

                "knowledge":"bed_status",

                "occupied":occupied,

                "available":available

            }

        }
    def greenhouse_status(self):
    
        active = (
            ProductionCycle.objects
            .filter(
                status__in=[
                    "Growing",
                    "Harvesting"
                ]
            )
            .values(
                "greenhouse__greenhouse_name"
            )
            .distinct()
        )

        return {

            "tool":"farm",

            "status":"success",

            "data":{

                "knowledge":"greenhouse_status",

                "greenhouses":[

                    g["greenhouse__greenhouse_name"]

                    for g in active

                ]

            }

        }