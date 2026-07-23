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

            if any(word in question for word in [
                "highest",
                "best",
                "most",
            ]):

                return self.best_crop()

            if any(word in question for word in [
                "lowest",
                "least",
            ]):

                return self.lowest_crop()

        if "greenhouse" in question:

            if any(word in question for word in [
                "highest",
                "best",
                "most",
            ]):

                return self.best_greenhouse()

            if any(word in question for word in [
                "lowest",
                "least",
            ]):

                return self.lowest_greenhouse()

        return None
    # def execute(self, question):

    #     question = question.lower()
    #     if "crop" in question and (
    #         "highest" in question
    #         or "best" in question
    #         or "most" in question
    #     ):

    #         return self.highest_crop()

    #     if "greenhouse" in question and (
    #         "best" in question
    #         or "highest" in question
    #         or "better" in question
    #         or "most" in question
    #     ):

    #         return self.best_greenhouse()

    #     return None
    def best_crop(self):
    
        data = (
            Harvest.objects
            .values(
                "production_cycle_bed__production_cycle__crop_variety__crop__crop_name"
            )
            .annotate(
                total=Sum("quantity_kg")
            )
            .order_by("-total")
        )

        if not data:
            return "No harvest records found."

        winner = data[0]

        return f"""
    🏆 Highest Harvest Crop

    {winner["production_cycle_bed__production_cycle__crop_variety__crop__crop_name"]}

    Total Harvest

    {winner["total"]} kg
    """
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

        return f"""
    📉 Lowest Harvest Crop

    {crop["production_cycle_bed__production_cycle__crop_variety__crop__crop_name"]}

    Total Harvest

    {crop["total"]} kg
    """

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

        return f"""
        🏆 Best Performing Greenhouse

        {winner["production_cycle_bed__bed__bay__greenhouse__greenhouse_name"]}

        Total Harvest

        {winner["total"]} kg
        """
    def highest_crop(self):
    
        data = (
            Harvest.objects
            .values(
                "production_cycle_bed__production_cycle__crop_variety__crop__crop_name"
            )
            .annotate(
                total=Sum("quantity_kg")
            )
            .order_by("-total")
        )

        if not data:
            return "No harvest records found."

        winner = data[0]

        return f"""
    🏆 Highest Harvested Crop

    Crop:
    {winner["production_cycle_bed__production_cycle__crop_variety__crop__crop_name"]}

    Total Harvest:
    {winner["total"]} kg
    """