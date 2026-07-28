from .plan import Plan
from .parameter_extractor import ParameterExtractor

from .tools.analysis_tool import AnalysisTool
from .tools.production_cycle_tool import ProductionCycleTool
from .tools.greenhouse_crop_tool import GreenhouseCropTool
from .tools.farm_knowledge_tool import FarmKnowledgeTool
from .tools.farm_status_tool import FarmStatusTool
from .tools.crop_tool import CropTool
from .tools.harvest_tool import HarvestTool
from .tools.greenhouse_tool import GreenhouseTool
from .tools.general_agriculture_tool import GeneralAgricultureTool


class Planner:

    @staticmethod
    def plan(question):

        parameters = ParameterExtractor.extract(question)

        q = question.lower()

        plan = Plan()

        plan.original_question = question
        plan.crop = parameters.crop
        plan.greenhouse = parameters.greenhouse

        ###########################################################
        # GREENHOUSE OCCUPANCY
        ###########################################################

        if "greenhouse" in q and any(text in q for text in [

            "occupied",
            "occupancy",
            "most occupied",
            "least occupied",
            "empty beds",
            "available beds",

        ]):

            plan.intent = "greenhouse_occupancy"
            plan.tools = [FarmStatusTool]

            return plan

        ###########################################################
        # 1. ANALYSIS QUESTIONS
        ###########################################################

        
        if any(word in q for word in [
            "highest",
            "lowest",
            "best",
            "better",
            "compare",
            "worst",
            "most",
            "least",
            "less",
            
        ]):
            plan.intent = "analysis"
            plan.tools = [AnalysisTool]
            return plan

        ###########################################################
        # 2. PRODUCTION CYCLE QUESTIONS
        ###########################################################

        # Which crops are ready for harvest?
        if any(text in q for text in [

            "ready for harvest",
            "ready to harvest",
            "which crops are ready",
            "harvest today",
            "ready now",

        ]):

            plan.intent = "ready_harvest"
            plan.tools = [ProductionCycleTool]
            return plan

        # What stage is tomato?
        if plan.crop and any(word in q for word in [

            "stage",
            "status",
            "growth stage",
            "current stage",

        ]):

            plan.intent = "crop_stage"
            plan.tools = [ProductionCycleTool]
            return plan

        # When was cucumber transplanted?
        if plan.crop and any(word in q for word in [

            "transplant",
            "transplanted",
            "transplanting",

        ]):

            plan.intent = "transplant_date"
            plan.tools = [ProductionCycleTool]
            return plan

        # When is the next harvest?
        if any(text in q for text in [

            "next harvest",
            "first harvest",
            "upcoming harvest",
            "harvest date",
            "when is harvest",
            "when will harvest",

        ]):

            plan.intent = "next_harvest"
            plan.tools = [ProductionCycleTool]
            return plan

        ###########################################################
        # 3. FARM KNOWLEDGE QUESTIONS
        ###########################################################

        # Which crop is currently growing?
        if any(text in q for text in [

            "currently growing",
            "current crop",
            "growing now",
            "what is growing",
            "which crop is growing",

        ]):

            plan.intent = "current_crop"
            plan.tools = [FarmKnowledgeTool]
            return plan

        ###########################################################
        # 4. GREENHOUSE + CROP QUESTIONS
        ###########################################################

        # Which greenhouse grows tomatoes?
        if plan.crop and any(word in q for word in [

            "greenhouse",
            "where",
            "which greenhouse",
            "from which greenhouse",

        ]):

            plan.intent = "greenhouse_crop"
            plan.tools = [GreenhouseCropTool]
            return plan

        ###########################################################
        # 5. GREENHOUSE STATUS QUESTIONS
        ###########################################################

        # What is happening in Greenhouse 1?
        if plan.greenhouse and any(word in q for word in [

            "happening",
            "status",
            "summary",
            "inside",
            "activity",
            "activities",
            "doing",
            "going on",
            "currently",

        ]):

            plan.intent = "greenhouse_summary"
            plan.tools = [FarmStatusTool]
            return plan

        ###########################################################
        # 6. GENERIC CROP QUESTIONS
        ###########################################################

        # Tell me about tomato
        # Show tomato information stored in YOUR database.
        if plan.crop:

            plan.intent = "crop"
            plan.tools = [CropTool]
            return plan

        ###########################################################
        # 7. GENERIC HARVEST QUESTIONS
        ###########################################################

        # What is the total production?
        # Harvest in Greenhouse 1
        # Tomato harvest
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

        ###########################################################
        # 8. GENERIC GREENHOUSE QUESTIONS
        ###########################################################

        # How many greenhouses do we have?
        # Show all greenhouses.
        if "greenhouse" in q:

            plan.intent = "greenhouse"
            plan.tools = [GreenhouseTool]
            return plan

        ###########################################################
        # 9. GENERAL AGRICULTURE (Gemini later)
        ###########################################################

        plan.intent = "general"
        plan.tools = [GeneralAgricultureTool]

        return plan