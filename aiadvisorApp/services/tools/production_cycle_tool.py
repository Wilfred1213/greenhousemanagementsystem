from .base_tool import BaseTool

from sqlApp.models import ProductionCycle
from django.utils import timezone


class ProductionCycleTool(BaseTool):

    name = "ProductionCycle"

    description = "Answers production cycle questions."

    keywords = []

    def execute(self, plan):
        print("=" * 50)
        print("ProductionCycleTool.execute()")
        print("Intent:", plan.intent)
        
        if plan.intent == "transplant_date":
            return self.transplant_date(plan)

        elif plan.intent == "next_harvest":
            return self.next_harvest(plan)

        elif plan.intent == "crop_stage":
            return self.crop_stage(plan)
        elif plan.intent == "ready_harvest":
            return self.ready_harvest(plan)

        return None
        
    def transplant_date(self, plan):
    
        if not plan.crop:
            return None

        cycle = (
            ProductionCycle.objects
            .filter(
                crop_variety__crop=plan.crop
            )
            .order_by("-actual_transplant_date")
            .first()
        )

        if not cycle:

            return {

                "tool": "production_cycle",

                "status": "not_found",

                "data": {}

            }

        return {

            "tool": "production_cycle",

            "status": "success",

            "data": {

                "production": "transplant_date",

                "crop": cycle.crop_variety.crop.crop_name,

                "date": cycle.actual_transplant_date

            }

        }
    

    def next_harvest(self, plan):

        today = timezone.now().date()

        cycle = (
            ProductionCycle.objects
            .filter(
                expected_first_harvest__gte=today
            )
            .order_by("expected_first_harvest")
            .select_related(
                "crop_variety__crop",
                "greenhouse"
            )
            .first()
        )
        print("="*50)
        print("NEXT HARVEST")
        print("Today:", today)
        print("Cycle:", cycle)

        if not cycle:

            return {
                "tool": "production_cycle",
                "status": "not_found",
                "data": {}
            }

        return {

            "tool": "production_cycle",

            "status": "success",

            "data": {

                "production": "next_harvest",

                "crop": cycle.crop_variety.crop.crop_name,

                "greenhouse": cycle.greenhouse.greenhouse_name,

                "date": cycle.expected_first_harvest

            }

        }
    def crop_stage(self, plan):
    
        if not plan.crop:
            return None

        cycle = (
            ProductionCycle.objects
            .filter(
                crop_variety__crop=plan.crop
            )
            .order_by("-created_at")
            .first()
        )

        if not cycle:

            return {
                "tool": "production_cycle",
                "status": "not_found",
                "data": {}
            }

        return {

            "tool": "production_cycle",

            "status": "success",

            "data": {

                "production": "crop_stage",

                "crop": cycle.crop_variety.crop.crop_name,

                "stage": cycle.status

            }

        }
    def ready_harvest(self, plan):
        print("=" * 50)
        print("ENTERED ready_harvest()")
        cycles = (

            ProductionCycle.objects

            .filter(

                status="Harvesting"

            )

            .select_related(

                "crop_variety__crop",
                "greenhouse"

            )

        )

        if not cycles.exists():

            return {

                "tool": "production_cycle",

                "status": "not_found",

                "data": {}

            }

        harvests = []

        for cycle in cycles:

            harvests.append({

                "crop": cycle.crop_variety.crop.crop_name,

                "greenhouse": cycle.greenhouse.greenhouse_name,

            })
        if not cycles.exists():
    
            print("No production cycles are in Harvesting status.")

            return {
                "tool": "production_cycle",
                "status": "not_found",
                "data": {}
            }
        if not cycles.exists():
    
            print("No production cycles are in Harvesting status.")

            return {
                "tool": "production_cycle",
                "status": "not_found",
                "data": {}
            }

        return {

            "tool": "production_cycle",

            "status": "success",

            "data": {

                "production": "ready_harvest",

                "harvests": harvests

            }

        }