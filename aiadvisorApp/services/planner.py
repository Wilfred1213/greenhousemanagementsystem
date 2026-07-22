from .intent_router import IntentRouter
from .tool_registry import ToolRegistry
from .entity_extractor import EntityExtractor


class Planner:

    @classmethod
    def plan(cls, question):

        question = question.lower()

        tools = []

        # First tool from the intent
        intent = IntentRouter.detect(question)

        tools.append(
            ToolRegistry.get_tool(intent)
        )

        crop = EntityExtractor.extract_crop(question)

        # -------------------------
        # Crop + greenhouse question
        # -------------------------

        if crop and "greenhouse" in question:

            tools.append(
                ToolRegistry.get_tool("greenhouse_crop")
            )

        # -------------------------
        # Crop question
        # -------------------------

        if crop:

            tools.append(
                ToolRegistry.get_tool("harvest")
            )

        # -------------------------
        # Analysis
        # -------------------------

        if any(word in question for word in [
            "highest",
            "best",
            "lowest",
            "most",
            "compare",
        ]):

            tools.append(
                ToolRegistry.get_tool("analysis")
            )

        # Remove duplicates

        return list(dict.fromkeys(tools))

# from .intent_router import IntentRouter
# from .tool_registry import ToolRegistry


# class Planner:

#     @classmethod
#     def plan(cls, question):

#         question = question.lower()

#         tools = []

#         intent = IntentRouter.detect(question)

#         # First tool from intent
#         tools.append(ToolRegistry.get_tool(intent))

#         # Multi-tool rules

#         if "greenhouse" in question and any(
#             crop in question
#             for crop in [
#                 "tomato",
#                 "cucumber",
#                 "pepper",
#                 "carrot",
#                 "potato",
#             ]
#         ):
#             tools.append(
#                 ToolRegistry.get_tool("crop")
#             )

#         if "highest" in question or "best" in question:
#             tools.append(
#                 ToolRegistry.get_tool("harvest")
#             )

#         return list(dict.fromkeys(tools))