from .plan import Plan
from .parameter_extractor import ParameterExtractor

from .tools.harvest_tool import HarvestTool
from .tools.greenhouse_tool import GreenhouseTool
from .tools.greenhouse_crop_tool import GreenhouseCropTool
from .tools.analysis_tool import AnalysisTool
from .tools.crop_tool import CropTool
from .tools.general_agriculture_tool import GeneralAgricultureTool


class Planner:

    @staticmethod
    def plan(question):

        parameters = ParameterExtractor.extract(question)

        crop = parameters.crop
        greenhouse = parameters.greenhouse

        q = question.lower()

        plan = Plan()

        plan.original_question = question
        plan.crop = crop
        plan.greenhouse = greenhouse

        # Highest harvest
        if any(word in q for word in [
            "highest",
            "best",
            "most",
        ]):

            plan.intent = "analysis"
            plan.tools = [AnalysisTool]

            return plan

        # Which greenhouse has tomatoes?
        if crop and "greenhouse" in q:

            plan.intent = "greenhouse_crop"
            plan.tools = [GreenhouseCropTool]

            return plan

        # Tell me about tomato
        if crop:

            plan.intent = "crop"
            plan.tools = [CropTool]

            return plan

        # Greenhouse summary
        if "greenhouse" in q:

            plan.intent = "greenhouse"
            plan.tools = [GreenhouseTool]

            return plan

        # Harvest
        if any(word in q for word in [

            "harvest",
            "yield",
            "production",
            "kg",
            "produce",

        ]):

            plan.intent = "harvest"
            plan.tools = [HarvestTool]

            return plan

        plan.intent = "general"
        plan.tools = [GeneralAgricultureTool]

        return plan