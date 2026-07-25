class ToolExecutor:
    
    @staticmethod
    def execute(plan):

        responses = []

        for tool in plan.tools:

            result = tool().execute(plan)

            if result:

                responses.append(result)

        return responses

        # temporal

        for tool in plan.tools:
        
            result = tool().execute(plan)

            print("=" * 50)
            print("RESULT FROM TOOL")
            print(result)

            if result:
                responses.append(result)