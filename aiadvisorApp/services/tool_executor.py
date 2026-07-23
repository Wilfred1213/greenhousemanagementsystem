class ToolExecutor:
    
    @staticmethod
    def execute(plan):

        responses = []

        for tool in plan.tools:

            result = tool().execute(plan)

            if result:

                responses.append(result)

        return responses