from django.db.models import Sum

from .base_tool import BaseTool

from sqlApp.models import (
    ProductionCycle,
    Harvest,
)


class FarmStatusTool(BaseTool):

    name = "Farm Status"

    description = "Answers greenhouse and production cycle questions."

    keywords = []

    def execute(self, plan):

        if plan.intent == "greenhouse_summary":
            return self.greenhouse_summary(plan)

        return None

    def greenhouse_summary(self, plan):

        greenhouse = plan.greenhouse

        if greenhouse is None:

            return {
                "tool": "farm_status",
                "status": "not_found",
                "data": {}
            }

        cycle = (
            ProductionCycle.objects
            .filter(
                greenhouse=greenhouse,
                status__in=[
                    "Growing",
                    "Harvesting",
                ]
            )
            .select_related(
                "crop_variety__crop",
                "season"
            )
            .first()
        )

        if cycle is None:

            return {
                "tool": "farm_status",
                "status": "not_found",
                "data": {}
            }

        total_harvest = (
            Harvest.objects.filter(
                production_cycle_bed__production_cycle=cycle
            )
            .aggregate(
                total=Sum("quantity_kg")
            )["total"] or 0
        )

        return {

            "tool": "farm_status",

            "status": "success",

            "data": {

                "knowledge": "greenhouse_summary",

                "greenhouse": greenhouse.greenhouse_name,

                "crop": cycle.crop_variety.crop.crop_name,

                "status": cycle.status,

                "season": cycle.season.season_name,

                "cycle": cycle.cycle_number,

                "transplant_date": cycle.actual_transplant_date,

                "next_harvest": cycle.expected_first_harvest,

                "beds": cycle.beds_used,

                "harvest": float(total_harvest),

            }

        }