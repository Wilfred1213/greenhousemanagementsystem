class ResponseComposer:
    
    @staticmethod
    def compose(question, responses):

        if not responses:
            return (
                "I'm sorry, I couldn't find enough information "
                "to answer that question."
            )

        if len(responses) == 1:
            return responses[0]

        answer = ""

        for response in responses:
            answer += response.strip()
            answer += "\n\n"

        return answer.strip()