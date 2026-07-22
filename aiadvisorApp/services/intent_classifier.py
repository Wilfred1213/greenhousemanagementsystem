from dataclasses import dataclass

class IntentClassifier:
    
    @staticmethod
    def classify(question):

        question = question.lower()

        if any(word in question for word in [
            "greenhouse",
            "bed",
            "bay",
        ]):

            return IntentResult(

                intent="greenhouse",

                confidence=0.95

            )

        if any(word in question for word in [
            "harvest",
            "yield",
            "production",
            "kg",
        ]):

            return IntentResult(

                intent="harvest",

                confidence=0.95

            )

        return IntentResult(

            intent="general",

            confidence=0.50

        )

@dataclass
class IntentResult:

    intent: str

    confidence: float