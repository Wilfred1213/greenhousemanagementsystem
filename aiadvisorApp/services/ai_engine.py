from .tool_registry import ToolRegistry
from .tools.general_agriculture_tool import GeneralAgricultureTool
from .intent_router import IntentRouter
from .planner import Planner
from .response_composer import ResponseComposer


class KwasariAI:

    def ask(self, question, context=None):

        print("=" * 50)
        print("Conversation Context")
        print(context)
        print("=" * 50)

        intent = IntentRouter.detect(question)

        print("=" * 50)
        print("Detected Intent:", intent)
        print("=" * 50)


        tools = Planner.plan(question)

        responses = []

        for tool in tools:

            result = tool().execute(question)

            if result:
                responses.append(result)

        return ResponseComposer.compose(
            question,
            responses
)

        # return GeneralAgricultureTool().execute(question)



# from .tool_registry import ToolRegistry
# from .tools.general_agriculture_tool import GeneralAgricultureTool
# from .intent_router import IntentRouter



# class KwasariAI:

#     def ask(self, question, context=None):

#         print("=" * 50)
#         print("Conversation Context")
#         print(context)
#         print("=" * 50)

#         # tools = ToolRegistry.get_tools()
#         intent = IntentRouter.detect(question)

#         print("="*50)
#         print("Detected Intent:", intent)
#         print("="*50)

#         tool = ToolRegistry.get_tool(intent)

#         return tool().execute(question)

#         # -----------------------------
#         # Step 1: Find matching tools
#         # -----------------------------
#         selected_tools = []

#         for tool in tools:

#             if tool.can_handle(question):

#                 selected_tools.append(tool)

#         # -----------------------------
#         # Step 2: Execute them
#         # -----------------------------
#         responses = []

#         for tool in selected_tools:

#             result = tool.execute(question)

#             if result:

#                 responses.append(result)

#         # -----------------------------
#         # Step 3: Return combined answer
#         # -----------------------------
#         if responses:

#             return "\n\n".join(responses)

#         # -----------------------------
#         # Step 4: Nothing matched
#         # -----------------------------
#         return GeneralAgricultureTool().execute(question)