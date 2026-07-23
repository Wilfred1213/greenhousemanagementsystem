from .planner import Planner
from .query_rewriter import QueryRewriter
from .response_composer import ResponseComposer
from .tool_executor import ToolExecutor


class KwasariAI:

    def ask(self, question, context=None):

        print("=" * 50)
        print("Conversation Context")
        print(context)
        print("=" * 50)

        question = QueryRewriter.rewrite(
            question,
            context
        )

        plan = Planner.plan(question)

        print("=" * 50)
        print("Intent:", plan.intent)
        print("Crop:", plan.crop)
        print("Greenhouse:", plan.greenhouse)
        print("Tools:", [tool.__name__ for tool in plan.tools])
        print("=" * 50)

        responses = ToolExecutor.execute(plan)

        return ResponseComposer.compose(
            plan.original_question,
            responses
        )