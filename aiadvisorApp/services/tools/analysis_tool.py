from .base_tool import BaseTool

from sqlApp.models import Harvest

from django.db.models import Sum


class AnalysisTool(BaseTool):

    name = "Analysis"

    description = "Compares farm performance."

    keywords = [
        "best",
        "highest",
        "lowest",
        "compare",
        "better",
        "most",
    ]
    def execute(self, plan):
    
        # question = question.lower()
        question = plan.original_question.lower()

        if "crop" in question:
    
            if any(w in question for w in ("highest", "best", "most")):
                return self.best_crop()

            if any(w in question for w in ("lowest", "least")):
                return self.lowest_crop()

        elif "greenhouse" in question:

            if any(w in question for w in ("highest", "best", "most")):
                return self.best_greenhouse()

            if any(w in question for w in ("lowest", "least")):
                return self.lowest_greenhouse()

        return None

        # if "crop" in question:

        #     if any(word in question for word in [
        #         "highest",
        #         "best",
        #         "most",
        #     ]):

        #         return self.best_crop()

        #     if any(word in question for word in [
        #         "lowest",
        #         "least",
        #     ]):

        #         return self.lowest_crop()

        # if "greenhouse" in question:

        #     if any(word in question for word in [
        #         "highest",
        #         "best",
        #         "most",
        #     ]):

        #         return self.best_greenhouse()

        #     if any(word in question for word in [
        #         "lowest",
        #         "least",
        #     ]):

        #         return self.lowest_greenhouse()

        # return None
    
    def best_crop(self):
    
        highest = (
            Harvest.objects
            .values(
                "production_cycle_bed__production_cycle__crop_variety__crop__crop_name"
            )
            .annotate(
                total=Sum("quantity_kg")
            )
            .order_by("-total")
            .first()
        )

        if not highest:

            return {

                "tool": "analysis",

                "status": "not_found",

                "data": {}

            }

        return {

            "tool": "analysis",

            "status": "success",

            "data": {

                "analysis": "highest_crop",

                "crop": highest[
                    "production_cycle_bed__production_cycle__crop_variety__crop__crop_name"
                ],

                "quantity_kg": float(
                    highest["total"]
                )

            }

        }
    def lowest_crop(self):
    
        data = (
            Harvest.objects
            .values(
                "production_cycle_bed__production_cycle__crop_variety__crop__crop_name"
            )
            .annotate(
                total=Sum("quantity_kg")
            )
            .order_by("total")
        )

        if not data:
            return "No harvest records found."

        crop = data[0]

        return {

    "tool": "analysis",

    "status": "success",

    "data": {

        "analysis": "lowest_crop",

        "crop": crop[
            "production_cycle_bed__production_cycle__crop_variety__crop__crop_name"
        ],

        "quantity_kg": float(crop["total"])

    }

}

    def best_greenhouse(self):

        data = (
            Harvest.objects
            .values(
                "production_cycle_bed__bed__bay__greenhouse__greenhouse_name"
            )
            .annotate(
                total=Sum("quantity_kg")
            )
            .order_by("-total")
        )

        if not data:

            return "There are no harvest records yet."

        winner = data[0]

        return {

            "tool": "analysis",

            "status": "success",

            "data": {

                "analysis": "highest_greenhouse",

                "greenhouse": winner[
                    "production_cycle_bed__bed__bay__greenhouse__greenhouse_name"
                ],

                "quantity_kg": float(winner["total"])

            }

        }
    
    def lowest_greenhouse(self):
    
        data = (
            Harvest.objects
            .values(
                "production_cycle_bed__bed__bay__greenhouse__greenhouse_name"
            )
            .annotate(
                total=Sum("quantity_kg")
            )
            .order_by("total")
        )

        if not data:

            return {

                "tool": "analysis",

                "status": "not_found",

                "data": {}

            }

        greenhouse = data[0]

        return {

            "tool": "analysis",

            "status": "success",

            "data": {

                "analysis": "lowest_greenhouse",

                "greenhouse": greenhouse[
                    "production_cycle_bed__bed__bay__greenhouse__greenhouse_name"
                ],

                "quantity_kg": float(greenhouse["total"])

            }

        }
        